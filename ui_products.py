import flet as ft
import requests

def build_products_view(page, language="en", show_back=False, go_back=None):
    # Localization
    texts = {
        "en": {
            "title": "Product Management",
            "name": "Name",
            "price": "Price",
            "stock": "Stock",
            "barcode": "Barcode",
            "add": "Add Product",
            "update": "Update",
            "delete": "Delete",
            "success": "Success!",
            "error": "Error: Cannot connect to server!"
        },
        "fr": {
            "title": "Gestion des produits",
            "name": "Nom",
            "price": "Prix",
            "stock": "Stock",
            "barcode": "Code-barres",
            "add": "Ajouter un produit",
            "update": "Mettre à jour",
            "delete": "Supprimer",
            "success": "Succès !",
            "error": "Erreur : Impossible de se connecter au serveur !"
        }
    }
    lang = texts[language]

    # State
    feedback = ft.Text("", color=ft.colors.RED)
    products = ft.Ref[ft.Column]()

    # Input fields
    name_field = ft.TextField(label=lang["name"], width=200)
    price_field = ft.TextField(label=lang["price"], width=100, keyboard_type=ft.KeyboardType.NUMBER)
    stock_field = ft.TextField(label=lang["stock"], width=100, keyboard_type=ft.KeyboardType.NUMBER)
    barcode_field = ft.TextField(label=lang["barcode"], width=200)

    def fetch_products():
        try:
            response = requests.get("http://localhost:5000/api/products")
            if response.status_code == 200:
                data = response.json()
                products.current.controls = [
                    ft.Row([
                        ft.Text(f"{p['name']} - ${p['price']} - Stock: {p['stock']}"),
                        ft.ElevatedButton(
                            lang["update"],
                            on_click=lambda e, pid=p['id']: update_product(pid),
                            bgcolor=ft.colors.BLUE,
                            color=ft.colors.WHITE
                        ),
                        ft.ElevatedButton(
                            lang["delete"],
                            on_click=lambda e, pid=p['id']: delete_product(pid),
                            bgcolor=ft.colors.RED,
                            color=ft.colors.WHITE
                        )
                    ]) for p in data['products']
                ]
                products.current.update()
        except Exception:
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
            feedback.update()

    def add_product(e):
        try:
            response = requests.post("http://localhost:5000/api/products", json={
                "name": name_field.value,
                "price": float(price_field.value),
                "stock": int(stock_field.value),
                "barcode": barcode_field.value
            })
            if response.status_code == 201:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                fetch_products()
            else:
                feedback.value = "Failed to add product"
                feedback.color = ft.colors.RED
        except Exception:
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
        feedback.update()

    def update_product(product_id):
        try:
            response = requests.put(f"http://localhost:5000/api/products/{product_id}", json={
                "name": name_field.value,
                "price": float(price_field.value),
                "stock": int(stock_field.value),
                "barcode": barcode_field.value
            })
            if response.status_code == 200:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                fetch_products()
            else:
                feedback.value = "Failed to update product"
                feedback.color = ft.colors.RED
        except Exception:
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
        feedback.update()

    def delete_product(product_id):
        try:
            response = requests.delete(f"http://localhost:5000/api/products/{product_id}")
            if response.status_code == 200:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                fetch_products()
            else:
                feedback.value = "Failed to delete product"
                feedback.color = ft.colors.RED
        except Exception:
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
        feedback.update()

    # Initial fetch
    fetch_products()

    # Back button
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=lambda e: go_back(),
        tooltip="Back",
        visible=show_back
    )

    return ft.Container(
        content=ft.Column([
            back_button,
            ft.Text(lang["title"], size=20, weight=ft.FontWeight.BOLD),
            ft.Row([
                name_field,
                price_field,
                stock_field,
                barcode_field,
                ft.ElevatedButton(lang["add"], on_click=add_product, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE)
            ], alignment=ft.MainAxisAlignment.CENTER),
            products.current if products.current else ft.Column(),
            feedback
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100)
    )
