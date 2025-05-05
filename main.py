import flet as ft
import requests
import asyncio

def main(page: ft.Page):
    print("Starting main function...")
    page.title = "OfflinePOS - Login"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.GREY_100
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Local state
    login_feedback = ft.Text("", color=ft.colors.RED)

    # Status text
    status_text = ft.Text("Checking...", color=ft.colors.BLUE)

    # Async internet check
    async def monitor_connection():
        while True:
            try:
                requests.get("https://www.google.com", timeout=3)
                status_text.value = "Online"
                status_text.color = ft.colors.GREEN
            except requests.RequestException:
                status_text.value = "Offline"
                status_text.color = ft.colors.RED
            status_text.update()
            await asyncio.sleep(5)  # Every 5 seconds

    # Logo
    logo = ft.Text("OfflinePOS", size=40, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)

    # Input fields
    username_field = ft.TextField(
        label="Username",
        width=300,
        border_color=ft.colors.BLUE,
        focused_border_color=ft.colors.BLUE_700,
        cursor_color=ft.colors.BLUE
    )

    password_field = ft.TextField(
        label="Password",
        password=True,
        width=300,
        border_color=ft.colors.BLUE,
        focused_border_color=ft.colors.BLUE_700,
        cursor_color=ft.colors.BLUE
    )

    # Login button logic
    def login_click(e):
        if not username_field.value or not password_field.value:
            login_feedback.value = "Please fill all fields"
            login_feedback.color = ft.colors.RED
            login_feedback.update()
            return

        login_feedback.value = "Logging in..."
        login_feedback.color = ft.colors.BLUE
        login_feedback.update()

        try:
            response = requests.post(
                "http://localhost:5000/api/login",
                json={
                    "username": username_field.value,
                    "password": password_field.value
                },
                timeout=5
            )
            if response.status_code == 200:
                login_feedback.value = "Login successful!"
                login_feedback.color = ft.colors.GREEN
            else:
                login_feedback.value = "Login failed!"
                login_feedback.color = ft.colors.RED
        except Exception:
            login_feedback.value = "Error connecting to server!"
            login_feedback.color = ft.colors.RED
        login_feedback.update()

    login_button = ft.ElevatedButton(
        text="Login",
        width=300,
        bgcolor=ft.colors.BLUE,
        color=ft.colors.WHITE,
        on_click=login_click
    )

    # Layout container
    main_container = ft.Container(
        content=ft.Column(
            [
                logo,
                status_text,
                username_field,
                password_field,
                login_button,
                login_feedback
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=30,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.colors.BLUE_100
        ),
        width=350
    )

    # Add UI to page
    page.add(main_container)

    # Start the async connection monitor
    page.run_task(monitor_connection)

if __name__ == "__main__":
    ft.app(target=main, host="0.0.0.0", port=8000)

