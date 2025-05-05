import logging
from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Product
from sqlalchemy.orm import Session

products_bp = Blueprint('products', __name__)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@products_bp.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        stock = data.get('stock')
        barcode = data.get('barcode')
        logger.info(f"Creating product: {name}")
        print(f"Creating product: {name}")

        db = next(get_db())
        product = Product(name=name, price=price, stock=stock, barcode=barcode)
        db.add(product)
        db.commit()
        logger.info(f"Product created: {name}")
        print(f"Product created: {name}")
        return jsonify({"message": "Product created successfully", "product_id": product.id}), 201
    except Exception as e:
        logger.error(f"Create product error: {str(e)}")
        print(f"Create product error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@products_bp.route('/products', methods=['GET'])
def get_products():
    try:
        db = next(get_db())
        products = db.query(Product).all()
        product_list = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock, "barcode": p.barcode} for p in products]
        logger.info("Fetched all products")
        print("Fetched all products")
        return jsonify({"products": product_list}), 200
    except Exception as e:
        logger.error(f"Get products error: {str(e)}")
        print(f"Get products error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.get_json()
        db = next(get_db())
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            logger.warning(f"Product not found: {product_id}")
            print(f"Product not found: {product_id}")
            return jsonify({"message": "Product not found"}), 404

        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        product.barcode = data.get('barcode', product.barcode)
        db.commit()
        logger.info(f"Product updated: {product_id}")
        print(f"Product updated: {product_id}")
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        logger.error(f"Update product error: {str(e)}")
        print(f"Update product error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        db = next(get_db())
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            logger.warning(f"Product not found: {product_id}")
            print(f"Product not found: {product_id}")
            return jsonify({"message": "Product not found"}), 404

        db.delete(product)
        db.commit()
        logger.info(f"Product deleted: {product_id}")
        print(f"Product deleted: {product_id}")
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Delete product error: {str(e)}")
        print(f"Delete product error: {str(e)}")
        return jsonify({"message": "Server error"}), 500
