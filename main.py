import sys
import flet as ft
import requests
import asyncio
from ui_login import build_login_view
from ui_products import build_products_view, build_products_view_unauthorized
from ui_sales import build_sales_view, build_sales_view_unauthorized
from ui_settings import build_settings_view
from ui_customers import build_customers_view, build_customers_view_unauthorized
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add current directory to sys.path to allow local imports
sys.path.append('/app')

def main(page: ft.Page):
    print("Starting main function...")
    page.title = "OfflinePOS"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.GREY_100

    # State for navigation
    current_user = None
    current_role = None
    current_language = "en"
    current_theme = ft.ThemeMode.LIGHT
    theme_mode = ft.Ref()
    nav_history = [0]

    # Navigation bar
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME, label="Dashboard"),
            ft.NavigationBarDestination(icon=ft.icons.STORE, label="Products"),
            ft.NavigationBarDestination(icon=ft.icons.RECEIPT, label="Sales"),
            ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Settings"),
            ft.NavigationBarDestination(icon=ft.icons.PERSON, label="Customers")
        ],
        on_change=lambda e: navigate(e),
        selected_index=0
    )

    def navigate(e):
        if e is not None:
            new_index = nav_bar.selected_index
            if new_index != nav_history[-1]:
                nav_history.append(new_index)
        page.controls.clear()
        current_index = nav_history[-1]
        nav_bar.selected_index = current_index
        if current_index == 0:
            if not current_user:
                content, start_monitoring = build_login_view(page, on_login=on_login, language=current_language, show_back=False, go_back=go_back)
                page.controls.append(ft.Column([nav_bar, content], scroll=ft.ScrollMode.AUTO))
                page.update()
                start_monitoring()
            else:
                content = build_dashboard_view(go_back=go_back)
                page.controls.append(ft.Column([nav_bar, content], scroll=ft.ScrollMode.AUTO))
                page.update()
        elif current_index == 1:
            if not current_user:
                content, populate = build_products_view_unauthorized(page, language=current_language, show_back=True, go_back=go_back)
                page.controls.append(ft.Column([nav_bar, content], scroll=ft.ScrollMode.AUTO))
                page.update()
                page.run_task(start_polling(populate))
            else:
                content, populate = build_products_view(page, language=current_language, show_back=True, go_back=go_back)
                page.controls.append(ft.Column([nav_bar, content], scroll=ft.ScrollMode.AUTO))
                page.update()
                page.run_task(start_polling(populate))
        elif current_index == 2:
            if not current_user:
                content, populate = build_sales_view_unauthorized(page, language=current_language, show_back=True, go_back=go_back)
                page.controls.append(ft.Column([nav_bar, content], scroll=ft.ScrollMode.AUTO))
                page.update()
                page.run_task(start_polling(populate))
            else:
                content, populate = build_sales_view(page, user_id=current_user, language=current_language, show_back=True, go_back=go_back)
                page.controls.append(ft.Column([nav_bar, content], scroll=ft.ScrollMode.AUTO))
                page.update()
                page.run_task(start_polling(populate))
        elif current_index == 3:
            content = build_settings_view(page, theme_mode=theme_mode, current_theme=current_theme, language=current_language, on_language_change=update_language, on_theme_change=update_theme, show_back=True, go_back=go_back)
            page.controls.append(ft.Column([nav_bar, content], scroll=ft.ScrollMode.AUTO))
            page.update()
        elif current_index == 4:
            if not current_user:
                content, populate = build_customers_view_unauthorized(page, language=current_language, show_back=True, go_back=go_back)
                page.controls.append(ft.Column([nav_bar, content], scroll=ft.ScrollMode.AUTO))
                page.update()
                page.run_task(start_polling(populate))
            else:
                content, populate = build_customers_view(page, language=current_language, show_back=True, go_back=go_back)
                page.controls.append(ft.Column([nav_bar, content], scroll=ft.ScrollMode.AUTO))
                page.update()
                page.run_task(start_polling(populate))

    async def start_polling(populate_func):
        while nav_bar.selected_index == nav_history[-1]:
            await asyncio.sleep(30)  # Poll every 30 seconds
            populate_func()

    def go_back():
        if len(nav_history) > 1:
            nav_history.pop()
            navigate(None)

    def on_login(user_id, role):
        nonlocal current_user, current_role
        current_user = user_id
        current_role = role
        nav_history = [0]  # Reset to dashboard after login
        navigate(None)

    def update_language(lang):
        nonlocal current_language
        current_language = lang
        navigate(None)

    def update_theme(new_theme):
        nonlocal current_theme
        current_theme = new_theme
        page.theme_mode = current_theme
        page.bgcolor = ft.colors.GREY_100 if current_theme == ft.ThemeMode.LIGHT else ft.colors.GREY_900
        navigate(None)  # Rebuild current view with new theme

    def fetch_analytics():
        try:
            response = requests.get("http://localhost:5000/api/sales/analytics")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Analytics fetch error: {str(e)}")
        return {"total_sales": 0, "sale_count": 0}

    def fetch_sales_data():
        try:
            response = requests.get("http://localhost:5000/api/sales")
            if response.status_code == 200:
                return response.json().get("sales", [])
        except Exception as e:
            print(f"Sales fetch error: {str(e)}")
        return []

    def build_dashboard_view(go_back):
        analytics = fetch_analytics()
        sales_data = fetch_sales_data()
        bgcolor = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800

        # Admin management buttons
        admin_controls = ft.Row([
            ft.ElevatedButton("Manage Products", on_click=lambda e: navigate(None), bgcolor=ft.colors.BLUE, color=ft.colors.WHITE),
            ft.ElevatedButton("Manage Sales", on_click=lambda e: navigate(None), bgcolor=ft.colors.GREEN, color=ft.colors.WHITE),
            ft.ElevatedButton("Manage Customers", on_click=lambda e: navigate(None), bgcolor=ft.colors.PURPLE, color=ft.colors.WHITE)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

        # Recent sales list
        sales_list = ft.ListView(expand=True, spacing=10)
        if sales_data:
            for sale in sales_data[-5:]:  # Show last 5 sales
                sales_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.RECEIPT),
                            title=ft.Text(f"Sale ID: {sale['id']}", size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Total: ${sale['total_amount']:.2f} | Method: {sale['payment_method']}", size=14),
                            trailing=ft.Text(sale['created_at'], size=12),
                        ),
                        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
                        border_radius=5,
                        padding=5
                    )
                )
        else:
            sales_list.controls.append(ft.Text("No recent sales", size=16, text_align="center"))

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda e: go_back(),
                        tooltip="Back",
                        visible=len(nav_history) > 1
                    ),
                    ft.ElevatedButton(
                        text="Logout",
                        on_click=lambda e: logout(),
                        bgcolor=ft.colors.RED,
                        color=ft.colors.WHITE
                    )
                ]),
                ft.Text("Admin Dashboard", size=20, weight=ft.FontWeight.BOLD),
                admin_controls,
                ft.Row([
                    ft.Text(f"Total Sales: ${analytics['total_sales']:.2f}", size=16),
                    ft.Text(f"Sale Count: {analytics['sale_count']}", size=16)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Text("Recent Sales", size=18, weight=ft.FontWeight.BOLD),
                sales_list
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, scroll=ft.ScrollMode.AUTO),
            padding=20,
            bgcolor=bgcolor,
            border_radius=15,
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_900)
        )

    def logout():
        nonlocal current_user, current_role
        current_user = None
        current_role = None
        nav_history = [0]
        requests.post("http://localhost:5000/api/logout")
        navigate(None)

    # Initial view
    page.add(
        ft.Column([
            nav_bar,
            build_login_view(page, on_login=on_login, language=current_language, show_back=False, go_back=go_back)[0]
        ], scroll=ft.ScrollMode.AUTO)
    )

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory and event.src_path.endswith('.py'):
            print(f"Change detected in {event.src_path}. Reloading Flet app...")
            page.update()

if __name__ == "__main__":
    ft.app(target=main, host="0.0.0.0", port=8000)
    observer = Observer()
    observer.schedule(ChangeHandler(), path=".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
