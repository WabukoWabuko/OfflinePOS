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
            "error": "Error: Cannot connect to server!",
            "invalid_price": "Price must be a positive number",
            "invalid_stock": "Stock must be a positive integer"
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
            "error": "Erreur : Impossible de se connecter au serveur !",
            "invalid_price": "Le prix doit être un nombre positif",
            "invalid_stock": "Le stock doit être un entier positif"
        }
    }
    lang = texts[language]

    # State
    feedback = ft.Text("", color=ft.colors.RED)
    products = ft.Ref[ft.Column]()

    # Input fields with validation
    name_field = ft.TextField(label=lang["name"], width=200)
    price_field = ft.TextField(label=lang["price"], width=100, keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: validate_price())
    stock_field = ft.TextField(label=lang["stock"], width=100, keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: validate_stock())
    barcode_field = ft.TextField(label=lang["barcode"], width=200)

    def validate_price():
        if price_field.value and (not price_field.value.replace('.', '').isdigit() or float(price_field.value) < 0):
            feedback.value = lang["invalid_price"]
            feedback.color = ft.colors.RED
        else:
            feedback.value = ""
        feedback.update()

    def validate_stock():
        if stock_field.value and (not stock_field.value.isdigit() or int(stock_field.value) < 0):
            feedback.value = lang["invalid_stock"]
            feedback.color = ft.colors.RED
        else:
            feedback.value = ""
        feedback.update()

    def fetch_products():
        try:
            response = requests.get("http://offlinepos:5000/api/products")
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
            else:
                feedback.value = lang["error"]
                feedback.color = ft.colors.RED
        except Exception as e:
            print(f"Fetch products error: {str(e)}")
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED

    def add_product(e):
        try:
            if not price_field.value.replace('.', '').isdigit() or float(price_field.value) < 0:
                feedback.value = lang["invalid_price"]
                feedback.color = ft.colors.RED
                feedback.update()
                return
            if not stock_field.value.isdigit() or int(stock_field.value) < 0:
                feedback.value = lang["invalid_stock"]
                feedback.color = ft.colors.RED
                feedback.update()
                return
            response = requests.post("http://offlinepos:5000/api/products", json={
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
        except Exception as e:
            print(f"Add product error: {str(e)}")
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
        feedback.update()

    def update_product(product_id):
        try:
            if not price_field.value.replace('.', '').isdigit() or float(price_field.value) < 0:
                feedback.value = lang["invalid_price"]
                feedback.color = ft.colors.RED
                feedback.update()
                return
            if not stock_field.value.isdigit() or int(stock_field.value) < 0:
                feedback.value = lang["invalid_stock"]
                feedback.color = ft.colors.RED
                feedback.update()
                return
            response = requests.put(f"http://offlinepos:5000/api/products/{product_id}", json={
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
        except Exception as e:
            print(f"Update product error: {str(e)}")
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
        feedback.update()

    def delete_product(product_id):
        try:
            response = requests.delete(f"http://offlinepos:5000/api/products/{product_id}")
            if response.status_code == 200:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                fetch_products()
            else:
                feedback.value = "Failed to delete product"
                feedback.color = ft.colors.RED
        except Exception as e:
            print(f"Delete product error: {str(e)}")
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
        feedback.update()

    # Build container first
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=lambda e: go_back(),
        tooltip="Back",
        visible=show_back
    )

    container = ft.Container(
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
            ft.Column(ref=products),
            feedback
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100)
    )

    # Fetch products after the container is built
    fetch_products()

    return container
