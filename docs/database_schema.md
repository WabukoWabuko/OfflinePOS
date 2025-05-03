# OfflinePOS SQLite Database Schema

This document outlines the SQLite database schema for the OfflinePOS system. It’s designed to store all data locally for offline use, with a structure that’s simple but flexible enough for our needs. Let’s dive in!

## Overview
- **Database Name**: `offline_pos.db`
- **Storage Location**: Local filesystem or Docker volume.
- **Tables**: Users, Products, Customers, Sales, SaleItems, Settings.
- **Notes**: All tables use auto-incrementing primary keys and include timestamps for tracking changes.

## Tables

### 1. Users
Stores info about users (cashiers, admins) for authentication and role-based access.
- **Columns**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique user ID.
  - `username` (TEXT, UNIQUE, NOT NULL): Login username.
  - `password_hash` (TEXT, NOT NULL): Hashed password for security.
  - `role` (TEXT, NOT NULL): Role (‘admin’ or ‘cashier’).
  - `created_at` (DATETIME, NOT NULL): When the user was created.
  - `updated_at` (DATETIME): When the user was last updated.

### 2. Products
Stores product details for the POS inventory.
- **Columns**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique product ID.
  - `name` (TEXT, NOT NULL): Product name.
  - `price` (REAL, NOT NULL): Price per unit.
  - `stock` (INTEGER, NOT NULL): Current stock quantity.
  - `barcode` (TEXT, UNIQUE): Barcode for scanning (optional).
  - `created_at` (DATETIME, NOT NULL): When the product was added.
  - `updated_at` (DATETIME): When the product was last updated.

### 3. Customers
Stores customer info for loyalty programs and tracking.
- **Columns**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique customer ID.
  - `name` (TEXT, NOT NULL): Customer’s full name.
  - `email` (TEXT, UNIQUE): Customer’s email (optional).
  - `phone` (TEXT): Customer’s phone number (optional).
  - `created_at` (DATETIME, NOT NULL): When the customer was added.
  - `updated_at` (DATETIME): When the customer was last updated.

### 4. Sales
Stores high-level sale records (one sale can have multiple items).
- **Columns**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique sale ID.
  - `user_id` (INTEGER, NOT NULL): ID of the cashier (references Users).
')

System: It looks like the database schema artifact was cut off mid-sentence. I’ll complete the schema for the `Sales` table and add the remaining tables (`SaleItems` and `Settings`) to ensure the document is complete, following the same structure and style. I’ll also proceed with the Git commands to commit the work done so far and provide guidance on setting up the GitHub repository remotely. Since you asked for a beginner-friendly approach, I’ll keep explanations clear and include all necessary steps.

---

### Step 4: Complete the SQLite Database Schema (Continued)
Let’s finish the `database_schema.md` file by completing the `Sales` table and adding the `SaleItems` and `Settings` tables.

<xaiArtifact artifact_id="1123aadb-8a33-4b24-a3c7-8e74385b6d15" artifact_version_id="d2b89b68-fcae-4f83-8d84-5db047a5704f" title="docs/database_schema.md" contentType="text/markdown">
# OfflinePOS SQLite Database Schema

This document outlines the SQLite database schema for the OfflinePOS system. It’s designed to store all data locally for offline use, with a structure that’s simple but flexible enough for our needs. Let’s dive in!

## Overview
- **Database Name**: `offline_pos.db`
- **Storage Location**: Local filesystem or Docker volume.
- **Tables**: Users, Products, Customers, Sales, SaleItems, Settings.
- **Notes**: All tables use auto-incrementing primary keys and include timestamps for tracking changes.

## Tables

### 1. Users
Stores info about users (cashiers, admins) for authentication and role-based access.
- **Columns**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique user ID.
  - `username` (TEXT, UNIQUE, NOT NULL): Login username.
  - `password_hash` (TEXT, NOT NULL): Hashed password for security.
  - `role` (TEXT, NOT NULL): Role (‘admin’ or ‘cashier’).
  - `created_at` (DATETIME, NOT NULL): When the user was created.
  - `updated_at` (DATETIME): When the user was last updated.

### 2. Products
Stores product details for the POS inventory.
- **Columns**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique product ID.
  - `name` (TEXT, NOT NULL): Product name.
  - `price` (REAL, NOT NULL): Price per unit.
  - `stock` (INTEGER, NOT NULL): Current stock quantity.
  - `barcode` (TEXT, UNIQUE): Barcode for scanning (optional).
  - `created_at` (DATETIME, NOT NULL): When the product was added.
  - `updated_at` (DATETIME): When the product was last updated.

### 3. Customers
Stores customer info for loyalty programs and tracking.
- **Columns**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique customer ID.
  - `name` (TEXT, NOT NULL): Customer’s full name.
  - `email` (TEXT, UNIQUE): Customer’s email (optional).
  - `phone` (TEXT): Customer’s phone number (optional).
  - `created_at` (DATETIME, NOT NULL): When the customer was added.
  - `updated_at` (DATETIME): When the customer was last updated.

### 4. Sales
Stores high-level sale records (one sale can have multiple items).
- **Columns**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique sale ID.
  - `user_id` (INTEGER, NOT NULL): ID of the cashier (references Users).
  - `customer_id` (INTEGER): ID of the customer (references Customers, optional).
  - `total_amount` (REAL, NOT NULL): Total sale amount (after discounts).
  - `payment_method` (TEXT, NOT NULL): Payment type (‘cash’, ‘card’).
  - `created_at` (DATETIME, NOT NULL): When the sale was made.

### 5. SaleItems
Stores individual items within a sale (e.g., multiple products in one transaction).
- **Columns**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique sale item ID.
  - `sale_id` (INTEGER, NOT NULL): ID of the sale (references Sales).
  - `product_id` (INTEGER, NOT NULL): ID of the product (references Products).
  - `quantity` (INTEGER, NOT NULL): Number of units sold.
  - `unit_price` (REAL, NOT NULL): Price per unit at the time of sale.
  - `created_at` (DATETIME, NOT NULL): When the item was added to the sale.

### 6. Settings
Stores app-wide settings (e.g., theme, sync preferences).
- **Columns**:
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique setting ID.
  - `key` (TEXT, UNIQUE, NOT NULL): Setting name (e.g., ‘theme’, ‘sync_enabled’).
  - `value` (TEXT, NOT NULL): Setting value (e.g., ‘dark’, ‘true’).
  - `updated_at` (DATETIME): When the setting was last updated.

## Notes
- **Foreign Keys**: `user_id` (Sales), `customer_id` (Sales), `sale_id` (SaleItems), and `product_id` (SaleItems) reference their respective tables to maintain data integrity.
- **Timestamps**: `created_at` and `updated_at` help track changes for sync and auditing.
- **Cloud Sync**: This schema will map to a PostgreSQL database for cloud storage, with similar structure but additional fields for sync metadata (to be designed later).

This schema gives us a solid foundation for the POS system. Next, we’ll implement it in SQLite during development!