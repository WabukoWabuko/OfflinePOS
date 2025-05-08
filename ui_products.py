import flet as ft
import requests

def build_products_view(page, language="en", show_back=False, go_back=None):
    texts = {
        "en": {
            "title": "Products",
            "name": "Name",
            "price": "Price",
            "stock": "Stock",
            "barcode": "Barcode",
            "add_product": "Add Product",
            "success": "Product created successfully!",
            "error": "Error creating product",
            "fetch_error": "Error fetching products",
            "no_products": "No products available"
        },
        "fr": {
            "title": "Produits",
            "name": "Nom",
            "price": "Prix",
            "stock": "Stock",
            "barcode": "Code-barres",
            "add_product": "Ajouter un produit",
            "success": "Produit créé avec succès !",
            "error": "Erreur lors de la création du produit",
            "fetch_error": "Erreur lors de la récupération des produits",
            "no_products": "Aucun produit disponible"
        }
    }
    lang = texts[language]

    products_list = ft.ListView(expand=True, spacing=10)
    feedback = ft.Text("", color=ft.colors.RED)

    def fetch_products():
        try:
            response = requests.get("http://offlinepos:5000/api/products")
            if response.status_code == 200:
                return response.json().get("products", [])
        except Exception as e:
            print(f"Fetch products error: {str(e)}")
            return []

    def populate_products():
        products_list.controls.clear()
        products = fetch_products()
        if not products:
            products_list.controls.append(ft.Text(lang["no_products"]))
        else:
            for product in products:
                products_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(f"{product['name']}"),
                        subtitle=ft.Text(f"Price: ${product['price']:.2f}, Stock: {product['stock']}, Barcode: {product['barcode']}")
                    )
                )
        products_list.update()

    def create_product(e):
        try:
            name_field = page.controls[0].controls[1].content.controls[2]  # Name field
            price_field = page.controls[0].controls[1].content.controls[3]  # Price field
            stock_field = page.controls[0].controls[1].content.controls[4]  # Stock field
            barcode_field = page.controls[0].controls[1].content.controls[5]  # Barcode field

            if not name_field.value or not price_field.value or not stock_field.value or not barcode_field.value:
                feedback.value = "Please fill all fields"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            response = requests.post(
                "http://offlinepos:5000/api/products",
                json={
                    "name": name_field.value,
                    "price": float(price_field.value),
                    "stock": int(stock_field.value),
                    "barcode": barcode_field.value
                }
            )
            if response.status_code == 201:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                populate_products()  # Refresh the list after adding a product
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
            ft.TextField(label=lang["name"], width=200, border_color=ft.colors.BLUE),
            ft.TextField(label=lang["price"], width=200, border_color=ft.colors.BLUE),
            ft.TextField(label=lang["stock"], width=200, border_color=ft.colors.BLUE),
            ft.TextField(label=lang["barcode"], width=200, border_color=ft.colors.BLUE),
            ft.ElevatedButton(
                text=lang["add_product"],
                width=200,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
                on_click=create_product
            ),
            feedback,
            products_list
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=bgcolor,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_900)
    )

    return container, populate_products
