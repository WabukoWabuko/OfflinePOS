import sys
import flet as ft
from ui_login import build_login_view
from ui_products import build_products_view
from ui_sales import build_sales_view
from ui_settings import build_settings_view

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
    current_language = "en"  # Default to English
    current_theme = ft.ThemeMode.LIGHT  # Separate theme state
    theme_mode = ft.Ref()  # Reference for UI updates
    nav_history = [0]  # Track navigation history (indices of nav_bar)

    # Navigation handler
    def navigate(e):
        if e is not None:  # If triggered by user clicking nav_bar
            new_index = nav_bar.selected_index
            if new_index != nav_history[-1]:  # Avoid duplicates
                nav_history.append(new_index)
        page.controls.clear()
        current_index = nav_history[-1]
        nav_bar.selected_index = current_index  # Sync nav_bar with history
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
        page.update()

    def go_back():
        if len(nav_history) > 1:  # Ensure there's a previous page
            nav_history.pop()  # Remove current page
            navigate(None)  # Navigate to previous page

    def on_login(user_id, role):
        nonlocal current_user, current_role
        current_user = user_id
        current_role = role
        nav_history.append(0)  # Reset to dashboard after login
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

    def build_dashboard_view(go_back):
        return ft.Container(
            content=ft.Column([
                ft.Text("Dashboard - Coming Soon", size=20),
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: go_back(),
                    tooltip="Back",
                    visible=len(nav_history) > 1
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.colors.WHITE if current_theme == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
            border_radius=15,
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100)
        )

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
            build_login_view(page, on_login=on_login, language=current_language, show_back=len(nav_history) > 1, go_back=go_back)
        ])
    )

if __name__ == "__main__":
    ft.app(target=main, host="0.0.0.0", port=8000)
