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
            "no_products": "No products available",
            "search": "Search Products",
            "confirm_add": "Are you sure you want to add this product?",
            "name_hint": "Enter product name (min 3 characters)",
            "price_hint": "Enter price (e.g., 10.99)",
            "stock_hint": "Enter stock quantity (e.g., 100)",
            "barcode_hint": "Enter barcode (e.g., 123456789)"
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
            "no_products": "Aucun produit disponible",
            "search": "Rechercher des produits",
            "confirm_add": "Êtes-vous sûr de vouloir ajouter ce produit ?",
            "name_hint": "Entrez le nom du produit (min 3 caractères)",
            "price_hint": "Entrez le prix (ex. 10.99)",
            "stock_hint": "Entrez la quantité en stock (ex. 100)",
            "barcode_hint": "Entrez le code-barres (ex. 123456789)"
        },
        "es": {
            "title": "Productos",
            "name": "Nombre",
            "price": "Precio",
            "stock": "Stock",
            "barcode": "Código de barras",
            "add_product": "Agregar producto",
            "success": "¡Producto creado con éxito!",
            "error": "Error al crear el producto",
            "fetch_error": "Error al obtener los productos",
            "no_products": "No hay productos disponibles",
            "search": "Buscar productos",
            "confirm_add": "¿Estás seguro de que deseas agregar este producto?",
            "name_hint": "Ingresa el nombre del producto (mín. 3 caracteres)",
            "price_hint": "Ingresa el precio (ej. 10.99)",
            "stock_hint": "Ingresa la cantidad en stock (ej. 100)",
            "barcode_hint": "Ingresa el código de barras (ej. 123456789)"
        }
    }
    lang = texts[language]

    products_list = ft.ListView(expand=True, spacing=10)
    feedback = ft.Text("", color=ft.colors.RED)
    loading = ft.ProgressRing(visible=False)
    search_field = ft.TextField(
        label=lang["search"],
        width=250,
        border_color=ft.colors.BLUE,
        on_change=lambda e: populate_products()
    )

    # Input fields
    name_field = ft.TextField(
        label=lang["name"],
        width=250,
        border_color=ft.colors.BLUE,
        tooltip=lang["name_hint"],
        on_change=lambda e: validate_inputs()
    )
    price_field = ft.TextField(
        label=lang["price"],
        width=250,
        border_color=ft.colors.BLUE,
        tooltip=lang["price_hint"],
        on_change=lambda e: validate_inputs()
    )
    stock_field = ft.TextField(
        label=lang["stock"],
        width=250,
        border_color=ft.colors.BLUE,
        tooltip=lang["stock_hint"],
        on_change=lambda e: validate_inputs()
    )
    barcode_field = ft.TextField(
        label=lang["barcode"],
        width=250,
        border_color=ft.colors.BLUE,
        tooltip=lang["barcode_hint"],
        on_change=lambda e: validate_inputs()
    )

    def validate_inputs():
        if len(name_field.value.strip()) < 3:
            name_field.error_text = "Name must be at least 3 characters"
        else:
            name_field.error_text = None
        try:
            if price_field.value:
                float(price_field.value)
            price_field.error_text = None
        except ValueError:
            price_field.error_text = "Price must be a number"
        try:
            if stock_field.value:
                int(stock_field.value)
            stock_field.error_text = None
        except ValueError:
            stock_field.error_text = "Stock must be an integer"
        if len(barcode_field.value.strip()) < 3:
            barcode_field.error_text = "Barcode must be at least 3 characters"
        else:
            barcode_field.error_text = None
        name_field.update()
        price_field.update()
        stock_field.update()
        barcode_field.update()

    def fetch_products():
        try:
            response = requests.get("http://localhost:5000/api/products")
            if response.status_code == 200:
                return response.json().get("products", [])
        except Exception as e:
            print(f"Fetch products error: {str(e)}")
            return []

    def populate_products():
        products_list.controls.clear()
        loading.visible = True
        loading.update()
        products = fetch_products()
        search_term = search_field.value.lower()
        if search_term:
            products = [p for p in products if search_term in p['name'].lower() or search_term in p['barcode'].lower()]
        if not products:
            products_list.controls.append(ft.Text(lang["no_products"], size=16, text_align="center"))
        else:
            for product in products:
                products_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.SHOPPING_BAG),
                            title=ft.Text(product['name'], size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Price: ${product['price']:.2f} | Stock: {product['stock']} | Barcode: {product['barcode']}", size=14),
                            content_padding=ft.padding.only(left=10, right=10),
                        ),
                        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
                        border_radius=5,
                        padding=5
                    )
                )
        loading.visible = False
        products_list.update()
        loading.update()

    def create_product(e):
        try:
            if not name_field.value or not price_field.value or not stock_field.value or not barcode_field.value:
                feedback.value = "Please fill all fields"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            if name_field.error_text or price_field.error_text or stock_field.error_text or barcode_field.error_text:
                feedback.value = "Please fix the errors in the form"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            def confirm_add(e):
                if e.control.text == "Yes":
                    try:
                        response = requests.post(
                            "http://localhost:5000/api/products",
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
            price_field,
            stock_field,
            barcode_field,
            ft.ElevatedButton(
                text=lang["add_product"],
                width=250,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
                on_click=create_product
            ),
            loading,
            feedback,
            ft.Container(
                content=products_list,
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

    return container, populate_products

def build_products_view_unauthorized(page, language="en", show_back=False, go_back=None):
    texts = {
        "en": {
            "title": "Products",
            "no_products": "No products available",
            "search": "Search Products"
        },
        "fr": {
            "title": "Produits",
            "no_products": "Aucun produit disponible",
            "search": "Rechercher des produits"
        },
        "es": {
            "title": "Productos",
            "no_products": "No hay productos disponibles",
            "search": "Buscar productos"
        }
    }
    lang = texts[language]

    products_list = ft.ListView(expand=True, spacing=10)
    loading = ft.ProgressRing(visible=False)
    search_field = ft.TextField(
        label=lang["search"],
        width=250,
        border_color=ft.colors.BLUE,
        on_change=lambda e: populate_products()
    )

    def fetch_products():
        try:
            response = requests.get("http://localhost:5000/api/products")
            if response.status_code == 200:
                return response.json().get("products", [])
        except Exception as e:
            print(f"Fetch products error: {str(e)}")
            return []

    def populate_products():
        products_list.controls.clear()
        loading.visible = True
        loading.update()
        products = fetch_products()
        search_term = search_field.value.lower()
        if search_term:
            products = [p for p in products if search_term in p['name'].lower() or search_term in p['barcode'].lower()]
        if not products:
            products_list.controls.append(ft.Text(lang["no_products"], size=16, text_align="center"))
        else:
            for product in products:
                products_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.SHOPPING_BAG),
                            title=ft.Text(product['name'], size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Price: ${product['price']:.2f} | Stock: {product['stock']} | Barcode: {product['barcode']}", size=14),
                            content_padding=ft.padding.only(left=10, right=10),
                        ),
                        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
                        border_radius=5,
                        padding=5
                    )
                )
        loading.visible = False
        products_list.update()
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
                content=products_list,
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

    return container, populate_products
