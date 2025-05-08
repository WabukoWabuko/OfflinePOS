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
            "no_customers": "No customers available"
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
            "no_customers": "Aucun client disponible"
        }
    }
    lang = texts[language]

    customers_list = ft.ListView(expand=True, spacing=10)
    feedback = ft.Text("", color=ft.colors.RED)

    def fetch_customers():
        try:
            response = requests.get("[invalid url, do not cite])
            if response.status_code == 200:
                return response.json().get("customers", [])
        except Exception as e:
            print(f"Fetch customers error: {str(e)}")
            return []

    def populate_customers():
        customers_list.controls.clear()
        customers = fetch_customers()
        if not customers:
            customers_list.controls.append(ft.Text(lang["no_customers"]))
        else:
            for customer in customers:
                customers_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(f"{customer['name']}"),
                        subtitle=ft.Text(f"Email: {customer.get('email', 'N/A')}, Phone: {customer.get('phone', 'N/A')}")
                    )
                )
        customers_list.update()

    def create_customer(e):
        try:
            name_field = page.controls[0].content.controls[2]  # Name field
            email_field = page.controls[0].content.controls[3]  # Email field
            phone_field = page.controls[0].content.controls[4]  # Phone field

            if not name_field.value:
                feedback.value = "Please fill the name field"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            response = requests.post(
                "[invalid url, do not cite],
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
            feedback.update()
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
            ft.Text(lang["title"], size=20, weight=ft.FontWeight.BOLD),
            ft.TextField(
                label=lang["name"],
                width=200,
                border_color=ft.colors.BLUE,
                focused_border_color=ft.colors.BLUE_700,
                cursor_color=ft.colors.BLUE
            ),
            ft.TextField(
                label=lang["email"],
                width=200,
                border_color=ft.colors.BLUE,
                focused_border_color=ft.colors.BLUE_700,
                cursor_color=ft.colors.BLUE
            ),
            ft.TextField(
                label=lang["phone"],
                width=200,
                border_color=ft.colors.BLUE,
                focused_border_color=ft.colors.BLUE_700,
                cursor_color=ft.colors.BLUE
            ),
            ft.ElevatedButton(
                text=lang["add_customer"],
                width=200,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
                on_click=create_customer
            ),
            feedback,
            customers_list
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=bgcolor,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.colors.BLUE_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_900
        )
    )

    return container, populate_customers
