import sys
import flet as ft
import requests
from ui_login import build_login_view
from ui_products import build_products_view
from ui_sales import build_sales_view
from ui_settings import build_settings_view
from ui_customers import build_customers_view
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
                page.controls.append(build_login_view(page, on_login=on_login, language=current_language, show_back=len(nav_history) > 1, go_back=go_back))
            else:
                page.controls.append(build_dashboard_view(go_back=go_back))
        elif current_index == 1:
            page.controls.append(build_products_view(page, language=current_language, show_back=len(nav_history) > 1, go_back=go_back))
        elif current_index == 2:
            page.controls.append(build_sales_view(page, user_id=current_user, language=current_language, show_back=len(nav_history) > 1, go_back=go_back))
        elif current_index == 3:
            page.controls.append(build_settings_view(page, theme_mode=theme_mode, current_theme=current_theme, language=current_language, on_language_change=update_language, on_theme_change=update_theme, show_back=len(nav_history) > 1, go_back=go_back))
        elif current_index == 4:
            page.controls.append(build_customers_view(page, language=current_language, show_back=len(nav_history) > 1, go_back=go_back))
        page.update()

    def go_back():
        if len(nav_history) > 1:
            nav_history.pop()
            navigate(None)

    def on_login(user_id, role):
        nonlocal current_user, current_role
        current_user = user_id
        current_role = role
        nav_history.append(0)
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
        page.update()

    def fetch_analytics():
        try:
            response = requests.get("http://offlinepos:5000/api/sales/analytics")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Analytics fetch error: {str(e)}")
            return {"total_sales": 0, "sale_count": 0}

    def build_dashboard_view(go_back):
        analytics = fetch_analytics()
        return ft.Container(
            content=ft.Column([
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: go_back(),
                    tooltip="Back",
                    visible=len(nav_history) > 1
                ),
                ft.Text("Dashboard", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Text(f"Total Sales: ${analytics['total_sales']:.2f}", size=16),
                    ft.Text(f"Sale Count: {analytics['sale_count']}", size=16)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            padding=20,
            bgcolor=ft.colors.WHITE if current_theme == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
            border_radius=15,
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100)
        )

    # Navigation bar
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.icons.STORE, label="Products"),
            ft.NavigationBarDestination(icon=ft.icons.RECEIPT, label="Sales"),
            ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Settings"),
            ft.NavigationBarDestination(icon=ft.icons.PERSON, label="Customers")
        ],
        on_change=navigate,
        selected_index=0
    )

    # Initial view
    page.add(
        ft.Column([
            nav_bar,
            build_login_view(page, on_login=on_login, language=current_language, show_back=len(nav_history) > 1, go_back=go_back)
        ])
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
