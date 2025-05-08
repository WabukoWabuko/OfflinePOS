import flet as ft

def build_settings_view(page, theme_mode, current_theme, language, on_language_change, on_theme_change, show_back=False, go_back=None):
    texts = {
        "en": {
            "title": "Settings",
            "theme": "Theme",
            "light": "Light",
            "dark": "Dark",
            "language": "Language",
            "english": "English",
            "french": "French",
            "spanish": "Spanish"
        },
        "fr": {
            "title": "Paramètres",
            "theme": "Thème",
            "light": "Clair",
            "dark": "Sombre",
            "language": "Langue",
            "english": "Anglais",
            "french": "Français",
            "spanish": "Espagnol"
        },
        "es": {
            "title": "Configuración",
            "theme": "Tema",
            "light": "Claro",
            "dark": "Oscuro",
            "language": "Idioma",
            "english": "Inglés",
            "french": "Francés",
            "spanish": "Español"
        }
    }
    lang = texts[language]

    theme_dropdown = ft.Dropdown(
        label=lang["theme"],
        width=200,
        options=[
            ft.dropdown.Option(text=lang["light"], key="light"),
            ft.dropdown.Option(text=lang["dark"], key="dark")
        ],
        value="light" if current_theme == ft.ThemeMode.LIGHT else "dark",
        border_color=ft.colors.BLUE,
        on_change=lambda e: on_theme_change(ft.ThemeMode.LIGHT if e.control.value == "light" else ft.ThemeMode.DARK)
    )

    language_dropdown = ft.Dropdown(
        label=lang["language"],
        width=200,
        options=[
            ft.dropdown.Option(text=lang["english"], key="en"),
            ft.dropdown.Option(text=lang["french"], key="fr"),
            ft.dropdown.Option(text=lang["spanish"], key="es")
        ],
        value=language,
        border_color=ft.colors.BLUE,
        on_change=lambda e: on_language_change(e.control.value)
    )

    bgcolor = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800

    return ft.Container(
        content=ft.Column([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda e: go_back(),
                tooltip="Back",
                visible=show_back
            ),
            ft.Text(lang["title"], size=24, weight=ft.FontWeight.BOLD, text_align="center"),
            theme_dropdown,
            language_dropdown
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, scroll=ft.ScrollMode.AUTO),
        padding=20,
        bgcolor=bgcolor,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_900),
        animate_opacity=500  # Smooth transition for theme change
    )
