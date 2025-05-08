import flet as ft
import requests

def build_sales_view(page, user_id, language="en", show_back=False, go_back=None):
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
            "fetch_error": "Error fetching sales",
            "no_sales": "No sales available"
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
            "fetch_error": "Erreur lors de la récupération des ventes",
            "no_sales": "Aucune vente disponible"
        }
    }
    lang = texts[language]

    sales_list = ft.ListView(expand=True, spacing=10)
    feedback = ft.Text("", color=ft.colors.RED)

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
        sales = fetch_sales()
        if not sales:
            sales_list.controls.append(ft.Text(lang["no_sales"], size=16, text_align="center"))
        else:
            for sale in sales:
                sales_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.RECEIPT),
                            title=ft.Text(f"Sale ID: {sale['id']}", size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Total: ${sale['total_amount']:.2f} | Method: {sale['payment_method']}", size=14),
                            trailing=ft.Text(sale['created_at'], size=12),
                            content_padding=ft.padding.only(left=10, right=10),
                        ),
                        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
                        border_radius=5,
                        padding=5
                    )
                )
        sales_list.update()

    def create_sale(e):
        try:
            total_amount_field = page.controls[0].controls[1].content.controls[3]  # Total amount field
            payment_method_dropdown = page.controls[0].controls[1].content.controls[4]  # Payment method dropdown

            if not total_amount_field.value or not payment_method_dropdown.value:
                feedback.value = "Please fill all fields"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            # Map dropdown value to API expected value
            payment_method = "CASH" if payment_method_dropdown.value.lower() == "cash" else "CARD"

            response = requests.post(
                "http://localhost:5000/api/sales",
                json={
                    "total_amount": float(total_amount_field.value),
                    "payment_method": payment_method,
                    "user_id": user_id,
                    "items": []  # Ensure items list is included even if empty
                }
            )
            if response.status_code == 201:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                populate_sales()  # Refresh the list after adding a sale
            else:
                feedback.value = lang["error"]
                feedback.color = ft.colors.RED
            feedback.update()
        except Exception as e:
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
            feedback.update()

    analytics = fetch_analytics()
    total_sales = analytics["total_sales"]
    sale_count = analytics["sale_count"]

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
            ft.Row([
                ft.Text(f"{lang['total_sales']}: ${total_sales:.2f}", size=16),
                ft.Text(f"{lang['sale_count']}: {sale_count}", size=16)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.TextField(
                label=lang["total_amount"],
                width=250,
                border_color=ft.colors.BLUE,
                focused_border_color=ft.colors.BLUE_700,
                cursor_color=ft.colors.BLUE
            ),
            ft.Dropdown(
                label=lang["payment_method"],
                width=250,
                options=[
                    ft.dropdown.Option(lang["cash"]),
                    ft.dropdown.Option(lang["card"])
                ],
                border_color=ft.colors.BLUE,
                focused_border_color=ft.colors.BLUE_700
            ),
            ft.ElevatedButton(
                text=lang["add_sale"],
                width=250,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
                on_click=create_sale
            ),
            feedback,
            ft.Container(
                content=sales_list,
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=bgcolor,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_900)
    )

    return container, populate_sales

def build_sales_view_unauthorized(page, language="en", show_back=False, go_back=None):
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
            "success": "Sale completed successfully!",
            "error": "Error completing sale",
            "fetch_error": "Error fetching sales",
            "no_sales": "No sales available"
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
            "success": "Vente terminée avec succès !",
            "error": "Erreur lors de la vente",
            "fetch_error": "Erreur lors de la récupération des ventes",
            "no_sales": "Aucune vente disponible"
        }
    }
    lang = texts[language]

    sales_list = ft.ListView(expand=True, spacing=10)
    feedback = ft.Text("", color=ft.colors.RED)

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
        sales = fetch_sales()
        if not sales:
            sales_list.controls.append(ft.Text(lang["no_sales"], size=16, text_align="center"))
        else:
            for sale in sales:
                sales_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.RECEIPT),
                            title=ft.Text(f"Sale ID: {sale['id']}", size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Total: ${sale['total_amount']:.2f} | Method: {sale['payment_method']}", size=14),
                            trailing=ft.Text(sale['created_at'], size=12),
                            content_padding=ft.padding.only(left=10, right=10),
                        ),
                        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_800,
                        border_radius=5,
                        padding=5
                    )
                )
        sales_list.update()

    def create_sale(e):
        try:
            total_amount_field = page.controls[0].controls[1].content.controls[2]  # Total amount field
            payment_method_dropdown = page.controls[0].controls[1].content.controls[3]  # Payment method dropdown

            if not total_amount_field.value or not payment_method_dropdown.value:
                feedback.value = "Please fill all fields"
                feedback.color = ft.colors.RED
                feedback.update()
                return

            # Map dropdown value to API expected value
            payment_method = "CASH" if payment_method_dropdown.value.lower() == "cash" else "CARD"

            response = requests.post(
                "http://localhost:5000/api/sales",
                json={
                    "total_amount": float(total_amount_field.value),
                    "payment_method": payment_method,
                    "user_id": 0,  # Use 0 for unauthorized sales
                    "items": []  # Ensure items list is included even if empty
                }
            )
            if response.status_code == 201:
                feedback.value = lang["success"]
                feedback.color = ft.colors.GREEN
                populate_sales()  # Refresh the list after adding a sale
            else:
                feedback.value = lang["error"]
                feedback.color = ft.colors.RED
            feedback.update()
        except Exception as e:
            feedback.value = lang["error"]
            feedback.color = ft.colors.RED
            feedback.update()

    analytics = fetch_analytics()
    total_sales = analytics["total_sales"]
    sale_count = analytics["sale_count"]

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
            ft.Row([
                ft.Text(f"{lang['total_sales']}: ${total_sales:.2f}", size=16),
                ft.Text(f"{lang['sale_count']}: {sale_count}", size=16)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.TextField(
                label=lang["total_amount"],
                width=250,
                border_color=ft.colors.BLUE,
                focused_border_color=ft.colors.BLUE_700,
                cursor_color=ft.colors.BLUE
            ),
            ft.Dropdown(
                label=lang["payment_method"],
                width=250,
                options=[
                    ft.dropdown.Option(lang["cash"]),
                    ft.dropdown.Option(lang["card"])
                ],
                border_color=ft.colors.BLUE,
                focused_border_color=ft.colors.BLUE_700
            ),
            ft.ElevatedButton(
                text=lang["sell"],
                width=250,
                bgcolor=ft.colors.GREEN,
                color=ft.colors.WHITE,
                on_click=create_sale
            ),
            feedback,
            ft.Container(
                content=sales_list,
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=bgcolor,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.colors.BLUE_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_900)
    )

    return container, populate_sales
