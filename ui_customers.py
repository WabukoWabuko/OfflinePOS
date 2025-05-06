import flet as ft
import requests

def build_customers_view(page, language="en", show_back=False, go_back=None):
    # Localization
    texts = {
        "en": {
            "title": "Customer Management",
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "add": "Add Customer",
            "update": "Update",
            "delete": "Delete",
            "success": "Success!",
            "error": "Error: Cannot connect to server!"
        },
        "fr": {
            "title": "Gestion des clients",
            "name": "Nom",
            "email": "Email",
            "phone": "Téléphone",
            "add": "Ajouter un client",
            "update": "Mettre à jour",
            "delete": "Supprimer",
            "success": "Succès !",
            "error": "Erreur : Impossible de se connecter au serveur !"
        }
    }
    lang = texts[language]

    # State
    feedback = ft.Text("", color=ft.colors.RED)
    customers = ft.Ref[ft.Column]()

    # Input fields
    name_field = ft.TextField(label=lang["name"], width=200)
    email_field = ft.TextField(label=lang["email"], width=200)
    phone_field = ft.TextField(label=lang["phone"], width=200)

    def fetch_customers():
        try:
            response = requests.get("http://offlinepos:5000/api/customers")
            if response.status_code == 200:
                data = response.json()
                customers.current.controls = [
                    ft.Row([
                        ft.Text(f"{c['name']} - {c['email']} - {c['phone']}"),
                        ft.ElevatedButton(
                            lang["update"],
                            on_click=lambda e, cid=c['id']: update_customer(cid),
                            bgcolor=ft.colors.BLUE,
                            color=ft.colors.WHITE
                        ),
                        ft.ElevatedButton(
                            lang["delete"],
                            on_click=lambda e, cid=c['id']: delete_customer(cid),
                            bgcolor=ft.colors.RED,
                            color=ft.colors.WHITE
                        )
                    ]) for c in data['customers']
                ]
            else:
                feedback.value = lang["error"]
                feedback.color = ft.colors.RED
        except Exception as e:
            print(f"Fetch customers error: {str(e)}")
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED

    def add_customer(e):
        try:
            response = requests.post("http://offlinepos:5000/api/customers", json={
                "name": name_field.value,
                "email": email_field.value,
                "phone": phone_field.value
            })
            if response.status_code == 201:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                fetch_customers()
            else:
                feedback.value = "Failed to add customer"
                feedback.color = ft.colors.RED
        except Exception as e:
            print(f"Add customer error: {str(e)}")
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
        feedback.update()

    def update_customer(customer_id):
        try:
            response = requests.put(f"http://offlinepos:5000/api/customers/{customer_id}", json={
                "name": name_field.value,
                "email": email_field.value,
                "phone": phone_field.value
            })
            if response.status_code == 200:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                fetch_customers()
            else:
                feedback.value = "Failed to update customer"
                feedback.color = ft.colors.RED
        except Exception as e:
            print(f"Update customer error: {str(e)}")
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
        feedback.update()

    def delete_customer(customer_id):
        try:
            response = requests.delete(f"http://offlinepos:5000/api/customers/{customer_id}")
            if response.status_code == 200:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                fetch_customers()
            else:
                feedback.value = "Failed to delete customer"
                feedback.color = ft.colors.RED
        except Exception as e:
            print(f"Delete customer error: {str(e)}")
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
        feedback.update()

    # Back button
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=lambda e: go_back(),
        tooltip="Back",
        visible=show_back
    )

    # Build the container first, then fetch customers
    container = ft.Container(
        content=ft.Column([
            back_button,
            ft.Text(lang["title"], size=20, weight=ft.FontWeight.BOLD),
            ft.Row([
                name_field,
                email_field,
                phone_field,
                ft.ElevatedButton(lang["add"], on_click=add_customer, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Column(ref=customers),
            feedback
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100)
    )

    # Fetch customers after the container is built
    fetch_customers()

    return container
