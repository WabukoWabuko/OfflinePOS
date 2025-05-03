import flet as ft

def main(page: ft.Page):
    page.title = "OfflinePOS - Login"
    page.window_width = 400
    page.window_height = 500
    page.window_resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT

    # Center the content
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Logo (placeholder text for now)
    logo = ft.Text("OfflinePOS", size=30, weight=ft.FontWeight.BOLD)

    # Input fields
    username_field = ft.TextField(label="Username", width=250)
    password_field = ft.TextField(label="Password", password=True, width=250)

    # Login button
    login_button = ft.ElevatedButton(
        text="Login",
        width=250,
        on_click=lambda e: page.add(ft.Text("Login clicked!"))  # Placeholder action
    )

    # Online/offline status (placeholder)
    status = ft.Text("Online", color=ft.colors.GREEN)

    # Layout
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    logo,
                    ft.Divider(),
                    username_field,
                    password_field,
                    login_button,
                    ft.Divider(),
                    status
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
    )

if __name__ == "__main__":
    ft.app(target=main)
