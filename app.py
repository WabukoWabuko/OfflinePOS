from flask import Flask
from routes_auth import auth_bp
from routes_products import products_bp
from routes_sales import sales_bp
from routes_sync import sync_bp
from routes_customers import customers_bp
from database import Base, engine, init_db

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(sync_bp)
app.register_blueprint(customers_bp)

# Initialize database only once at startup
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
