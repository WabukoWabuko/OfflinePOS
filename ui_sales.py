import flet as ft
import requests

def build_sales_view(page, user_id, language="en"):
    texts = {
        "en": {
            "title": "Sales",
            "total_sales": "Total Sales",
            "sale_count": "Sale Count",
            "create_sale": "Create Sale",
            "total_amount": "Total Amount",
            "payment_method": "Payment Method",
            "cash": "Cash",
            "card": "Card",
            "add_sale": "Add Sale",
            "success": "Sale created successfully!",
            "error": "Error creating sale",
            "no_sales": "No sales available",
            "search": "Search Sales",
            "confirm_add": "Are you sure you want to add this sale?",
            "view_details": "View Details",
            "sort_by": "Sort By",
            "date_asc": "Date (Oldest First)",
            "date_desc": "Date (Newest First)",
            "amount_asc": "Amount (Low to High)",
            "amount_desc": "Amount (High to Low)",
            "total_amount_hint": "Enter total amount (e.g., 29.99)",
            "payment_method_hint": "Select payment method"
        },
        "fr": {
            "title": "Ventes",
            "total_sales": "Ventes totales",
            "sale_count": "Nombre de ventes",
            "create_sale": "Créer une vente",
            "total_amount": "Montant total",
            "payment_method": "Méthode de paiement",
            "cash": "Espèces",
            "card": "Carte",
            "add_sale": "Ajouter une vente",
            "success": "Vente créée avec succès !",
            "error": "Erreur lors de la création de la vente",
            "no_sales": "Aucune vente disponible",
            "search": "Rechercher des ventes",
            "confirm_add": "Êtes-vous sûr de vouloir ajouter cette vente ?",
            "view_details": "Voir les détails",
            "sort_by": "Trier par",
            "date_asc": "Date (Plus ancien en premier)",
            "date_desc": "Date (Plus récent en premier)",
            "amount_asc": "Montant (Croissant)",
            "amount_desc": "Montant (Décroissant)",
            "total_amount_hint": "Entrez le montant total (ex. 29.99)",
            "payment_method_hint": "Sélectionnez la méthode de paiement"
        },
        "es": {
            "title": "Ventas",
            "total_sales": "Ventas totales",
            "sale_count": "Cantidad de ventas",
            "create_sale": "Crear venta",
            "total_amount": "Monto total",
            "payment_method": "Método de pago",
            "cash": "Efectivo",
            "card": "Tarjeta",
            "add_sale": "Agregar venta",
            "success": "¡Venta creada con éxito!",
            "error": "Error al crear la venta",
            "no_sales": "No hay ventas disponibles",
            "search": "Buscar ventas",
            "confirm_add": "¿Estás seguro de que deseas agregar esta venta?",
            "view_details": "Ver detalles",
            "sort_by": "Ordenar por",
            "date_asc": "Fecha (Más antiguo primero)",
            "date_desc": "Fecha (Más reciente primero)",
            "amount_asc": "Monto (Menor a Mayor)",
            "amount_desc": "Monto (Mayor a Menor)",
            "total_amount_hint": "Ingresa el monto total (ej. 29.99)",
            "payment_method_hint": "Selecciona el método de pago"
        }
    }
    lang = texts[language]

    sales_list = ft.ListView(expand=True, spacing=10)
    feedback = ft.Text("", color=ft.colors.RED)
    loading = ft.ProgressRing(visible=False)
    search_field = ft.TextField(
        label=lang["search"],
        width=250,
        border_color=ft.colors.BLUE_700,
        on_change=lambda e: populate_sales()
    )
    sort_dropdown = ft.Dropdown(
        label=lang["sort_by"],
        width=200,
        options=[
            ft.dropdown.Option(key="date_desc", text=lang["date_desc"]),
            ft.dropdown.Option(key="date_asc", text=lang["date_asc"]),
            ft.dropdown.Option(key="amount_asc", text=lang["amount_asc"]),
            ft.dropdown.Option(key="amount_desc", text=lang["amount_desc"])
        ],
        value="date_desc",
        border_color=ft.colors.BLUE_700,
        on_change=lambda e: populate_sales()
    )

    # Input fields
    total_amount_field = ft.TextField(
        label=lang["total_amount"],
        width=250,
        border_color=ft.colors.BLUE_700,
        tooltip=lang["total_amount_hint"],
        on_change=lambda e: validate_inputs()
    )
    payment_method_dropdown = ft.Dropdown(
        label=lang["payment_method"],
        width=250,
        options=[
            ft.dropdown.Option(lang["cash"]),
            ft.dropdown.Option(lang["card"])
        ],
        border_color=ft.colors.BLUE_700,
        tooltip=lang["payment_method_hint"]
    )

    def validate_inputs():
        try:
            if total_amount_field.value:
                float(total_amount_field.value)
            total_amount_field.error_text = None
        except ValueError:
            total_amount_field.error_text = "Total amount must be a number"
        total_amount_field.update()

    def fetch_analytics():
        try:
            response = requests.get("http://localhost:5000/api/sales/analytics")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Analytics fetch error: {str(e)}")
            return {"total_sales": 0, "sale_count": 0}

    def fetch_sales():
        try:
            response = requests.get("http://localhost:5000/api/sales")
            if response.status_code == 200:
                return response.json().get("sales", [])
        except Exception as e:
            print(f"Fetch sales error: {str(e)}")
            return []

    def populate_sales():
        sales_list.controls.clear()
        loading.visible = True
        loading.update()
        sales = fetch_sales()
        search_term = search_field.value.lower()
        if search_term:
            sales = [s for s in sales if search_term in str(s['id']).lower() or search_term in s['payment_method'].lower()]
        
        # Sorting
        sort_key = sort_dropdown.value
        if sort_key == "date_asc":
            sales.sort(key=lambda x: x['created_at'])
        elif sort_key == "date_desc":
            sales.sort(key=lambda x: x['created_at'], reverse=True)
        elif sort_key == "amount_asc":
            sales.sort(key=lambda x: x['total_amount'])
        elif sort_key == "amount_desc":
            sales.sort(key=lambda x: x['total_amount'], reverse=True)

        if not sales:
            sales_list.controls.append(ft.Text(lang["no_sales"], size=16, text_align="center"))
        else:
            for sale in sales:
                sale_id = sale['id']
                sales_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.RECEIPT, color=ft.colors.BLUE_700),
                                title=ft.Text(f"Sale ID: {sale['id']}", size=16, weight=ft.FontWeight.BOLD),
                                subtitle=ft.Text(f"Total: ${sale['total_amount']:.2f} | Method: {sale['payment_method']}", size=14),
                                trailing=ft.Text(sale['created_at'], size=12),
                                content_padding=ft.padding.only(left=10, right=10),
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.icons.VISIBILITY,
                                tooltip=lang["view_details"],
                                icon_color=ft.colors.BLUE_700,
                                on_click=lambda e, sid=sale_id: view_sale_details(sid)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=ft.colors.WHITE,
                        border_radius=5,
                        padding=5
                    )
                )
        loading.visible = False
        sales_list.update()
        loading.update()

    def create_sale(e):
        try:
            if not total_amount_field.value or not payment_method_dropdown.value:
                feedback.value = "Please fill all fields"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            if total_amount_field.error_text:
                feedback.value = "Please fix the errors in the form"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            def confirm_add(e):
                if e.control.text == "Yes":
                    try:
                        payment_method = "CASH" if payment_method_dropdown.value.lower() == "cash" else "CARD"
                        response = requests.post(
                            "http://localhost:5000/api/sales",
                            json={
                                "total_amount": float(total_amount_field.value),
                                "payment_method": payment_method,
                                "user_id": user_id,
                                "items": []
                            }
                        )
                        if response.status_code == 201:
                            feedback.value = lang["success"]
                            feedback.color = ft.colors.GREEN
                            populate_sales()
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

    def view_sale_details(sale_id):
        sale = next((s for s in fetch_sales() if s['id'] == sale_id), None)
        if sale:
            content = ft.Column([
                ft.Text(f"Sale ID: {sale['id']}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Total Amount: ${sale['total_amount']:.2f}"),
                ft.Text(f"Payment Method: {sale['payment_method']}"),
                ft.Text(f"Date: {sale['created_at']}")
            ])
            page.dialog = ft.AlertDialog(
                title=ft.Text("Sale Details"),
                content=content,
                actions=[ft.ElevatedButton("Close", on_click=lambda e: close_dialog())],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.update()

    def close_dialog():
        page.dialog = None
        page.update()

    def clear_fields():
        total_amount_field.value = ""
        payment_method_dropdown.value = None
        total_amount_field.error_text = None
        total_amount_field.update()
        payment_method_dropdown.update()

    analytics = fetch_analytics()
    total_sales = analytics["total_sales"]
    sale_count = analytics["sale_count"]

    container = ft.Container(
        content=ft.Column([
            ft.Text(lang["title"], size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Row([
                ft.Text(f"{lang['total_sales']}: ${total_sales:.2f}", size=16),
                ft.Text(f"{lang['sale_count']}: {sale_count}", size=16)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Row([
                search_field,
                sort_dropdown
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            total_amount_field,
            payment_method_dropdown,
            ft.ElevatedButton(
                text=lang["add_sale"],
                width=250,
                bgcolor=ft.colors.BLUE_700,
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=create_sale
            ),
            loading,
            feedback,
            ft.Container(
                content=sales_list,
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

    return container, populate_sales

def build_sales_view_unauthorized(page, language="en"):
    texts = {
        "en": {
            "title": "Sales",
            "total_sales": "Total Sales",
            "sale_count": "Sale Count",
            "sell": "Sell",
            "total_amount": "Total Amount",
            "payment_method": "Payment Method",
            "cash": "Cash",
            "card": "Card",
            "barcode": "Barcode",
            "success": "Sale completed successfully!",
            "error": "Error completing sale",
            "no_sales": "No sales available",
            "search": "Search Sales",
            "receipt": "Receipt",
            "confirm_add": "Are you sure you want to complete this sale?",
            "view_details": "View Details",
            "sort_by": "Sort By",
            "date_asc": "Date (Oldest First)",
            "date_desc": "Date (Newest First)",
            "amount_asc": "Amount (Low to High)",
            "amount_desc": "Amount (High to Low)",
            "total_amount_hint": "Enter total amount (e.g., 29.99)",
            "payment_method_hint": "Select payment method",
            "barcode_hint": "Enter barcode to auto-fill amount"
        },
        "fr": {
            "title": "Ventes",
            "total_sales": "Ventes totales",
            "sale_count": "Nombre de ventes",
            "sell": "Vendre",
            "total_amount": "Montant total",
            "payment_method": "Méthode de paiement",
            "cash": "Espèces",
            "card": "Carte",
            "barcode": "Code-barres",
            "success": "Vente terminée avec succès !",
            "error": "Erreur lors de la vente",
            "no_sales": "Aucune vente disponible",
            "search": "Rechercher des ventes",
            "receipt": "Reçu",
            "confirm_add": "Êtes-vous sûr de vouloir finaliser cette vente ?",
            "view_details": "Voir les détails",
            "sort_by": "Trier par",
            "date_asc": "Date (Plus ancien en premier)",
            "date_desc": "Date (Plus récent en premier)",
            "amount_asc": "Montant (Croissant)",
            "amount_desc": "Montant (Décroissant)",
            "total_amount_hint": "Entrez le montant total (ex. 29.99)",
            "payment_method_hint": "Sélectionnez la méthode de paiement",
            "barcode_hint": "Entrez le code-barres pour remplir automatiquement"
        },
        "es": {
            "title": "Ventas",
            "total_sales": "Ventas totales",
            "sale_count": "Cantidad de ventas",
            "sell": "Vender",
            "total_amount": "Monto total",
            "payment_method": "Método de pago",
            "cash": "Efectivo",
            "card": "Tarjeta",
            "barcode": "Código de barras",
            "success": "¡Venta completada con éxito!",
            "error": "Error al completar la venta",
            "no_sales": "No hay ventas disponibles",
            "search": "Buscar ventas",
            "receipt": "Recibo",
            "confirm_add": "¿Estás seguro de que deseas completar esta venta?",
            "view_details": "Ver detalles",
            "sort_by": "Ordenar por",
            "date_asc": "Fecha (Más antiguo primero)",
            "date_desc": "Fecha (Más reciente primero)",
            "amount_asc": "Monto (Menor a Mayor)",
            "amount_desc": "Monto (Mayor a Menor)",
            "total_amount_hint": "Ingresa el monto total (ej. 29.99)",
            "payment_method_hint": "Selecciona el método de pago",
            "barcode_hint": "Ingresa el código de barras para autocompletar"
        }
    }
    lang = texts[language]

    sales_list = ft.ListView(expand=True, spacing=10)
    feedback = ft.Text("", color=ft.colors.RED)
    loading = ft.ProgressRing(visible=False)
    search_field = ft.TextField(
        label=lang["search"],
        width=250,
        border_color=ft.colors.BLUE_700,
        on_change=lambda e: populate_sales()
    )
    sort_dropdown = ft.Dropdown(
        label=lang["sort_by"],
        width=200,
        options=[
            ft.dropdown.Option(key="date_desc", text=lang["date_desc"]),
            ft.dropdown.Option(key="date_asc", text=lang["date_asc"]),
            ft.dropdown.Option(key="amount_asc", text=lang["amount_asc"]),
            ft.dropdown.Option(key="amount_desc", text=lang["amount_desc"])
        ],
        value="date_desc",
        border_color=ft.colors.BLUE_700,
        on_change=lambda e: populate_sales()
    )

    # Input fields
    barcode_field = ft.TextField(
        label=lang["barcode"],
        width=250,
        border_color=ft.colors.BLUE_700,
        tooltip=lang["barcode_hint"],
        on_change=lambda e: auto_fill_amount()
    )
    total_amount_field = ft.TextField(
        label=lang["total_amount"],
        width=250,
        border_color=ft.colors.BLUE_700,
        tooltip=lang["total_amount_hint"],
        on_change=lambda e: validate_inputs()
    )
    payment_method_dropdown = ft.Dropdown(
        label=lang["payment_method"],
        width=250,
        options=[
            ft.dropdown.Option(lang["cash"]),
            ft.dropdown.Option(lang["card"])
        ],
        border_color=ft.colors.BLUE_700,
        tooltip=lang["payment_method_hint"]
    )

    def validate_inputs():
        try:
            if total_amount_field.value:
                float(total_amount_field.value)
            total_amount_field.error_text = None
        except ValueError:
            total_amount_field.error_text = "Total amount must be a number"
        total_amount_field.update()

    def auto_fill_amount():
        try:
            barcode = barcode_field.value
            if barcode:
                response = requests.get("http://localhost:5000/api/products")
                if response.status_code == 200:
                    products = response.json().get("products", [])
                    for product in products:
                        if product['barcode'] == barcode:
                            total_amount_field.value = str(product['price'])
                            total_amount_field.update()
                            break
        except Exception as e:
            print(f"Barcode fetch error: {str(e)}")

    def fetch_analytics():
        try:
            response = requests.get("http://localhost:5000/api/sales/analytics")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Analytics fetch error: {str(e)}")
            return {"total_sales": 0, "sale_count": 0}

    def fetch_sales():
        try:
            response = requests.get("http://localhost:5000/api/sales")
            if response.status_code == 200:
                return response.json().get("sales", [])
        except Exception as e:
            print(f"Fetch sales error: {str(e)}")
            return []

    def populate_sales():
        sales_list.controls.clear()
        loading.visible = True
        loading.update()
        sales = fetch_sales()
        search_term = search_field.value.lower()
        if search_term:
            sales = [s for s in sales if search_term in str(s['id']).lower() or search_term in s['payment_method'].lower()]
        
        # Sorting
        sort_key = sort_dropdown.value
        if sort_key == "date_asc":
            sales.sort(key=lambda x: x['created_at'])
        elif sort_key == "date_desc":
            sales.sort(key=lambda x: x['created_at'], reverse=True)
        elif sort_key == "amount_asc":
            sales.sort(key=lambda x: x['total_amount'])
        elif sort_key == "amount_desc":
            sales.sort(key=lambda x: x['total_amount'], reverse=True)

        if not sales:
            sales_list.controls.append(ft.Text(lang["no_sales"], size=16, text_align="center"))
        else:
            for sale in sales:
                sale_id = sale['id']
                sales_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.RECEIPT, color=ft.colors.BLUE_700),
                                title=ft.Text(f"Sale ID: {sale['id']}", size=16, weight=ft.FontWeight.BOLD),
                                subtitle=ft.Text(f"Total: ${sale['total_amount']:.2f} | Method: {sale['payment_method']}", size=14),
                                trailing=ft.Text(sale['created_at'], size=12),
                                content_padding=ft.padding.only(left=10, right=10),
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.icons.VISIBILITY,
                                tooltip=lang["view_details"],
                                icon_color=ft.colors.BLUE_700,
                                on_click=lambda e, sid=sale_id: view_sale_details(sid)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=ft.colors.WHITE,
                        border_radius=5,
                        padding=5
                    )
                )
        loading.visible = False
        sales_list.update()
        loading.update()

    def create_sale(e):
        try:
            if not total_amount_field.value or not payment_method_dropdown.value:
                feedback.value = "Please fill all fields"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            if total_amount_field.error_text:
                feedback.value = "Please fix the errors in the form"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            def confirm_add(e):
                if e.control.text == "Yes":
                    try:
                        payment_method = "CASH" if payment_method_dropdown.value.lower() == "cash" else "CARD"
                        response = requests.post(
                            "http://localhost:5000/api/sales",
                            json={
                                "total_amount": float(total_amount_field.value),
                                "payment_method": payment_method,
                                "user_id": 0,
                                "items": []
                            }
                        )
                        if response.status_code == 201:
                            sale_data = response.json()
                            show_receipt(sale_data)
                            feedback.value = lang["success"]
                            feedback.color = ft.colors.GREEN
                            populate_sales()
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

    def show_receipt(sale_data):
        receipt_content = ft.Column([
            ft.Text(lang["receipt"], size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Sale ID: {sale_data.get('id', 'N/A')}"),
            ft.Text(f"Total: ${sale_data.get('total_amount', 0):.2f}"),
            ft.Text(f"Payment Method: {sale_data.get('payment_method', 'N/A')}"),
            ft.Text(f"Date: {sale_data.get('created_at', 'N/A')}")
        ])
        page.dialog = ft.AlertDialog(
            title=ft.Text("Receipt"),
            content=receipt_content,
            actions=[
                ft.ElevatedButton(text="Close", on_click=lambda e: close_dialog())
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.update()

    def view_sale_details(sale_id):
        sale = next((s for s in fetch_sales() if s['id'] == sale_id), None)
        if sale:
            content = ft.Column([
                ft.Text(f"Sale ID: {sale['id']}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Total Amount: ${sale['total_amount']:.2f}"),
                ft.Text(f"Payment Method: {sale['payment_method']}"),
                ft.Text(f"Date: {sale['created_at']}")
            ])
            page.dialog = ft.AlertDialog(
                title=ft.Text("Sale Details"),
                content=content,
                actions=[ft.ElevatedButton("Close", on_click=lambda e: close_dialog())],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.update()

    def close_dialog():
        page.dialog = None
        page.update()

    def clear_fields():
        barcode_field.value = ""
        total_amount_field.value = ""
        payment_method_dropdown.value = None
        total_amount_field.error_text = None
        barcode_field.update()
        total_amount_field.update()
        payment_method_dropdown.update()

    analytics = fetch_analytics()
    total_sales = analytics["total_sales"]
    sale_count = analytics["sale_count"]

    container = ft.Container(
        content=ft.Column([
            ft.Text(lang["title"], size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Row([
                ft.Text(f"{lang['total_sales']}: ${total_sales:.2f}", size=16),
                ft.Text(f"{lang['sale_count']}: {sale_count}", size=16)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Row([
                search_field,
                sort_dropdown
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            barcode_field,
            total_amount_field,
            payment_method_dropdown,
            ft.ElevatedButton(
                text=lang["sell"],
                width=250,
                bgcolor=ft.colors.GREEN_600,
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=create_sale
            ),
            loading,
            feedback,
            ft.Container(
                content=sales_list,
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

    return container, populate_sales
