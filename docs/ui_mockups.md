# OfflinePOS UI Mockups Description

This document describes the UI layout for the OfflinePOS system. It’s a guide for creating mockups in Figma (or another tool) to visualize the app before coding. The UI is clean, modern, and optimized for both touch and mouse input. Let’s walk through the key screens!

## 1. Login Screen
- **Purpose**: Let users (cashiers, admins) log in securely.
- **Components**:
  - App logo centered at the top.
  - Username field (text input).
  - Password field (text input, masked).
  - “Login” button (prominent, blue).
  - “Forgot Password?” link (optional, for future implementation).
  - Online/offline status indicator (small icon in top-right: green for online, red for offline).
- **Layout**: Centered card with a subtle shadow, white background (or dark in dark mode), and rounded corners.
- **Notes**: Simple and distraction-free to get users into the app quickly.

## 2. Main Dashboard
- **Purpose**: Central hub for accessing POS features.
- **Components**:
  - **Top Bar**:
    - App name/logo (left).
    - Current user’s name and role (e.g., “John Doe - Cashier”).
    - Online/offline status icon.
    - Logout button.
  - **Sidebar (Left)**:
    - Navigation menu with icons: Sales, Products, Customers, Transactions, Settings.
    - Collapsible for smaller screens.
  - **Main Content Area**:
    - Defaults to Sales screen (see below).
    - Changes based on selected menu item.
- **Layout**: Sidebar on the left, top bar above, and main content filling the rest. Responsive for different screen sizes.
- **Notes**: Clean and intuitive, with quick access to core features.

## 3. Sales Screen
- **Purpose**: Process sales by adding products and completing transactions.
- **Components**:
  - **Left Panel**: Product selection.
    - Search bar (filter by name or barcode).
    - Grid or list of products (name, price, stock).
    - “Scan Barcode” button (for future barcode scanner integration).
  - **Right Panel**: Cart.
    - List of added items (product name, quantity, price, subtotal).
    - Quantity controls (+/- buttons).
    - “Remove Item” button per item.
    - Total amount display.
    - “Apply Discount” button (optional).
    - “Checkout” button (green, prominent).
  - **Footer**: Customer selector (dropdown to pick or add a customer).
- **Layout**: Split layout (left for products, right for cart) with a footer for customer info.
- **Notes**: Optimized for speed, with touch-friendly buttons.

## 4. Products Screen
- **Purpose**: Manage inventory (add, edit, delete products).
- **Components**:
  - Table listing products (columns: ID, Name, Price, Stock, Barcode).
  - “Add Product” button (opens a dialog).
  - “Edit” and “Delete” buttons per row.
  - Search bar to filter products.
  - “Import CSV” and “Export CSV” buttons.
- **Dialog (Add/Edit Product)**:
  - Fields: Name, Price, Stock, Barcode (optional).
  - “Save” and “Cancel” buttons.
- **Layout**: Table-based with action buttons above and dialogs for CRUD operations.
- **Notes**: Admin-only access for editing/deleting.

## 5. Customers Screen
- **Purpose**: Manage customer data for loyalty programs.
- **Components**:
  - Table listing customers (columns: ID, Name, Email, Phone).
  - “Add Customer” button (opens a dialog).
  - “Edit” and “Delete” buttons per row.
  - Search bar to filter customers.
- **Dialog (Add/Edit Customer)**:
  - Fields: Name, Email (optional), Phone (optional).
  - “Save” and “Cancel” buttons.
- **Layout**: Similar to Products screen but with customer-specific fields.
- **Notes**: Optional feature for businesses with loyalty programs.

## 6. Transactions Screen
- **Purpose**: View and filter past sales.
- **Components**:
  - Table listing sales (columns: ID, Date, Cashier, Customer, Total, Payment Method).
  - Filters: Date range, Cashier, Customer.
  - “View Details” button per row (shows sale items and receipt).
  - “Export CSV” button.
- **Layout**: Table-based with filters above.
- **Notes**: Useful for auditing and reporting.

## 7. Settings Screen
- **Purpose**: Configure the app.
- **Components**:
  - Tabs or sections for:
    - **Profile**: Update username, password.
    - **Appearance**: Toggle light/dark theme.
    - **Sync**: Enable/disable cloud sync, set server URL.
    - **Backup**: Create/restore backups.
    - **Branding**: Upload logo, set app name, choose colors.
  - “Save” button for each section.
- **Layout**: Tabbed or accordion-style layout for easy navigation.
- **Notes**: Admin-only for sensitive settings like branding.

## Notes
- **Design Principles**:
  - Use a clean, minimalistic style with plenty of whitespace.
  - Ensure buttons are large enough for touch input.
  - Support light and dark themes (toggle in Settings).
  - Use consistent colors (e.g., blue for primary actions, red for destructive actions).
- **Tools**:
  - Create mockups in Figma, Adobe XD, or Sketch.
  - Export screenshots to include in the `docs/` folder later.
- **Next Steps**:
  - Create mockups based on this description.
  - Review with stakeholders (if any) before coding the UI in F gereki

System: It seems the `ui_mockups.md` artifact was cut off. I'll complete it, ensuring the content is consistent and beginner-friendly, and then proceed with committing the changes to Git. I'll also summarize what we've done in Phase 1 and outline the next steps for moving into Phase 2. Since you're a beginner, I'll keep explanations clear, include Git commands, and ensure files are split appropriately.

---

### Step 6: Complete the UI Mockups Description (Continued)
Let’s finish the `docs/ui_mockups.md` file by completing the "Notes" section and ensuring it’s ready for use as a guide for creating mockups in Figma or another tool.

