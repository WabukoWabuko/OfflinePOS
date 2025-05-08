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
            "failed": "Login failed! Check credentials",
            "error": "Error: Cannot connect to server!",
            "already_logged_in": "Already logged in, redirecting...",
            "remember_me": "Remember Me",
            "username_hint": "Enter your username (e.g., admin)",
            "password_hint": "Enter your password (min 8 characters)"
        },
        "fr": {
            "title": "OfflinePOS",
            "username": "Nom d'utilisateur",
            "password": "Mot de passe",
            "login": "Connexion",
            "logging_in": "Connexion en cours...",
            "fill_fields": "Veuillez remplir tous les champs",
            "success": "Connexion réussie !",
            "failed": "Échec de la connexion ! Vérifiez vos identifiants",
            "error": "Erreur : Impossible de se connecter au serveur !",
            "already_logged_in": "Déjà connecté, redirection en cours...",
            "remember_me": "Se souvenir de moi",
            "username_hint": "Entrez votre nom d'utilisateur (ex. admin)",
            "password_hint": "Entrez votre mot de passe (min 8 caractères)"
        },
        "es": {
            "title": "OfflinePOS",
            "username": "Nombre de usuario",
            "password": "Contraseña",
            "login": "Iniciar sesión",
            "logging_in": "Iniciando sesión...",
            "fill_fields": "Por favor completa todos los campos",
            "success": "¡Inicio de sesión exitoso!",
            "failed": "¡Fallo en el inicio de sesión! Verifica tus credenciales",
            "error": "Error: ¡No se puede conectar al servidor!",
            "already_logged_in": "Ya estás conectado, redirigiendo...",
            "remember_me": "Recordarme",
            "username_hint": "Ingresa tu nombre de usuario (ej. admin)",
            "password_hint": "Ingresa tu contraseña (mín. 8 caracteres)"
        }
    }
    lang = texts[language]

    # Local state
    login_feedback = ft.Text("", color=ft.colors.RED)
    status_text = ft.Text("Checking...")
    loading = ft.ProgressRing(visible=False)

    # Input fields
    username_field = ft.TextField(
        label=lang["username"],
        width=300,
        border_color=ft.colors.BLUE,
        focused_border_color=ft.colors.BLUE_700,
        cursor_color=ft.colors.BLUE,
        tooltip=lang["username_hint"],
        on_change=lambda e: validate_inputs()
    )
    password_field = ft.TextField(
        label=lang["password"],
        password=True,
        width=300,
        border_color=ft.colors.BLUE,
        focused_border_color=ft.colors.BLUE_700,
        cursor_color=ft.colors.BLUE,
        tooltip=lang["password_hint"],
        on_change=lambda e: validate_inputs()
    )
    remember_me = ft.Checkbox(label=lang["remember_me"], value=False)

    def validate_inputs():
        if len(username_field.value.strip()) < 3:
            username_field.error_text = "Username must be at least 3 characters"
        else:
            username_field.error_text = None
        if len(password_field.value) < 8:
            password_field.error_text = "Password must be at least 8 characters"
        else:
            password_field.error_text = None
        username_field.update()
        password_field.update()

    # Async internet check
    async def monitor_connection():
        while True:
            try:
                requests.get("https://www.google.com", timeout=3)
                if status_text.page:
                    status_text.value = "Online"
                    status_text.color = ft.colors.GREEN
                    status_text.update()
            except requests.RequestException:
                if status_text.page:
                    status_text.value = "Offline"
                    status_text.color = ft.colors.RED
                    status_text.update()
            await asyncio.sleep(5)

    # Check session
    def check_session():
        try:
            response = requests.get("http://localhost:5000/api/check-session")
            if response.status_code == 200 and response.json().get("user_id"):
                login_feedback.value = lang["already_logged_in"]
                login_feedback.color = ft.colors.BLUE
                login_feedback.update()
                page.go("/dashboard")
        except Exception:
            pass

    # Login button logic
    async def login_click(e):
        if not username_field.value or not password_field.value:
            login_feedback.value = lang["fill_fields"]
            login_feedback.color = ft.colors.RED
            login_feedback.update()
            return

        if len(username_field.value.strip()) < 3 or len(password_field.value) < 8:
            login_feedback.value = lang["fill_fields"]
            login_feedback.color = ft.colors.RED
            login_feedback.update()
            return

        loading.visible = True
        login_feedback.value = lang["logging_in"]
        login_feedback.color = ft.colors.BLUE
        login_feedback.update()
        loading.update()

        retries = 3
        for attempt in range(retries):
            try:
                response = requests.post(
                    "http://localhost:5000/api/login",
                    json={
                        "username": username_field.value,
                        "password": password_field.value
                    },
                    timeout=5
                )
                print(f"Login response status: {response.status_code}")
                print(f"Login response body: {response.text}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"Login data: {data}")
                    if "user_id" in data and "role" in data:
                        login_feedback.value = lang["success"]
                        login_feedback.color = ft.colors.GREEN
                        on_login(data["user_id"], data["role"])
                    else:
                        login_feedback.value = lang["failed"]
                        login_feedback.color = ft.colors.RED
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
        loading.visible = False
        login_feedback.update()
        loading.update()

    bgcolor = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800

    main_container = ft.Container(
        content=ft.Column(
            [
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: go_back() if go_back else None,
                    tooltip="Back",
                    visible=show_back
                ),
                ft.Text(lang["title"], size=40, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                status_text,
                username_field,
                password_field,
                remember_me,
                ft.ElevatedButton(
                    text=lang["login"],
                    width=300,
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                    on_click=lambda e: page.run_task(login_click, e)
                ),
                loading,
                login_feedback
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            scroll=ft.ScrollMode.AUTO  # Make the login view scrollable
        ),
        padding=30,
        bgcolor=bgcolor,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.colors.BLUE_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_900
        ),
        width=350
    )

    # Return the container and a function to start monitoring
    def start_monitoring():
        page.run_task(monitor_connection)

    return main_container, start_monitoring
