import flet as ft
import requests

def build_products_view(page, language="en"):
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
            "no_products": "No products available",
            "search": "Search Products",
            "confirm_add": "Are you sure you want to add this product?",
            "confirm_delete": "Are you sure you want to delete this product?",
            "edit": "Edit",
            "delete": "Delete",
            "sort_by": "Sort By",
            "name_asc": "Name (A-Z)",
            "name_desc": "Name (Z-A)",
            "price_asc": "Price (Low to High)",
            "price_desc": "Price (High to Low)",
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
            "no_products": "Aucun produit disponible",
            "search": "Rechercher des produits",
            "confirm_add": "Êtes-vous sûr de vouloir ajouter ce produit ?",
            "confirm_delete": "Êtes-vous sûr de vouloir supprimer ce produit ?",
            "edit": "Modifier",
            "delete": "Supprimer",
            "sort_by": "Trier par",
            "name_asc": "Nom (A-Z)",
            "name_desc": "Nom (Z-A)",
            "price_asc": "Prix (Croissant)",
            "price_desc": "Prix (Décroissant)",
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
            "no_products": "No hay productos disponibles",
            "search": "Buscar productos",
            "confirm_add": "¿Estás seguro de que deseas agregar este producto?",
            "confirm_delete": "¿Estás seguro de que deseas eliminar este producto?",
            "edit": "Editar",
            "delete": "Eliminar",
            "sort_by": "Ordenar por",
            "name_asc": "Nombre (A-Z)",
            "name_desc": "Nombre (Z-A)",
            "price_asc": "Precio (Menor a Mayor)",
            "price_desc": "Precio (Mayor a Menor)",
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
        border_color=ft.colors.BLUE_700,
        on_change=lambda e: populate_products()
    )
    sort_dropdown = ft.Dropdown(
        label=lang["sort_by"],
        width=200,
        options=[
            ft.dropdown.Option(key="name_asc", text=lang["name_asc"]),
            ft.dropdown.Option(key="name_desc", text=lang["name_desc"]),
            ft.dropdown.Option(key="price_asc", text=lang["price_asc"]),
            ft.dropdown.Option(key="price_desc", text=lang["price_desc"])
        ],
        value="name_asc",
        border_color=ft.colors.BLUE_700,
        on_change=lambda e: populate_products()
    )

    # Input fields
    name_field = ft.TextField(
        label=lang["name"],
        width=250,
        border_color=ft.colors.BLUE_700,
        tooltip=lang["name_hint"],
        on_change=lambda e: validate_inputs()
    )
    price_field = ft.TextField(
        label=lang["price"],
        width=250,
        border_color=ft.colors.BLUE_700,
        tooltip=lang["price_hint"],
        on_change=lambda e: validate_inputs()
    )
    stock_field = ft.TextField(
        label=lang["stock"],
        width=250,
        border_color=ft.colors.BLUE_700,
        tooltip=lang["stock_hint"],
        on_change=lambda e: validate_inputs()
    )
    barcode_field = ft.TextField(
        label=lang["barcode"],
        width=250,
        border_color=ft.colors.BLUE_700,
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
        
        # Sorting
        sort_key = sort_dropdown.value
        if sort_key == "name_asc":
            products.sort(key=lambda x: x['name'].lower())
        elif sort_key == "name_desc":
            products.sort(key=lambda x: x['name'].lower(), reverse=True)
        elif sort_key == "price_asc":
            products.sort(key=lambda x: x['price'])
        elif sort_key == "price_desc":
            products.sort(key=lambda x: x['price'], reverse=True)

        if not products:
            products_list.controls.append(ft.Text(lang["no_products"], size=16, text_align="center"))
        else:
            for product in products:
                product_id = product['id']
                products_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.SHOPPING_BAG, color=ft.colors.BLUE_700),
                                title=ft.Text(product['name'], size=16, weight=ft.FontWeight.BOLD),
                                subtitle=ft.Text(f"Price: ${product['price']:.2f} | Stock: {product['stock']} | Barcode: {product['barcode']}", size=14),
                                content_padding=ft.padding.only(left=10, right=10),
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip=lang["edit"],
                                icon_color=ft.colors.BLUE_700,
                                on_click=lambda e, pid=product_id: edit_product(pid)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip=lang["delete"],
                                icon_color=ft.colors.RED_600,
                                on_click=lambda e, pid=product_id: delete_product(pid)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=ft.colors.WHITE,
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
                            populate_products()
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

    def edit_product(product_id):
        # Placeholder for edit functionality
        feedback.value = f"Edit product {product_id} (not implemented)"
        feedback.color = ft.colors.BLUE
        feedback.update()

    def delete_product(product_id):
        def confirm_delete(e):
            if e.control.text == "Yes":
                try:
                    response = requests.delete(f"http://localhost:5000/api/products/{product_id}")
                    if response.status_code == 204:
                        feedback.value = "Product deleted successfully!"
                        feedback.color = ft.colors.GREEN
                        populate_products()
                    else:
                        feedback.value = "Error deleting product"
                        feedback.color = ft.colors.RED
                except Exception as e:
                    feedback.value = "Error deleting product"
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
        price_field.value = ""
        stock_field.value = ""
        barcode_field.value = ""
        name_field.error_text = None
        price_field.error_text = None
        stock_field.error_text = None
        barcode_field.error_text = None
        name_field.update()
        price_field.update()
        stock_field.update()
        barcode_field.update()

    container = ft.Container(
        content=ft.Column([
            ft.Text(lang["title"], size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Row([
                search_field,
                sort_dropdown
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            name_field,
            price_field,
            stock_field,
            barcode_field,
            ft.ElevatedButton(
                text=lang["add_product"],
                width=250,
                bgcolor=ft.colors.BLUE_700,
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=create_product
            ),
            loading,
            feedback,
            ft.Container(
                content=products_list,
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

    return container, populate_products

def build_products_view_unauthorized(page, language="en"):
    texts = {
        "en": {
            "title": "Products",
            "no_products": "No products available",
            "search": "Search Products",
            "sort_by": "Sort By",
            "name_asc": "Name (A-Z)",
            "name_desc": "Name (Z-A)",
            "price_asc": "Price (Low to High)",
            "price_desc": "Price (High to Low)"
        },
        "fr": {
            "title": "Produits",
            "no_products": "Aucun produit disponible",
            "search": "Rechercher des produits",
            "sort_by": "Trier par",
            "name_asc": "Nom (A-Z)",
            "name_desc": "Nom (Z-A)",
            "price_asc": "Prix (Croissant)",
            "price_desc": "Prix (Décroissant)"
        },
        "es": {
            "title": "Productos",
            "no_products": "No hay productos disponibles",
            "search": "Buscar productos",
            "sort_by": "Ordenar por",
            "name_asc": "Nombre (A-Z)",
            "name_desc": "Nombre (Z-A)",
            "price_asc": "Precio (Menor a Mayor)",
            "price_desc": "Precio (Mayor a Menor)"
        }
    }
    lang = texts[language]

    products_list = ft.ListView(expand=True, spacing=10)
    loading = ft.ProgressRing(visible=False)
    search_field = ft.TextField(
        label=lang["search"],
        width=250,
        border_color=ft.colors.BLUE_700,
        on_change=lambda e: populate_products()
    )
    sort_dropdown = ft.Dropdown(
        label=lang["sort_by"],
        width=200,
        options=[
            ft.dropdown.Option(key="name_asc", text=lang["name_asc"]),
            ft.dropdown.Option(key="name_desc", text=lang["name_desc"]),
            ft.dropdown.Option(key="price_asc", text=lang["price_asc"]),
            ft.dropdown.Option(key="price_desc", text=lang["price_desc"])
        ],
        value="name_asc",
        border_color=ft.colors.BLUE_700,
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
        
        # Sorting
        sort_key = sort_dropdown.value
        if sort_key == "name_asc":
            products.sort(key=lambda x: x['name'].lower())
        elif sort_key == "name_desc":
            products.sort(key=lambda x: x['name'].lower(), reverse=True)
        elif sort_key == "price_asc":
            products.sort(key=lambda x: x['price'])
        elif sort_key == "price_desc":
            products.sort(key=lambda x: x['price'], reverse=True)

        if not products:
            products_list.controls.append(ft.Text(lang["no_products"], size=16, text_align="center"))
        else:
            for product in products:
                products_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.SHOPPING_BAG, color=ft.colors.BLUE_700),
                            title=ft.Text(product['name'], size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Price: ${product['price']:.2f} | Stock: {product['stock']} | Barcode: {product['barcode']}", size=14),
                            content_padding=ft.padding.only(left=10, right=10),
                        ),
                        bgcolor=ft.colors.WHITE,
                        border_radius=5,
                        padding=5
                    )
                )
        loading.visible = False
        products_list.update()
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
                content=products_list,
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

    return container, populate_products
