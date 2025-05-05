import flet as ft

def build_settings_view(page, theme_mode, language, on_language_change):
    # Localization
    texts = {
        "en": {
            "title": "Settings",
            "theme": "Theme",
            "language": "Language",
            "light": "Light",
            "dark": "Dark"
        },
        "fr": {
            "title": "Paramètres",
            "theme": "Thème",
            "language": "Langue",
            "light": "Clair",
            "dark": "Sombre"
        }
    }
    lang = texts[language]

    def toggle_theme(e):
        theme_mode.current = ft.ThemeMode.DARK if theme_mode.current == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.theme_mode = theme_mode.current
        page.bgcolor = ft.colors.GREY_100 if theme_mode.current == ft.ThemeMode.LIGHT else ft.colors.GREY_900
        page.update()

    def change_language(e):
        on_language_change(language_dropdown.value)

    theme_switch = ft.Switch(
        label=f"{lang['theme']}: {lang['light'] if theme_mode.current == ft.ThemeMode.LIGHT else lang['dark']}",
        value=theme_mode.current == ft.ThemeMode.DARK,
        on_change=toggle_theme
    )

    language_dropdown = ft.Dropdown(
        label=lang["language"],
        options=[
            ft.dropdown.Option("en", "English"),
            ft.dropdown.Option("fr", "Français")
        ],
        value=language,
        on_change=change_language,
        width=200
    )

    return ft.Container(
        content=ft.Column([
            ft.Text(lang["title"], size=20, weight=ft.FontWeight.BOLD),
            theme_switch,
            language_dropdown
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=ft.colors.WHITE if theme_mode.current == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100)
    )
