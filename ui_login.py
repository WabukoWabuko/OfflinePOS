import flet as ft
import requests
import asyncio

def build_login_view(page, on_login, language="en", show_back=False, go_back=None):
    # Localization
    texts = {
        "en": {
            "title": "OfflinePOS",
            "username": "Username",
            "password": "Password",
            "login": "Login",
            "logging_in": "Logging in...",
            "fill_fields": "Please fill all fields",
            "success": "Login successful!",
            "failed": "Login failed!",
            "error": "Error: Cannot connect to server!",
            "already_logged_in": "Already logged in, redirecting..."
        },
        "fr": {
            "title": "OfflinePOS",
            "username": "Nom d'utilisateur",
            "password": "Mot de passe",
            "login": "Connexion",
            "logging_in": "Connexion en cours...",
            "fill_fields": "Veuillez remplir tous les champs",
            "success": "Connexion réussie !",
            "failed": "Échec de la connexion !",
            "error": "Erreur : Impossible de se connecter au serveur !",
            "already_logged_in": "Déjà connecté, redirection en cours..."
        }
    }
    lang = texts[language]

    # Local state
    login_feedback = ft.Text("", color=ft.colors.RED)
    status_text = ft.Text("Checking...", color=ft.colors.BLUE)

    # Add controls to page initially
    main_container = ft.Container(
        content=ft.Column(
            [
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: go_back(),
                    tooltip="Back",
                    visible=show_back
                ),
                ft.Text(lang["title"], size=40, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                status_text,
                ft.TextField(
                    label=lang["username"],
                    width=300,
                    border_color=ft.colors.BLUE,
                    focused_border_color=ft.colors.BLUE_700,
                    cursor_color=ft.colors.BLUE
                ),
                ft.TextField(
                    label=lang["password"],
                    password=True,
                    width=300,
                    border_color=ft.colors.BLUE,
                    focused_border_color=ft.colors.BLUE_700,
                    cursor_color=ft.colors.BLUE
                ),
                ft.ElevatedButton(
                    text=lang["login"],
                    width=300,
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                    on_click=lambda e: login_click(e, page, on_login, login_feedback)
                ),
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

    # Async internet check
    async def monitor_connection():
        try:
            response = requests.get("https://www.google.com", timeout=3)
            status_text.value = "Online"
            status_text.color = ft.colors.GREEN
        except requests.RequestException:
            status_text.value = "Offline"
            status_text.color = ft.colors.RED
        status_text.update()
        await asyncio.sleep(5)

    # Check session
    def check_session():
        try:
            response = requests.get("http://offlinepos:5000/api/check-session")
            if response.status_code == 200 and response.json().get("user_id"):
                login_feedback.value = lang["already_logged_in"]
                login_feedback.color = ft.colors.BLUE
                login_feedback.update()
                page.go("/dashboard")
        except Exception:
            pass

    # Login button logic
    async def login_click(e, page, on_login, login_feedback):
        username_field = page.controls[0].content.controls[3]  # TextField for username
        password_field = page.controls[0].content.controls[4]  # TextField for password

        if not username_field.value or not password_field.value:
            login_feedback.value = lang["fill_fields"]
            login_feedback.color = ft.colors.RED
            login_feedback.update()
            return

        login_feedback.value = lang["logging_in"]
        login_feedback.color = ft.colors.BLUE
        login_feedback.update()

        retries = 3
        for attempt in range(retries):
            try:
                response = requests.post(
                    "http://offlinepos:5000/api/login",
                    json={
                        "username": username_field.value,
                        "password": password_field.value
                    },
                    timeout=5
                )
                if response.status_code == 200:
                    login_feedback.value = lang["success"]
                    login_feedback.color = ft.colors.GREEN
                    data = response.json()
                    on_login(data["user_id"], data["role"])
                else:
                    login_feedback.value = lang["failed"]
                    login_feedback.color = ft.colors.RED
                break
            except requests.exceptions.ConnectionError as ce:
                print(f"Connection error on attempt {attempt + 1}: {str(ce)}")
                if attempt == retries - 1:
                    login_feedback.value = lang["error"]
                    login_feedback.color = ft.colors.RED
                else:
                    await asyncio.sleep(2)
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                login_feedback.value = f"Error: {str(e)}"
                login_feedback.color = ft.colors.RED
                break
        login_feedback.update()

    # Start the async connection monitor and check session
    check_session()
    page.run_task(monitor_connection)

    return main_container