<xaiArtifact artifact_id="c650708a-bfdf-4f61-bb93-119d892931fe" artifact_version_id="72217b27-f5df-4272-930a-f5e9f33372bf" title="docs/ui_mockups.md" contentType="text/markdown">
# OfflinePOS UI Mockups Description

This document describes the UI layout for the OfflinePOS system. It’s a guide for creating mockups in Figma (or another tool) to visualize the app before coding. The UI is clean, modern, and optimized for both touch and mouse input. Let’s walk through the key screens!

## 1. Login Screen
- **Purpose**: Let users (cashiers, admins) log in securely.
- **Components**:
  - App logo centered at the top.
  - Username field (text input).
  - Password field (text input, masked).
  - “Login” button (prominent, blue).
  - “Forgot Password?” link (optional, for future implementation).
  - Online/offline status indicator (small icon in top-right: green for online, red for offline).
- **Layout**: Centered card with a subtle shadow, white background (or dark in dark mode), and rounded corners.
- **Notes**: Simple and distraction-free to get users into the app quickly.

## 2. Main Dashboard
- **Purpose**: Central hub for accessing POS features.
- **Components**:
  - **Top Bar**:
    - App name/logo (left).
    - Current user’s name and role (e.g., “John Doe - Cashier”).
    - Online/offline status icon.
    - Logout button.
  - **Sidebar (Left)**:
    - Navigation menu with icons: Sales, Products, Customers, Transactions, Settings.
    - Collapsible for smaller screens.
  - **Main Content Area**:
    - Defaults to Sales screen (see below).
    - Changes based on selected menu item.
- **Layout**: Sidebar on the left, top bar above, and main content filling the rest. Responsive for different screen sizes.
- **Notes**: Clean and intuitive, with quick access to core features.

## 3. Sales Screen
- **Purpose**: Process sales by adding products and completing transactions.
- **Components**:
  - **Left Panel**: Product selection.
    - Search bar (filter by name or barcode).
    - Grid or list of products (name, price, stock).
    - “Scan Barcode” button (for future barcode scanner integration).
  - **Right Panel**: Cart.
    - List of added items (product name, quantity, price, subtotal).
    - Quantity controls (+/- buttons).
    - “Remove Item” button per item.
    - Total amount display.
    - “Apply Discount” button (optional).
    - “Checkout” button (green, prominent).
  - **Footer**: Customer selector (dropdown to pick or add a customer).
- **Layout**: Split layout (left for products, right for cart) with a footer for customer info.
- **Notes**: Optimized for speed, with touch-friendly buttons.

## 4. Products Screen
- **Purpose**: Manage inventory (add, edit, delete products).
- **Components**:
  - Table listing products (columns: ID, Name, Price, Stock, Barcode).
  - “Add Product” button (opens a dialog).
  - “Edit” and “Delete” buttons per row.
  - Search bar to filter products.
  - “Import CSV” and “Export CSV” buttons.
- **Dialog (Add/Edit Product)**:
  - Fields: Name, Price, Stock, Barcode (optional).
  - “Save” and “Cancel” buttons.
- **Layout**: Table-based with action buttons above and dialogs for CRUD operations.
- **Notes**: Admin-only access for editing/deleting.

## 5. Customers Screen
- **Purpose**: Manage customer data for loyalty programs.
- **Components**:
  - Table listing customers (columns: ID, Name, Email, Phone).
  - “Add Customer” button (opens a dialog).
  - “Edit” and “Delete” buttons per row.
  - Search bar to filter customers.
- **Dialog (Add/Edit Customer)**:
  - Fields: Name, Email (optional), Phone (optional).
  - “Save” and “Cancel” buttons.
- **Layout**: Similar to Products screen but with customer-specific fields.
- **Notes**: Optional feature for businesses with loyalty programs.

## 6. Transactions Screen
- **Purpose**: View and filter past sales.
- **Components**:
  - Table listing sales (columns: ID, Date, Cashier, Customer, Total, Payment Method).
  - Filters: Date range, Cashier, Customer.
  - “View Details” button per row (shows sale items and receipt).
  - “Export CSV” button.
- **Layout**: Table-based with filters above.
- **Notes**: Useful for auditing and reporting.

## 7. Settings Screen
- **Purpose**: Configure the app.
- **Components**:
  - Tabs or sections for:
    - **Profile**: Update username, password.
    - **Appearance**: Toggle light/dark theme.
    - **Sync**: Enable/disable cloud sync, set server URL.
    - **Backup**: Create/restore backups.
    - **Branding**: Upload logo, set app name, choose colors.
  - “Save” button for each section.
- **Layout**: Tabbed or accordion-style layout for easy navigation.
- **Notes**: Admin-only for sensitive settings like branding.

## Notes
- **Design Principles**:
  - Use a clean, minimalistic style with plenty of whitespace.
  - Ensure buttons are large enough for touch input.
  - Support light and dark themes (toggle in Settings).
  - Use consistent colors (e.g., blue for primary actions, red for destructive actions like delete).
- **Tools**:
  - Create mockups in Figma, Adobe XD, or Sketch.
  - Export screenshots and save them in the `docs/` folder (e.g., `docs/screenshots/`).
  - If you don’t have a design tool, you can sketch on paper and scan/photograph it for reference.
- **Next Steps**:
  - Create mockups based on this description.
  - Share with stakeholders (if any) for feedback.
  - Use the mockups to guide Flet UI development in Phase 2.
  - Update this document with screenshot file paths once mockups are created (e.g., `See docs/screenshots/login.png`).

This description should give you a clear starting point for designing the UI. Let’s make it look sleek and user-friendly!