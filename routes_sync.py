import logging
from flask import Blueprint, jsonify
from database import SessionLocal
from models import CachedSale, Sale, SaleItem
from sqlalchemy.orm import Session

sync_bp = Blueprint('sync', __name__, url_prefix='/api/sync')
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@sync_bp.route('/sales', methods=['POST'])
def sync_sales():
    try:
        db = next(get_db())
        cached_sales = db.query(CachedSale).filter(CachedSale.synced == False).all()
        if not cached_sales:
            logger.info("No cached sales to sync")
            return jsonify({"message": "No cached sales to sync"}), 200

        for cached_sale in cached_sales:
            sale = Sale(
                user_id=cached_sale.user_id,
                customer_id=cached_sale.customer_id,
                total_amount=cached_sale.total_amount,
                payment_method=cached_sale.payment_method,
                created_at=cached_sale.created_at
            )
            db.add(sale)
            db.flush()

            # Update cached sale to mark as synced
            cached_sale.synced = True

        db.commit()
        logger.info(f"Synced {len(cached_sales)} sales")
        return jsonify({"message": f"Synced {len(cached_sales)} sales successfully"}), 200
    except Exception as e:
        logger.error(f"Sync sales error: {str(e)}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500
