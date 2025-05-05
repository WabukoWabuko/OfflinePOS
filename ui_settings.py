import flet as ft

def build_settings_view(page, theme_mode, current_theme, language, on_language_change, on_theme_change, show_back=False, go_back=None):
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
        new_theme = ft.ThemeMode.DARK if current_theme == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        on_theme_change(new_theme)
        theme_switch.label = f"{lang['theme']}: {lang['light'] if current_theme == ft.ThemeMode.LIGHT else lang['dark']}"
        theme_switch.update()

    theme_switch = ft.Switch(
        label=f"{lang['theme']}: {lang['light'] if current_theme == ft.ThemeMode.LIGHT else lang['dark']}",
        value=current_theme == ft.ThemeMode.DARK,
        on_change=toggle_theme
    )

    language_dropdown = ft.Dropdown(
        label=lang["language"],
        options=[
            ft.dropdown.Option("en", "English"),
            ft.dropdown.Option("fr", "Français")
        ],
        value=language,
        on_change=lambda e: on_language_change(language_dropdown.value),
        width=200
    )

    # Back button
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=lambda e: go_back(),
        tooltip="Back",
        visible=show_back
    )

    return ft.Container(
        content=ft.Column([
            back_button,
            ft.Text(lang["title"], size=20, weight=ft.FontWeight.BOLD),
            theme_switch,
            language_dropdown
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=ft.colors.WHITE if current_theme == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100)
    )
