import logging
from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Customer
from sqlalchemy.orm import Session

customers_bp = Blueprint('customers', __name__, url_prefix='/api/customers')
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_customer_data(data):
    required_fields = {"name"}
    if not all(k in data for k in required_fields):
        return False, "Missing required field: name"
    return True, ""

@customers_bp.route('', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        is_valid, message = validate_customer_data(data)
        if not is_valid:
            logger.warning(f"Create customer failed: {message}")
            return jsonify({"message": message}), 400

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        logger.info(f"Creating customer: {name}")

        db = next(get_db())
        customer = Customer(name=name, email=email, phone=phone)
        db.add(customer)
        db.commit()
        logger.info(f"Customer created: {name}, ID: {customer.id}")
        return jsonify({"message": "Customer created successfully", "customer_id": customer.id}), 201
    except Exception as e:
        logger.error(f"Create customer error: {str(e)}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500

@customers_bp.route('', methods=['GET'])
def get_customers():
    try:
        db = next(get_db())
        customers = db.query(Customer).all()
        customer_list = [{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone} for c in customers]
        logger.info("Fetched all customers")
        return jsonify({"customers": customer_list}), 200
    except Exception as e:
        logger.error(f"Get customers error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        data = request.get_json()
        is_valid, message = validate_customer_data(data)
        if not is_valid:
            logger.warning(f"Update customer failed: {message}")
            return jsonify({"message": message}), 400

        db = next(get_db())
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            logger.warning(f"Customer not found: {customer_id}")
            return jsonify({"message": "Customer not found"}), 404

        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        db.commit()
        logger.info(f"Customer updated: {customer_id}")
        return jsonify({"message": "Customer updated successfully"}), 200
    except Exception as e:
        logger.error(f"Update customer error: {str(e)}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500

@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        db = next(get_db())
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            logger.warning(f"Customer not found: {customer_id}")
            return jsonify({"message": "Customer not found"}), 404

        db.delete(customer)
        db.commit()
        logger.info(f"Customer deleted: {customer_id}")
        return jsonify({"message": "Customer deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Delete customer error: {str(e)}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500
