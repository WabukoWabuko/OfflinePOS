import flet as ft
import requests

def build_customers_view(page, language="en"):
    texts = {
        "en": {
            "title": "Customers",
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "add_customer": "Add Customer",
            "success": "Customer created successfully!",
            "error": "Error creating customer",
            "no_customers": "No customers available",
            "search": "Search Customers",
            "confirm_add": "Are you sure you want to add this customer?",
            "confirm_delete": "Are you sure you want to delete this customer?",
            "edit": "Edit",
            "delete": "Delete",
            "sort_by": "Sort By",
            "name_asc": "Name (A-Z)",
            "name_desc": "Name (Z-A)",
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
            "no_customers": "Aucun client disponible",
            "search": "Rechercher des clients",
            "confirm_add": "Êtes-vous sûr de vouloir ajouter ce client ?",
            "confirm_delete": "Êtes-vous sûr de vouloir supprimer ce client ?",
            "edit": "Modifier",
            "delete": "Supprimer",
            "sort_by": "Trier par",
            "name_asc": "Nom (A-Z)",
            "name_desc": "Nom (Z-A)",
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
            "no_customers": "No hay clientes disponibles",
            "search": "Buscar clientes",
            "confirm_add": "¿Estás seguro de que deseas agregar este cliente?",
            "confirm_delete": "¿Estás seguro de que deseas eliminar este cliente?",
            "edit": "Editar",
            "delete": "Eliminar",
            "sort_by": "Ordenar por",
            "name_asc": "Nombre (A-Z)",
            "name_desc": "Nombre (Z-A)",
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
        border_color=ft.colors.BLUE_700,
        on_change=lambda e: populate_customers()
    )
    sort_dropdown = ft.Dropdown(
        label=lang["sort_by"],
        width=200,
        options=[
            ft.dropdown.Option(key="name_asc", text=lang["name_asc"]),
            ft.dropdown.Option(key="name_desc", text=lang["name_desc"])
        ],
        value="name_asc",
        border_color=ft.colors.BLUE_700,
        on_change=lambda e: populate_customers()
    )

    # Input fields
    name_field = ft.TextField(
        label=lang["name"],
        width=250,
        border_color=ft.colors.BLUE_700,
        tooltip=lang["name_hint"],
        on_change=lambda e: validate_inputs()
    )
    email_field = ft.TextField(
        label=lang["email"],
        width=250,
        border_color=ft.colors.BLUE_700,
        tooltip=lang["email_hint"]
    )
    phone_field = ft.TextField(
        label=lang["phone"],
        width=250,
        border_color=ft.colors.BLUE_700,
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
        
        # Sorting
        sort_key = sort_dropdown.value
        if sort_key == "name_asc":
            customers.sort(key=lambda x: x['name'].lower())
        elif sort_key == "name_desc":
            customers.sort(key=lambda x: x['name'].lower(), reverse=True)

        if not customers:
            customers_list.controls.append(ft.Text(lang["no_customers"], size=16, text_align="center"))
        else:
            for customer in customers:
                customer_id = customer['id']
                customers_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.PERSON, color=ft.colors.BLUE_700),
                                title=ft.Text(customer['name'], size=16, weight=ft.FontWeight.BOLD),
                                subtitle=ft.Text(f"Email: {customer.get('email', 'N/A')} | Phone: {customer.get('phone', 'N/A')}", size=14),
                                content_padding=ft.padding.only(left=10, right=10),
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip=lang["edit"],
                                icon_color=ft.colors.BLUE_700,
                                on_click=lambda e, cid=customer_id: edit_customer(cid)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip=lang["delete"],
                                icon_color=ft.colors.RED_600,
                                on_click=lambda e, cid=customer_id: delete_customer(cid)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=ft.colors.WHITE,
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
                            clear_fields()
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

    def edit_customer(customer_id):
        # Placeholder for edit functionality
        feedback.value = f"Edit customer {customer_id} (not implemented)"
        feedback.color = ft.colors.BLUE
        feedback.update()

    def delete_customer(customer_id):
        def confirm_delete(e):
            if e.control.text == "Yes":
                try:
                    response = requests.delete(f"http://localhost:5000/api/customers/{customer_id}")
                    if response.status_code == 204:
                        feedback.value = "Customer deleted successfully!"
                        feedback.color = ft.colors.GREEN
                        populate_customers()
                    else:
                        feedback.value = "Error deleting customer"
                        feedback.color = ft.colors.RED
                except Exception as e:
                    feedback.value = "Error deleting customer"
                    feedback.color = ft.colors.RED
            page.dialog = None
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text(lang["confirm_delete"]),
            actions=[
                ft.ElevatedButton(text="Yes", on_click=confirm_delete),
                ft.ElevatedButton(text="No", on_click=confirm_delete)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.update()

    def clear_fields():
        name_field.value = ""
        email_field.value = ""
        phone_field.value = ""
        name_field.error_text = None
        name_field.update()
        email_field.update()
        phone_field.update()

    container = ft.Container(
        content=ft.Column([
            ft.Text(lang["title"], size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Row([
                search_field,
                sort_dropdown
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            name_field,
            email_field,
            phone_field,
            ft.ElevatedButton(
                text=lang["add_customer"],
                width=250,
                bgcolor=ft.colors.BLUE_700,
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=create_customer
            ),
            loading,
            feedback,
            ft.Container(
                content=customers_list,
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                height=300
            )
        ], spacing=20, scroll=ft.ScrollMode.AUTO),
        padding=30,
        bgcolor=ft.colors.WHITE,
        expand=True
    )

    return container, populate_customers

def build_customers_view_unauthorized(page, language="en"):
    texts = {
        "en": {
            "title": "Customers",
            "no_customers": "No customers available",
            "search": "Search Customers",
            "sort_by": "Sort By",
            "name_asc": "Name (A-Z)",
            "name_desc": "Name (Z-A)"
        },
        "fr": {
            "title": "Clients",
            "no_customers": "Aucun client disponible",
            "search": "Rechercher des clients",
            "sort_by": "Trier par",
            "name_asc": "Nom (A-Z)",
            "name_desc": "Nom (Z-A)"
        },
        "es": {
            "title": "Clientes",
            "no_customers": "No hay clientes disponibles",
            "search": "Buscar clientes",
            "sort_by": "Ordenar por",
            "name_asc": "Nombre (A-Z)",
            "name_desc": "Nombre (Z-A)"
        }
    }
    lang = texts[language]

    customers_list = ft.ListView(expand=True, spacing=10)
    loading = ft.ProgressRing(visible=False)
    search_field = ft.TextField(
        label=lang["search"],
        width=250,
        border_color=ft.colors.BLUE_700,
        on_change=lambda e: populate_customers()
    )
    sort_dropdown = ft.Dropdown(
        label=lang["sort_by"],
        width=200,
        options=[
            ft.dropdown.Option(key="name_asc", text=lang["name_asc"]),
            ft.dropdown.Option(key="name_desc", text=lang["name_desc"])
        ],
        value="name_asc",
        border_color=ft.colors.BLUE_700,
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
        
        # Sorting
        sort_key = sort_dropdown.value
        if sort_key == "name_asc":
            customers.sort(key=lambda x: x['name'].lower())
        elif sort_key == "name_desc":
            customers.sort(key=lambda x: x['name'].lower(), reverse=True)

        if not customers:
            customers_list.controls.append(ft.Text(lang["no_customers"], size=16, text_align="center"))
        else:
            for customer in customers:
                customers_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.PERSON, color=ft.colors.BLUE_700),
                            title=ft.Text(customer['name'], size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Email: {customer.get('email', 'N/A')} | Phone: {customer.get('phone', 'N/A')}", size=14),
                            content_padding=ft.padding.only(left=10, right=10),
                        ),
                        bgcolor=ft.colors.WHITE,
                        border_radius=5,
                        padding=5
                    )
                )
        loading.visible = False
        customers_list.update()
        loading.update()

    container = ft.Container(
        content=ft.Column([
            ft.Text(lang["title"], size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Row([
                search_field,
                sort_dropdown
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            loading,
            ft.Container(
                content=customers_list,
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                height=350
            )
        ], spacing=20, scroll=ft.ScrollMode.AUTO),
        padding=30,
        bgcolor=ft.colors.WHITE,
        expand=True
    )

    return container, populate_customers
