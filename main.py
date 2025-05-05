import flet as ft
from ui_login import build_login_view
from ui_products import build_products_view
from ui_sales import build_sales_view
from ui_settings import build_settings_view

def main(page: ft.Page):
    print("Starting main function...")
    page.title = "OfflinePOS"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.GREY_100

    # State for navigation
    current_user = None
    current_role = None
    current_language = "en"  # Default to English
    theme_mode = ft.Ref[ft.ThemeMode](ft.ThemeMode.LIGHT)

    # Navigation handler
    def navigate(e):
        page.controls.clear()
        if nav_bar.selected_index == 0:
            if not current_user:
                page.controls.append(build_login_view(page, on_login=on_login, language=current_language))
            else:
                page.controls.append(ft.Text("Dashboard - Coming Soon", size=20))
        elif nav_bar.selected_index == 1:
            page.controls.append(build_products_view(page, language=current_language))
        elif nav_bar.selected_index == 2:
            page.controls.append(build_sales_view(page, user_id=current_user, language=current_language))
        elif nav_bar.selected_index == 3:
            page.controls.append(build_settings_view(page, theme_mode=theme_mode, language=current_language, on_language_change=update_language))
        page.update()

    def on_login(user_id, role):
        nonlocal current_user, current_role
        current_user = user_id
        current_role = role
        nav_bar.selected_index = 0
        navigate(None)

    def update_language(lang):
        nonlocal current_language
        current_language = lang
        navigate(None)

    # Navigation bar
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.STORE, label="Products"),
            ft.NavigationDestination(icon=ft.icons.RECEIPT, label="Sales"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
        ],
        on_change=navigate,
        selected_index=0
    )

    # Initial view
    page.add(
        ft.Column([
            nav_bar,
            build_login_view(page, on_login=on_login, language=current_language)
        ])
    )

if __name__ == "__main__":
    ft.app(target=main, host="0.0.0.0", port=8000)
