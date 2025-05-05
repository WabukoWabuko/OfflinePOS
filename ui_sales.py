import flet as ft
import requests

def build_sales_view(page, user_id, language="en"):
    # Localization
    texts = {
        "en": {
            "title": "Sales Tracking",
            "product_id": "Product ID",
            "quantity": "Quantity",
            "unit_price": "Unit Price",
            "payment": "Payment Method",
            "add": "Add Sale",
            "success": "Sale recorded!",
            "error": "Error: Cannot connect to server!"
        },
        "fr": {
            "title": "Suivi des ventes",
            "product_id": "ID du produit",
            "quantity": "Quantité",
            "unit_price": "Prix unitaire",
            "payment": "Méthode de paiement",
            "add": "Ajouter une vente",
            "success": "Vente enregistrée !",
            "error": "Erreur : Impossible de se connecter au serveur !"
        }
    }
    lang = texts[language]

    # State
    feedback = ft.Text("", color=ft.colors.RED)
    sales = ft.Ref[ft.Column]()

    # Input fields
    product_id_field = ft.TextField(label=lang["product_id"], width=100, keyboard_type=ft.KeyboardType.NUMBER)
    quantity_field = ft.TextField(label=lang["quantity"], width=100, keyboard_type=ft.KeyboardType.NUMBER)
    unit_price_field = ft.TextField(label=lang["unit_price"], width=100, keyboard_type=ft.KeyboardType.NUMBER)
    payment_field = ft.Dropdown(label=lang["payment"], options=[
        ft.dropdown.Option("Cash"),
        ft.dropdown.Option("Card")
    ], width=200)

    def fetch_sales():
        try:
            response = requests.get("http://localhost:5000/api/sales")
            if response.status_code == 200:
                data = response.json()
                sales.current.controls = [
                    ft.Text(f"Sale #{s['id']} - Total: ${s['total_amount']} - {s['payment_method']} - {s['created_at']}")
                    for s in data['sales']
                ]
                sales.current.update()
        except Exception:
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
            feedback.update()

    def add_sale(e):
        try:
            total_amount = float(unit_price_field.value) * int(quantity_field.value)
            response = requests.post("http://localhost:5000/api/sales", json={
                "user_id": user_id,
                "customer_id": None,
                "total_amount": total_amount,
                "payment_method": payment_field.value,
                "items": [{
                    "product_id": int(product_id_field.value),
                    "quantity": int(quantity_field.value),
                    "unit_price": float(unit_price_field.value)
                }]
            })
            if response.status_code == 201:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                fetch_sales()
            else:
                feedback.value = "Failed to record sale"
                feedback.color = ft.colors.RED
        except Exception:
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
        feedback.update()

    # Initial fetch
    fetch_sales()

    return ft.Container(
        content=ft.Column([
            ft.Text(lang["title"], size=20, weight=ft.FontWeight.BOLD),
            ft.Row([
                product_id_field,
                quantity_field,
                unit_price_field,
                payment_field,
                ft.ElevatedButton(lang["add"], on_click=add_sale, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE)
            ], alignment=ft.MainAxisAlignment.CENTER),
            sales.current if sales.current else ft.Column(),
            feedback
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100)
    )
