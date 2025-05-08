import flet as ft

def build_settings_view(page, theme_mode, current_theme, language="en", on_language_change=None, on_theme_change=None, show_back=False, go_back=None):
    texts = {
        "en": {
            "title": "Settings",
            "theme": "Theme",
            "light": "Light",
            "dark": "Dark",
            "language": "Language",
            "english": "English",
            "french": "French"
        },
        "fr": {
            "title": "Paramètres",
            "theme": "Thème",
            "light": "Clair",
            "dark": "Sombre",
            "language": "Langue",
            "english": "Anglais",
            "french": "Français"
        }
    }
    lang = texts[language]

    def update_theme(e):
        new_theme = ft.ThemeMode.LIGHT if theme_dropdown.value == lang["light"] else ft.ThemeMode.DARK
        on_theme_change(new_theme)

    def update_language(e):
        new_lang = "en" if language_dropdown.value == lang["english"] else "fr"
        on_language_change(new_lang)

    theme_dropdown = ft.Dropdown(
        label=lang["theme"],
        width=200,
        options=[
            ft.dropdown.Option(lang["light"]),
            ft.dropdown.Option(lang["dark"])
        ],
        value=lang["light"] if current_theme == ft.ThemeMode.LIGHT else lang["dark"],
        on_change=update_theme,
        border_color=ft.colors.BLUE,
        focused_border_color=ft.colors.BLUE_700
    )

    language_dropdown = ft.Dropdown(
        label=lang["language"],
        width=200,
        options=[
            ft.dropdown.Option(lang["english"]),
            ft.dropdown.Option(lang["french"])
        ],
        value=lang["english"] if language == "en" else lang["french"],
        on_change=update_language,
        border_color=ft.colors.BLUE,
        focused_border_color=ft.colors.BLUE_700
    )

    return ft.Container(
        content=ft.Column([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda e: go_back(),
                tooltip="Back",
                visible=show_back
            ),
            ft.Text(lang["title"], size=20, weight=ft.FontWeight.BOLD),
            theme_dropdown,
            language_dropdown
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100)
    )
