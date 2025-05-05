import flet as ft
import time
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.utils.network import get_status

def load_translations(lang="en"):
    with open(f"app/frontend/locales/{lang}.json", "r") as f:
        return json.load(f)

def main(page: ft.Page):
    # Load initial language
    lang = "en"
    translations = load_translations(lang)

    page.title = translations["app_name"]
    page.window_width = 400  # Ignored in web mode, but kept for consistency
    page.window_height = 500
    page.window_resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT

    # Center the content
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Logo
    logo = ft.Text(translations["app_name"], size=30, weight=ft.FontWeight.BOLD)

    # Input fields
    username_field = ft.TextField(label=translations["username"], width=250)
    password_field = ft.TextField(label=translations["password"], password=True, width=250)

    # Login button
    login_button = ft.ElevatedButton(
        text=translations["login"],
        width=250,
        on_click=lambda e: page.add(ft.Text("Login clicked!"))
    )

    # Online/offline status
    status_text = ft.Text(
        translations[get_status().lower()],
        color=ft.colors.GREEN if get_status() == "Online" else ft.colors.RED
    )

    # Dark mode toggle
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        container.bgcolor = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK87
        page.update()

    theme_toggle = ft.Switch(label="Dark Mode", on_change=toggle_theme)

    # Language toggle
    def change_language(e):
        nonlocal lang, translations
        lang = "es" if lang == "en" else "en"
        translations = load_translations(lang)
        page.title = translations["app_name"]
        logo.value = translations["app_name"]
        username_field.label = translations["username"]
        password_field.label = translations["password"]
        login_button.text = translations["login"]
        status_text.value = translations[get_status().lower()]
        page.update()

    lang_toggle = ft.Dropdown(
        label="Language",
        width=250,
        options=[
            ft.dropdown.Option("en", "English"),
            ft.dropdown.Option("es", "Español")
        ],
        value="en",
        on_change=change_language
    )

    # Update status periodically
    def update_status():
        while True:
            new_status = get_status()
            status_text.value = translations[new_status.lower()]
            status_text.color = ft.colors.GREEN if new_status == "Online" else ft.colors.RED
            page.update()
            time.sleep(5)

    import threading
    threading.Thread(target=update_status, daemon=True).start()

    # Layout
    container = ft.Container(
        content=ft.Column(
            [
                logo,
                ft.Divider(),
                username_field,
                password_field,
                login_button,
                ft.Divider(),
                status_text,
                theme_toggle,
                lang_toggle
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.colors.BLACK26
        )
    )

    page.add(container)

if __name__ == "__main__":
    ft.app(target=main, host="0.0.0.0", port=8000)
