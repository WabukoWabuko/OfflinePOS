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

sys.path.append('/app')

def main(page: ft.Page):
    print("Starting main function...")
    page.title = "OfflinePOS - Premium"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.BLUE_50
    page.padding = 0

    current_user = None
    current_role = None
    current_language = "en"
    current_theme = ft.ThemeMode.LIGHT
    nav_index = 0

    def navigate(index):
        nonlocal nav_index
        nav_index = index
        sidebar.selected_index = nav_index
        page.controls.clear()
        if nav_index == 0:
            if not current_user:
                content, start_monitoring = build_login_view(page, on_login=on_login, language=current_language)
                page.controls.append(ft.Row([sidebar, content], expand=True))
                page.update()
                start_monitoring()
            else:
                content = build_dashboard_view()
                page.controls.append(ft.Row([sidebar, content], expand=True))
                page.update()
        elif nav_index == 1:
            if not current_user:
                content, populate = build_products_view_unauthorized(page, language=current_language)
                page.controls.append(ft.Row([sidebar, content], expand=True))
                page.update()
                populate()
                page.run_task(lambda: start_polling(populate))
            else:
                content, populate = build_products_view(page, language=current_language)
                page.controls.append(ft.Row([sidebar, content], expand=True))
                page.update()
                populate()
                page.run_task(lambda: start_polling(populate))
        elif nav_index == 2:
            if not current_user:
                content, populate = build_sales_view_unauthorized(page, language=current_language)
                page.controls.append(ft.Row([sidebar, content], expand=True))
                page.update()
                populate()
                page.run_task(lambda: start_polling(populate))
            else:
                content, populate = build_sales_view(page, user_id=current_user, language=current_language)
                page.controls.append(ft.Row([sidebar, content], expand=True))
                page.update()
                populate()
                page.run_task(lambda: start_polling(populate))
        elif nav_index == 3:
            if not current_user:
                content, populate = build_customers_view_unauthorized(page, language=current_language)
                page.controls.append(ft.Row([sidebar, content], expand=True))
                page.update()
                populate()
                page.run_task(lambda: start_polling(populate))
            else:
                content, populate = build_customers_view(page, language=current_language)
                page.controls.append(ft.Row([sidebar, content], expand=True))
                page.update()
                populate()
                page.run_task(lambda: start_polling(populate))
        elif nav_index == 4:
            content = build_settings_view(page, current_theme=current_theme, language=current_language,
                                          on_language_change=update_language, on_theme_change=update_theme)
            page.controls.append(ft.Row([sidebar, content], expand=True))
            page.update()

    async def start_polling(populate_func):
        while nav_index == sidebar.selected_index:
            await asyncio.sleep(30)
            populate_func()

    def on_login(user_id, role):
        nonlocal current_user, current_role
        current_user = user_id
        current_role = role
        navigate(0)

    def update_language(lang):
        nonlocal current_language
        current_language = lang
        navigate(nav_index)

    def update_theme(new_theme):
        nonlocal current_theme
        current_theme = new_theme
        page.theme_mode = current_theme
        page.bgcolor = ft.colors.BLUE_50 if current_theme == ft.ThemeMode.LIGHT else ft.colors.GREY_900
        navigate(nav_index)

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

    def fetch_top_products():
        try:
            response = requests.get("http://localhost:5000/api/products")
            if response.status_code == 200:
                products = response.json().get("products", [])
                return sorted(products, key=lambda x: x['stock'], reverse=True)[:3]
        except Exception as e:
            print(f"Top products fetch error: {str(e)}")
        return []

    def build_dashboard_view():
        analytics = fetch_analytics()
        sales_data = fetch_sales_data()
        top_products = fetch_top_products()

        metric_cards = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Total Sales", size=16, color=ft.colors.BLUE_900),
                    ft.Text(f"${analytics['total_sales']:.2f}", size=24, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor=ft.colors.WHITE,
                padding=20,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLUE_200),
                width=200,
                height=100
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Sale Count", size=16, color=ft.colors.BLUE_900),
                    ft.Text(str(analytics['sale_count']), size=24, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor=ft.colors.WHITE,
                padding=20,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLUE_200),
                width=200,
                height=100
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Daily Sales", size=16, color=ft.colors.BLUE_900),
                    ft.Text("$0.00", size=24, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor=ft.colors.WHITE,
                padding=20,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLUE_200),
                width=200,
                height=100
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        sales_list = ft.ListView(expand=True, spacing=10)
        if sales_data:
            for sale in sales_data[-5:]:
                sales_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.RECEIPT, color=ft.colors.BLUE_700),
                            title=ft.Text(f"Sale ID: {sale['id']}", size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Total: ${sale['total_amount']:.2f} | Method: {sale['payment_method']}", size=14),
                            trailing=ft.Text(sale['created_at'], size=12),
                        ),
                        bgcolor=ft.colors.WHITE,
                        border_radius=5,
                        padding=5
                    )
                )
        else:
            sales_list.controls.append(ft.Text("No recent sales", size=16, text_align="center"))

        top_products_list = ft.ListView(expand=True, spacing=10)
        if top_products:
            for product in top_products:
                top_products_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.STORE, color=ft.colors.BLUE_700),
                            title=ft.Text(product['name'], size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Price: ${product['price']:.2f} | Stock: {product['stock']}", size=14),
                        ),
                        bgcolor=ft.colors.WHITE,
                        border_radius=5,
                        padding=5
                    )
                )
        else:
            top_products_list.controls.append(ft.Text("No products available", size=16, text_align="center"))

        dashboard_content = ft.Column([
            ft.Row([
                ft.Text("Admin Dashboard", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                ft.ElevatedButton(
                    text="Logout",
                    on_click=lambda e: logout(),
                    bgcolor=ft.colors.RED_600,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            metric_cards,
            ft.Text("Recent Sales", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Container(content=sales_list, height=200, padding=10, border=ft.border.all(1, ft.colors.GREY_300), border_radius=10),
            ft.Text("Top Products", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Container(content=top_products_list, height=200, padding=10, border=ft.border.all(1, ft.colors.GREY_300), border_radius=10)
        ], spacing=20)

        return ft.Container(
            content=dashboard_content,
            padding=30,
            bgcolor=ft.colors.WHITE,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

    def logout():
        nonlocal current_user, current_role
        current_user = None
        current_role = None
        requests.post("http://localhost:5000/api/logout")
        navigate(0)

    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.DASHBOARD, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.icons.STORE, label="Products"),
            ft.NavigationRailDestination(icon=ft.icons.RECEIPT, label="Sales"),
            ft.NavigationRailDestination(icon=ft.icons.PERSON, label="Customers"),
            ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="Settings"),
        ],
        on_change=lambda e: navigate(e.control.selected_index),
    )

    page.add(
        ft.Row([
            sidebar,
            build_login_view(page, on_login=on_login, language=current_language)[0]
        ], expand=True)
    )

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory and event.src_path.endswith('.py'):
            print(f"Change detected in {event.src_path}. Reloading Flet app...")

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
