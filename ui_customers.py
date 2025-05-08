import flet as ft
import requests

def build_customers_view(page, language="en", show_back=False, go_back=None):
    texts = {
        "en": {
            "title": "Customers",
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "add_customer": "Add Customer",
            "success": "Customer created successfully!",
            "error": "Error creating customer",
            "fetch_error": "Error fetching customers",
            "no_customers": "No customers available",
            "search": "Search Customers",
            "confirm_add": "Are you sure you want to add this customer?",
            "name_hint": "Enter customer name (min 3 characters)",
            "email_hint": "Enter email (optional)",
            "phone_hint": "Enter phone number (optional)"
        },
        "fr": {
            "title": "Clients",
            "name": "Nom",
            "email": "Email",
            "phone": "Téléphone",
            "add_customer": "Ajouter un client",
            "success": "Client créé avec succès !",
            "error": "Erreur lors de la création du client",
            "fetch_error": "Erreur lors de la récupération des clients",
            "no_customers": "Aucun client disponible",
            "search": "Rechercher des clients",
            "confirm_add": "Êtes-vous sûr de vouloir ajouter ce client ?",
            "name_hint": "Entrez le nom du client (min 3 caractères)",
            "email_hint": "Entrez l'email (facultatif)",
            "phone_hint": "Entrez le numéro de téléphone (facultatif)"
        },
        "es": {
            "title": "Clientes",
            "name": "Nombre",
            "email": "Correo",
            "phone": "Teléfono",
            "add_customer": "Agregar cliente",
            "success": "¡Cliente creado con éxito!",
            "error": "Error al crear el cliente",
            "fetch_error": "Error al obtener los clientes",
            "no_customers": "No hay clientes disponibles",
            "search": "Buscar clientes",
            "confirm_add": "¿Estás seguro de que deseas agregar este cliente?",
            "name_hint": "Ingresa el nombre del cliente (mín. 3 caracteres)",
            "email_hint": "Ingresa el correo (opcional)",
            "phone_hint": "Ingresa el número de teléfono (opcional)"
        }
    }
    lang = texts[language]

    customers_list = ft.ListView(expand=True, spacing=10)
    feedback = ft.Text("", color=ft.colors.RED)
    loading = ft.ProgressRing(visible=False)
    search_field = ft.TextField(
        label=lang["search"],
        width=250,
        border_color=ft.colors.BLUE,
        on_change=lambda e: populate_customers()
    )

    # Input fields
    name_field = ft.TextField(
        label=lang["name"],
        width=250,
        border_color=ft.colors.BLUE,
        tooltip=lang["name_hint"],
        on_change=lambda e: validate_inputs()
    )
    email_field = ft.TextField(
        label=lang["email"],
        width=250,
        border_color=ft.colors.BLUE,
        tooltip=lang["email_hint"]
    )
    phone_field = ft.TextField(
        label=lang["phone"],
        width=250,
        border_color=ft.colors.BLUE,
        tooltip=lang["phone_hint"]
    )

    def validate_inputs():
        if len(name_field.value.strip()) < 3:
            name_field.error_text = "Name must be at least 3 characters"
        else:
            name_field.error_text = None
        name_field.update()

    def fetch_customers():
        try:
            response = requests.get("http://localhost:5000/api/customers")
            if response.status_code == 200:
                return response.json().get("customers", [])
        except Exception as e:
            print(f"Fetch customers error: {str(e)}")
            return []

    def populate_customers():
        customers_list.controls.clear()
        loading.visible = True
        loading.update()
        customers = fetch_customers()
        search_term = search_field.value.lower()
        if search_term:
            customers = [c for c in customers if search_term in c['name'].lower() or (c.get('email') and search_term in c['email'].lower())]
        if not customers:
            customers_list.controls.append(ft.Text(lang["no_customers"], size=16, text_align="center"))
        else:
            for customer in customers:
                customers_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.PERSON),
                            title=ft.Text(customer['name'], size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Email: {customer.get('email', 'N/A')} | Phone: {customer.get('phone', 'N/A')}", size=14),
                            content_padding=ft.padding.only(left=10, right=10),
                        ),
                        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
                        border_radius=5,
                        padding=5
                    )
                )
        loading.visible = False
        customers_list.update()
        loading.update()

    def create_customer(e):
        try:
            if not name_field.value:
                feedback.value = "Please fill the name field"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            if name_field.error_text:
                feedback.value = "Please fix the errors in the form"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            def confirm_add(e):
                if e.control.text == "Yes":
                    try:
                        response = requests.post(
                            "http://localhost:5000/api/customers",
                            json={
                                "name": name_field.value,
                                "email": email_field.value,
                                "phone": phone_field.value
                            }
                        )
                        if response.status_code == 201:
                            feedback.value = lang["success"]
                            feedback.color = ft.colors.GREEN
                            populate_customers()
                        else:
                            feedback.value = lang["error"]
                            feedback.color = ft.colors.RED
                    except Exception as e:
                        feedback.value = lang["error"]
                        feedback.color = ft.colors.RED
                page.dialog = None
                page.update()

            page.dialog = ft.AlertDialog(
                title=ft.Text(lang["confirm_add"]),
                actions=[
                    ft.ElevatedButton(text="Yes", on_click=confirm_add),
                    ft.ElevatedButton(text="No", on_click=confirm_add)
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.update()

        except Exception as e:
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
            feedback.update()

    bgcolor = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800

    container = ft.Container(
        content=ft.Column([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda e: go_back(),
                tooltip="Back",
                visible=show_back
            ),
            ft.Text(lang["title"], size=24, weight=ft.FontWeight.BOLD, text_align="center"),
            search_field,
            name_field,
            email_field,
            phone_field,
            ft.ElevatedButton(
                text=lang["add_customer"],
                width=250,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
                on_click=create_customer
            ),
            loading,
            feedback,
            ft.Container(
                content=customers_list,
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, scroll=ft.ScrollMode.AUTO),
        padding=20,
        bgcolor=bgcolor,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_900)
    )

    return container, populate_customers

def build_customers_view_unauthorized(page, language="en", show_back=False, go_back=None):
    texts = {
        "en": {
            "title": "Customers",
            "no_customers": "No customers available",
            "search": "Search Customers"
        },
        "fr": {
            "title": "Clients",
            "no_customers": "Aucun client disponible",
            "search": "Rechercher des clients"
        },
        "es": {
            "title": "Clientes",
            "no_customers": "No hay clientes disponibles",
            "search": "Buscar clientes"
        }
    }
    lang = texts[language]

    customers_list = ft.ListView(expand=True, spacing=10)
    loading = ft.ProgressRing(visible=False)
    search_field = ft.TextField(
        label=lang["search"],
        width=250,
        border_color=ft.colors.BLUE,
        on_change=lambda e: populate_customers()
    )

    def fetch_customers():
        try:
            response = requests.get("http://localhost:5000/api/customers")
            if response.status_code == 200:
                return response.json().get("customers", [])
        except Exception as e:
            print(f"Fetch customers error: {str(e)}")
            return []

    def populate_customers():
        customers_list.controls.clear()
        loading.visible = True
        loading.update()
        customers = fetch_customers()
        search_term = search_field.value.lower()
        if search_term:
            customers = [c for c in customers if search_term in c['name'].lower() or (c.get('email') and search_term in c['email'].lower())]
        if not customers:
            customers_list.controls.append(ft.Text(lang["no_customers"], size=16, text_align="center"))
        else:
            for customer in customers:
                customers_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.PERSON),
                            title=ft.Text(customer['name'], size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Email: {customer.get('email', 'N/A')} | Phone: {customer.get('phone', 'N/A')}", size=14),
                            content_padding=ft.padding.only(left=10, right=10),
                        ),
                        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
                        border_radius=5,
                        padding=5
                    )
                )
        loading.visible = False
        customers_list.update()
        loading.update()

    bgcolor = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800

    container = ft.Container(
        content=ft.Column([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda e: go_back(),
                tooltip="Back",
                visible=show_back
            ),
            ft.Text(lang["title"], size=24, weight=ft.FontWeight.BOLD, text_align="center"),
            search_field,
            loading,
            ft.Container(
                content=customers_list,
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, scroll=ft.ScrollMode.AUTO),
        padding=20,
        bgcolor=bgcolor,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_900)
    )

    return container, populate_customers
