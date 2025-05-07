import logging
from flask import Blueprint, request, jsonify
from database import SessionLocal, cache_sale
from models import Sale, SaleItem
from sqlalchemy.orm import Session

sales_bp = Blueprint('sales', __name__, url_prefix='/api/sales')
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_sale_data(data):
    required_fields = {"total_amount", "payment_method"}
    if not all(k in data for k in required_fields):
        return False, "Missing required fields: total_amount or payment_method"
    if not isinstance(data["total_amount"], (int, float)) or data["total_amount"] < 0:
        return False, "Invalid total_amount"
    if data["payment_method"] not in ["Cash", "Card"]:
        return False, "Invalid payment_method"
    return True, ""

@sales_bp.route('/cache', methods=['POST'])
def cache_sale_endpoint():
    try:
        data = request.get_json()
        required_fields = {"user_id", "total_amount", "payment_method"}
        if not all(k in data for k in required_fields):
            logger.warning("Cache sale failed: Missing required fields")
            return jsonify({"message": "Missing required fields: user_id, total_amount, payment_method"}), 400

        db = next(get_db())
        cache_sale(db, data)
        logger.info("Sale cached successfully")
        return jsonify({"message": "Sale cached successfully"}), 201
    except Exception as e:
        logger.error(f"Cache sale error: {str(e)}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500

@sales_bp.route('', methods=['POST'])
def create_sale():
    try:
        data = request.get_json()
        is_valid, message = validate_sale_data(data)
        if not is_valid:
            return jsonify({"message": message}), 400

        total_amount = float(data.get('total_amount'))
        payment_method = data.get('payment_method')
        user_id = data.get('user_id')
        customer_id = data.get('customer_id')
        items = data.get('items', [])

        logger.info(f"Creating sale with total_amount: {total_amount}, payment_method: {payment_method}")
        db = next(get_db())
        sale = Sale(user_id=user_id, customer_id=customer_id, total_amount=total_amount, payment_method=payment_method)
        db.add(sale)
        db.flush()

        for item in items:
            sale_item = SaleItem(sale_id=sale.id, product_id=item.get('product_id'), quantity=item.get('quantity'), unit_price=item.get('unit_price'))
            db.add(sale_item)

        db.commit()
        logger.info(f"Sale created with id: {sale.id}")
        return jsonify({"message": "Sale created successfully", "sale_id": sale.id}), 201
    except ValueError as ve:
        logger.error(f"Validation error creating sale: {str(ve)}")
        return jsonify({"message": f"Validation error: {str(ve)}"}), 400
    except Exception as e:
        logger.error(f"Create sale error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@sales_bp.route('', methods=['GET'])
def get_sales():
    try:
        db = next(get_db())
        sales = db.query(Sale).all()
        sales_list = [{"id": s.id, "user_id": s.user_id, "customer_id": s.customer_id, "total_amount": s.total_amount, "payment_method": s.payment_method, "created_at": s.created_at.isoformat()} for s in sales]
        logger.info("Fetched all sales")
        return jsonify({"sales": sales_list}), 200
    except Exception as e:
        logger.error(f"Get sales error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@sales_bp.route('/<int:sale_id>', methods=['PUT'])
def update_sale(sale_id):
    try:
        data = request.get_json()
        is_valid, message = validate_sale_data(data)
        if not is_valid:
            return jsonify({"message": message}), 400

        db = next(get_db())
        sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if not sale:
            logger.warning(f"Sale not found: {sale_id}")
            return jsonify({"message": "Sale not found"}), 404

        sale.total_amount = float(data.get('total_amount', sale.total_amount))
        sale.payment_method = data.get('payment_method', sale.payment_method)
        db.commit()
        logger.info(f"Sale updated: {sale_id}")
        return jsonify({"message": "Sale updated successfully"}), 200
    except ValueError as ve:
        logger.error(f"Validation error updating sale: {str(ve)}")
        return jsonify({"message": f"Validation error: {str(ve)}"}), 400
    except Exception as e:
        logger.error(f"Update sale error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@sales_bp.route('/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    try:
        db = next(get_db())
        sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if not sale:
            logger.warning(f"Sale not found: {sale_id}")
            return jsonify({"message": "Sale not found"}), 404

        db.delete(sale)
        db.commit()
        logger.info(f"Sale deleted: {sale_id}")
        return jsonify({"message": "Sale deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Delete sale error: {str(e)}")
        return jsonify({"message": "Server error"}), 500
