import logging
from flask import Blueprint, request, jsonify
from database import SessionLocal, cache_sale
from models import Sale, SaleItem, CachedSale
from sqlalchemy.orm import Session

sales_bp = Blueprint('sales', __name__)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_internet_available():
    import requests
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.RequestException:
        return False

@sales_bp.route('/sales', methods=['POST'])
def create_sale():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        customer_id = data.get('customer_id')
        total_amount = data.get('total_amount')
        payment_method = data.get('payment_method')
        items = data.get('items')  # List of {product_id, quantity, unit_price}
        logger.info(f"Creating sale for user: {user_id}")
        print(f"Creating sale for user: {user_id}")

        db = next(get_db())
        if not is_internet_available():
            # Cache sale for offline sync
            sale_data = {
                "user_id": user_id,
                "customer_id": customer_id,
                "total_amount": total_amount,
                "payment_method": payment_method
            }
            cache_sale(db, sale_data)
            logger.info("Sale cached offline")
            print("Sale cached offline")
            return jsonify({"message": "Sale cached offline"}), 201

        # Online: Save sale directly
        sale = Sale(
            user_id=user_id,
            customer_id=customer_id,
            total_amount=total_amount,
            payment_method=payment_method
        )
        db.add(sale)
        db.flush()

        for item in items:
            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                unit_price=item['unit_price']
            )
            db.add(sale_item)
        db.commit()
        logger.info(f"Sale created: {sale.id}")
        print(f"Sale created: {sale.id}")
        return jsonify({"message": "Sale created successfully", "sale_id": sale.id}), 201
    except Exception as e:
        logger.error(f"Create sale error: {str(e)}")
        print(f"Create sale error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@sales_bp.route('/sales', methods=['GET'])
def get_sales():
    try:
        db = next(get_db())
        sales = db.query(Sale).all()
        sale_list = [
            {
                "id": s.id,
                "user_id": s.user_id,
                "customer_id": s.customer_id,
                "total_amount": s.total_amount,
                "payment_method": s.payment_method,
                "created_at": s.created_at.isoformat()
            } for s in sales
        ]
        logger.info("Fetched all sales")
        print("Fetched all sales")
        return jsonify({"sales": sale_list}), 200
    except Exception as e:
        logger.error(f"Get sales error: {str(e)}")
        print(f"Get sales error: {str(e)}")
        return jsonify({"message": "Server error"}), 500
