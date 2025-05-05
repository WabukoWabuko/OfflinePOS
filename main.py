import flet as ft
import requests

def main(page: ft.Page):
    page.title = "OfflinePOS - Login"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.GREY_100

    # State with proper Value initialization
    is_online = ft.Value(False)
    login_feedback = ft.Text("", color=ft.colors.RED)

    def check_internet():
        try:
            requests.get("https://www.google.com", timeout=5)
            is_online.value = True
            status_text.value = "Online"
            status_text.color = ft.colors.GREEN
        except requests.RequestException:
            is_online.value = False
            status_text.value = "Offline"
            status_text.color = ft.colors.RED
        status_text.update()

    # Status Indicator
    status_text = ft.Text("Checking...", color=ft.colors.BLUE)
    ft.Timer(2, check_internet)  # Check every 2 seconds
    ft.Timer(2, lambda: check_internet(), True)  # Initial check

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

    # Login button
    def login_click(e):
        if not username_field.value or not password_field.value:
            login_feedback.value = "Please fill all fields"
            login_feedback.update()
            return
        login_feedback.value = "Logging in..."
        login_feedback.update()
        # Simulate API call
        try:
            response = requests.post("http://localhost:5000/api/login", json={
                "username": username_field.value,
                "password": password_field.value
            })
            if response.status_code == 200:
                login_feedback.value = "Login successful!"
                login_feedback.color = ft.colors.GREEN
            else:
                login_feedback.value = "Login failed!"
                login_feedback.color = ft.colors.RED
        except Exception as e:
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

    # Layout
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    logo,
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    status_text,
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    username_field,
                    password_field,
                    login_button,
                    login_feedback
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
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
    )

if __name__ == "__main__":
    ft.app(target=main, host="0.0.0.0", port=8000)
