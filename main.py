import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# =========================
# APP SETTINGS
# =========================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Inventory Sales System")
app.geometry("1200x700")
app.minsize(1000, 600)

# =========================
# COLORS
# =========================
DARK_BLUE = "#015A84"
MID_BLUE = "#0B719E"
LIGHT_BLUE = "#D8EAF2"
VERY_LIGHT_BLUE = "#EEF7FA"
WHITE = "#FFFFFF"
TEXT = "#064B6B"
GREEN = "#27AE60"
RED = "#E74C3C"
GRAY = "#6B7280"

# =========================
# MYSQL CONNECTION
# =========================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="vincecandil!2003",
        database="inventory_system"
    )
# =========================
# LOAD PRODUCTS FROM MYSQL
# =========================
def load_products_from_db():
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            SELECT product_id, product_name, category, price, stock, status
            FROM products
        """)

        rows = cursor.fetchall()

        cursor.close()
        db.close()

        return [
            (
                row[0],
                row[1],
                row[2],
                f"₱{float(row[3]):,.2f}",
                str(row[4]),
                row[5]
            )
            for row in rows
        ]

    except mysql.connector.Error as err:
        print("Error loading products:", err)
        return []
    
# =========================
# PRODUCT DATA
# =========================
products = load_products_from_db()




# =========================
# CLEAR SCREEN
# =========================
def clear_screen():
    for widget in app.winfo_children():
        widget.destroy()


# =========================
# DASHBOARD
# =========================
def show_dashboard():
    clear_screen()

    # Get latest products from MySQL
    global products
    products = load_products_from_db()

    # Get sales summary
    total_transactions, total_sales = get_sales_summary()

    # -------------------------
    # MAIN BACKGROUND
    # -------------------------
    main = ctk.CTkFrame(
        app,
        fg_color="#071A2B",
        corner_radius=0
    )
    main.pack(fill="both", expand=True)

    # -------------------------
    # SIDEBAR
    # -------------------------
    sidebar = ctk.CTkFrame(
        main,
        width=230,
        corner_radius=0,
        fg_color="#061525"
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Logo
    logo_frame = ctk.CTkFrame(
        sidebar,
        fg_color="transparent"
    )
    logo_frame.pack(fill="x", pady=(25, 20))

    logo_icon = ctk.CTkLabel(
        logo_frame,
        text="▣",
        font=("Arial", 28, "bold"),
        text_color="#2F80FF"
    )
    logo_icon.pack()

    logo_title = ctk.CTkLabel(
        logo_frame,
        text="Inventory and Sales\nManagement System",
        font=("Arial", 13, "bold"),
        text_color=WHITE,
        justify="center"
    )
    logo_title.pack(pady=(5, 0))

    # -------------------------
    # MENU
    # -------------------------
    menu_title = ctk.CTkLabel(
        sidebar,
        text="MAIN MENU",
        font=("Arial", 11, "bold"),
        text_color="#718096"
    )
    menu_title.pack(anchor="w", padx=25, pady=(10, 10))

    # Dashboard
    dashboard_btn = ctk.CTkButton(
        sidebar,
        text="  Dashboard",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="#1769E0",
        hover_color="#1769E0",
        text_color=WHITE,
        font=("Arial", 13, "bold"),
        anchor="w",
        command=show_dashboard
    )
    dashboard_btn.pack(pady=4)

    # Products
    products_btn = ctk.CTkButton(
        sidebar,
        text="  Products",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_products
    )
    products_btn.pack(pady=4)

    # Inventory
    inventory_btn = ctk.CTkButton(
        sidebar,
        text="  Inventory",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_inventory
    )
    inventory_btn.pack(pady=4)

    # Sales
    sales_btn = ctk.CTkButton(
        sidebar,
        text="  Sales",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_sales
    )
    sales_btn.pack(pady=4)

    # Reports
    reports_btn = ctk.CTkButton(
        sidebar,
        text="  Reports",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_reports
    )
    reports_btn.pack(pady=4)

    # -------------------------
    # LOGOUT
    # -------------------------
    logout_btn = ctk.CTkButton(
        sidebar,
        text="  Logout",
        width=190,
        height=40,
        corner_radius=8,
        fg_color="#C0392B",
        hover_color="#962D22",
        text_color=WHITE,
        font=("Arial", 13, "bold"),
        anchor="w",
        command=show_login
    )
    logout_btn.pack(
        side="bottom",
        pady=25,
        padx=20
    )

    # -------------------------
    # CONTENT AREA
    # -------------------------
    content = ctk.CTkFrame(
        main,
        fg_color="#071A2B",
        corner_radius=0
    )
    content.pack(
        side="right",
        fill="both",
        expand=True
    )

    # -------------------------
    # TOP HEADER
    # -------------------------
    header = ctk.CTkFrame(
        content,
        height=65,
        fg_color="#081E32",
        corner_radius=0
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    # Search bar
    search_box = ctk.CTkEntry(
        header,
        width=300,
        height=36,
        corner_radius=8,
        fg_color="#102D47",
        border_width=0,
        text_color=WHITE,
        placeholder_text="Search anything...",
        placeholder_text_color="#718096"
    )
    search_box.pack(
        side="left",
        padx=25,
        pady=14
    )

    # Admin
    admin_label = ctk.CTkLabel(
        header,
        text="●  Admin  ▾",
        font=("Arial", 13, "bold"),
        text_color=WHITE
    )
    admin_label.pack(
        side="right",
        padx=30
    )

    # -------------------------
    # DASHBOARD CONTENT
    # -------------------------
    dashboard_content = ctk.CTkFrame(
        content,
        fg_color="transparent"
    )
    dashboard_content.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=25
    )

    # Title
    title = ctk.CTkLabel(
        dashboard_content,
        text="Dashboard",
        font=("Arial", 30, "bold"),
        text_color=WHITE
    )
    title.pack(anchor="w")

    subtitle = ctk.CTkLabel(
        dashboard_content,
        text="Overview of your inventory and sales",
        font=("Arial", 13),
        text_color="#718096"
    )
    subtitle.pack(anchor="w", pady=(3, 25))

    # -------------------------
    # STATISTICS
    # -------------------------
    total_products = len(products)

    total_stock = sum(
        int(product[4])
        for product in products
    )

    low_stock = sum(
        1
        for product in products
        if int(product[4]) <= 5
    )

    cards_frame = ctk.CTkFrame(
        dashboard_content,
        fg_color="transparent"
    )
    cards_frame.pack(
        fill="x",
        pady=(0, 20)
    )

    # -------------------------
    # CARD FUNCTION
    # -------------------------
    def create_card(parent, title_text, value_text, value_color):
        card = ctk.CTkFrame(
            parent,
            height=125,
            fg_color="#0B243A",
            corner_radius=12,
            border_width=1,
            border_color="#153A56"
        )
        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )
        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title_text,
            font=("Arial", 13, "bold"),
            text_color="#8FA3B8"
        )
        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value_text,
            font=("Arial", 27, "bold"),
            text_color=value_color
        )
        value_label.pack(
            anchor="w",
            padx=20
        )

        return card

    # Cards
    create_card(
        cards_frame,
        "Total Products",
        str(total_products),
        "#2F80FF"
    )

    create_card(
        cards_frame,
        "Total Stock",
        str(total_stock),
        "#27AE60"
    )

    create_card(
        cards_frame,
        "Low Stock",
        str(low_stock),
        "#F2A900"
    )

    create_card(
        cards_frame,
        "Total Sales",
        f"₱{float(total_sales):,.2f}",
        "#A855F7"
    )

    # -------------------------
    # LOWER DASHBOARD AREA
    # -------------------------
    lower_frame = ctk.CTkFrame(
        dashboard_content,
        fg_color="transparent"
    )
    lower_frame.pack(
        fill="both",
        expand=True
    )

    # Sales Overview
    sales_overview = ctk.CTkFrame(
        lower_frame,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    sales_overview.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(6, 10)
    )

    ctk.CTkLabel(
        sales_overview,
        text="Sales Overview",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 5)
    )

    ctk.CTkLabel(
        sales_overview,
        text="Current sales activity",
        font=("Arial", 12),
        text_color="#718096"
    ).pack(
        anchor="w",
        padx=20
    )

    # Sales information
    sales_info = ctk.CTkFrame(
        sales_overview,
        fg_color="#102D47",
        corner_radius=10
    )
    sales_info.pack(
        fill="x",
        padx=20,
        pady=20
    )

    ctk.CTkLabel(
        sales_info,
        text="Total Transactions",
        font=("Arial", 12),
        text_color="#8FA3B8"
    ).pack(
        anchor="w",
        padx=15,
        pady=(15, 3)
    )

    ctk.CTkLabel(
        sales_info,
        text=str(total_transactions),
        font=("Arial", 24, "bold"),
        text_color="#2F80FF"
    ).pack(
        anchor="w",
        padx=15,
        pady=(0, 15)
    )

    ctk.CTkLabel(
        sales_overview,
        text="Manage your sales and view transaction history.",
        font=("Arial", 12),
        text_color="#8FA3B8"
    ).pack(
        anchor="w",
        padx=20,
        pady=5
    )

    view_sales_btn = ctk.CTkButton(
        sales_overview,
        text="View Sales",
        width=140,
        height=38,
        corner_radius=8,
        fg_color="#1769E0",
        hover_color="#1255B5",
        text_color=WHITE,
        font=("Arial", 12, "bold"),
        command=show_sales
    )
    view_sales_btn.pack(
        anchor="w",
        padx=20,
        pady=20
    )

    # -------------------------
    # INVENTORY OVERVIEW
    # -------------------------
    inventory_overview = ctk.CTkFrame(
        lower_frame,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    inventory_overview.pack(
        side="right",
        fill="both",
        expand=True,
        padx=(10, 6)
    )

    ctk.CTkLabel(
        inventory_overview,
        text="Inventory Status",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 5)
    )

    ctk.CTkLabel(
        inventory_overview,
        text="Current stock condition",
        font=("Arial", 12),
        text_color="#718096"
    ).pack(
        anchor="w",
        padx=20
    )

    # Available
    available_count = total_products - low_stock

    available_frame = ctk.CTkFrame(
        inventory_overview,
        fg_color="#102D47",
        corner_radius=10
    )
    available_frame.pack(
        fill="x",
        padx=20,
        pady=(20, 8)
    )

    ctk.CTkLabel(
        available_frame,
        text="Available Products",
        font=("Arial", 12),
        text_color="#8FA3B8"
    ).pack(
        side="left",
        padx=15,
        pady=15
    )

    ctk.CTkLabel(
        available_frame,
        text=str(available_count),
        font=("Arial", 20, "bold"),
        text_color="#27AE60"
    ).pack(
        side="right",
        padx=15
    )

    # Low stock
    low_frame = ctk.CTkFrame(
        inventory_overview,
        fg_color="#102D47",
        corner_radius=10
    )
    low_frame.pack(
        fill="x",
        padx=20,
        pady=8
    )

    ctk.CTkLabel(
        low_frame,
        text="Needs Attention",
        font=("Arial", 12),
        text_color="#8FA3B8"
    ).pack(
        side="left",
        padx=15,
        pady=15
    )

    ctk.CTkLabel(
        low_frame,
        text=str(low_stock),
        font=("Arial", 20, "bold"),
        text_color="#F2A900"
    ).pack(
        side="right",
        padx=15
    )

    inventory_btn2 = ctk.CTkButton(
        inventory_overview,
        text="View Inventory",
        width=140,
        height=38,
        corner_radius=8,
        fg_color="#1769E0",
        hover_color="#1255B5",
        text_color=WHITE,
        font=("Arial", 12, "bold"),
        command=show_inventory
    )
    inventory_btn2.pack(
        anchor="w",
        padx=20,
        pady=20
    )

# =========================
# ADD PRODUCT FUNCTION
# =========================
def add_product():

    add_window = ctk.CTkToplevel(app)
    add_window.title("Add Product")
    add_window.geometry("450x550")
    add_window.resizable(False, False)

    title = ctk.CTkLabel(
        add_window,
        text="Add New Product",
        font=("Arial", 24, "bold"),
        text_color=DARK_BLUE
    )
    title.pack(pady=(30, 20))

    # Product Name
    name_label = ctk.CTkLabel(
        add_window,
        text="Product Name",
        font=("Arial", 13, "bold")
    )
    name_label.pack(anchor="w", padx=40)

    name_entry = ctk.CTkEntry(
        add_window,
        width=370,
        height=40,
        placeholder_text="Enter product name"
    )
    name_entry.pack(pady=(5, 15))

    # Category
    category_label = ctk.CTkLabel(
        add_window,
        text="Category",
        font=("Arial", 13, "bold")
    )
    category_label.pack(anchor="w", padx=40)

    category_entry = ctk.CTkEntry(
        add_window,
        width=370,
        height=40,
        placeholder_text="Enter category"
    )
    category_entry.pack(pady=(5, 15))

    # Price
    price_label = ctk.CTkLabel(
        add_window,
        text="Price",
        font=("Arial", 13, "bold")
    )
    price_label.pack(anchor="w", padx=40)

    price_entry = ctk.CTkEntry(
        add_window,
        width=370,
        height=40,
        placeholder_text="Enter price"
    )
    price_entry.pack(pady=(5, 15))

    # Stock
    stock_label = ctk.CTkLabel(
        add_window,
        text="Stock",
        font=("Arial", 13, "bold")
    )
    stock_label.pack(anchor="w", padx=40)

    stock_entry = ctk.CTkEntry(
        add_window,
        width=370,
        height=40,
        placeholder_text="Enter stock quantity"
    )
    stock_entry.pack(pady=(5, 15))

    # Error Message
    error_label = ctk.CTkLabel(
        add_window,
        text="",
        font=("Arial", 12),
        text_color=RED
    )
    error_label.pack(pady=5)

    # =========================
    # SAVE PRODUCT
    # =========================
    def save_product():

        name = name_entry.get().strip()
        category = category_entry.get().strip()
        price = price_entry.get().strip()
        stock = stock_entry.get().strip()

        if not name or not category or not price or not stock:
            error_label.configure(
                text="Please fill in all fields."
            )
            return

        try:
            price_value = float(price)
        except ValueError:
            error_label.configure(
                text="Price must be a number."
            )
            return

        try:
            stock_value = int(stock)
        except ValueError:
            error_label.configure(
                text="Stock must be a whole number."
            )
            return

        if stock_value <= 5:
            status = "Low Stock"
        else:
            status = "Available"

        try:
            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                SELECT COUNT(*) FROM products
                """
            )

            count = cursor.fetchone()[0]
            product_id = f"P{count + 1:03d}"

            cursor.execute(
                """
                INSERT INTO products
                (product_id, product_name, category, price, stock, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    product_id,
                    name,
                    category,
                    price_value,
                    stock_value,
                    status
                )
            )

            db.commit()

            cursor.close()
            db.close()

            add_window.destroy()

            global products
            products = load_products_from_db()

            show_products()

        except mysql.connector.Error as err:
            error_label.configure(
                text=f"Database error: {err}"
            )
       

    # Save Button
    save_button = ctk.CTkButton(
        add_window,
        text="Save Product",
        width=170,
        height=40,
        fg_color=DARK_BLUE,
        hover_color=MID_BLUE,
        command=save_product
    )
    save_button.pack(pady=10)

    # Cancel Button
    cancel_button = ctk.CTkButton(
        add_window,
        text="Cancel",
        width=170,
        height=40,
        fg_color=GRAY,
        hover_color="#555555",
        command=add_window.destroy
    )
    cancel_button.pack(pady=5)

# =========================
# EDIT PRODUCT
# =========================
def edit_product(index):

    product = products[index]

    edit_window = ctk.CTkToplevel(app)
    edit_window.title("Edit Product")
    edit_window.geometry("450x500")
    edit_window.resizable(False, False)

    title = ctk.CTkLabel(
        edit_window,
        text="Edit Product",
        font=("Arial", 24, "bold"),
        text_color=DARK_BLUE
    )
    title.pack(pady=(25, 20))

    id_label = ctk.CTkLabel(
        edit_window,
        text=f"Product ID: {product[0]}",
        font=("Arial", 13),
        text_color=TEXT
    )
    id_label.pack(pady=5)

    name_entry = ctk.CTkEntry(
        edit_window,
        width=320,
        height=40,
        placeholder_text="Product Name"
    )
    name_entry.pack(pady=8)
    name_entry.insert(0, product[1])

    category_entry = ctk.CTkEntry(
        edit_window,
        width=320,
        height=40,
        placeholder_text="Category"
    )
    category_entry.pack(pady=8)
    category_entry.insert(0, product[2])

    price_entry = ctk.CTkEntry(
        edit_window,
        width=320,
        height=40,
        placeholder_text="Price"
    )
    price_entry.pack(pady=8)
    price_entry.insert(0, product[3].replace("₱", ""))

    stock_entry = ctk.CTkEntry(
        edit_window,
        width=320,
        height=40,
        placeholder_text="Stock"
    )
    stock_entry.pack(pady=8)
    stock_entry.insert(0, product[4])

    def update_product():

        name = name_entry.get().strip()
        category = category_entry.get().strip()
        price = price_entry.get().strip()
        stock = stock_entry.get().strip()

        if not name or not category or not price or not stock:
            return

        try:
            price_value = float(price)
            stock_value = int(stock)
        except ValueError:
            return

        if stock_value <= 5:
            status = "Low Stock"
        else:
            status = "Available"

        db = None
        cursor = None

        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(
                """
                UPDATE products
                SET product_name = %s,
                    category = %s,
                    price = %s,
                    stock = %s,
                    status = %s
                WHERE product_id = %s
                """,
                (
                    name,
                    category,
                    price_value,
                    stock_value,
                    status,
                    product[0]
                )
            )

            db.commit()

            print("Updated rows:", cursor.rowcount)

            global products
            products = load_products_from_db()

            edit_window.destroy()
            show_products()

        except mysql.connector.Error as err:
            print("Database error:", err)

    update_button = ctk.CTkButton(
        edit_window,
        text="Update Product",
        width=180,
        height=40,
        fg_color=DARK_BLUE,
        hover_color=MID_BLUE,
        command=update_product
    )
    update_button.pack(pady=20)


# =========================
# DELETE PRODUCT
# =========================
def delete_product(index):

    product = products[index]

    confirm_window = ctk.CTkToplevel(app)
    confirm_window.title("Delete Product")
    confirm_window.geometry("400x220")
    confirm_window.resizable(False, False)

    message = ctk.CTkLabel(
        confirm_window,
        text=f"Delete {product[1]}?",
        font=("Arial", 18, "bold"),
        text_color=TEXT
    )
    message.pack(pady=(35, 10))

    warning = ctk.CTkLabel(
        confirm_window,
        text="This action cannot be undone.",
        font=("Arial", 12),
        text_color=GRAY
    )
    warning.pack(pady=5)

    button_frame = ctk.CTkFrame(
        confirm_window,
        fg_color="transparent"
    )
    button_frame.pack(pady=20)

    def confirm_delete():

        db = None
        cursor = None

        try:
            print("DELETE PRODUCT CLICKED")
            print("ID:", product[0])

            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                DELETE FROM products
                WHERE product_id = %s
                """,
                (product[0],)
            )

            print("Rows deleted:", cursor.rowcount)

            db.commit()

            print("MySQL DELETE committed successfully")

            global products
            products = load_products_from_db()

            confirm_window.destroy()
            show_products()

        except mysql.connector.Error as err:
            print("Database error:", err)

        finally:
            if cursor is not None:
                cursor.close()

            if db is not None:
                db.close()

    delete_button = ctk.CTkButton(
        button_frame,
        text="Delete",
        width=100,
        height=35,
        fg_color=RED,
        hover_color="#C0392B",
        command=confirm_delete
    )
    delete_button.pack(side="left", padx=8)

    cancel_button = ctk.CTkButton(
        button_frame,
        text="Cancel",
        width=100,
        height=35,
        fg_color=GRAY,
        hover_color="#555555",
        command=confirm_window.destroy
    )
    cancel_button.pack(side="left", padx=8)
    

# =========================
# EDIT PRODUCT BY ID
# =========================
def edit_product_by_id(product_id):

    for index, product in enumerate(products):

        if product[0] == product_id:
            edit_product(index)
            return


# =========================
# DELETE PRODUCT BY ID
# =========================
def delete_product_by_id(product_id):

    for index, product in enumerate(products):

        if product[0] == product_id:
            delete_product(index)
            return



# =========================
# SEARCH PRODUCTS
# =========================
def search_products(search_text):

    search_text = search_text.lower().strip()

    if not search_text:
        show_products()
        return

    filtered_products = [
        product for product in products
        if search_text in product[0].lower()
        or search_text in product[1].lower()
        or search_text in product[2].lower()
    ]

    show_products(filtered_products)

# =========================
# LOW STOCK PRODUCTS
# =========================
def show_low_stock():

    low_stock_products = [
        product for product in products
        if int(product[4]) <= 5
    ]
    

    show_products(low_stock_products)
def restock_product(product_id, product_name, current_stock):

    restock_window = ctk.CTkToplevel(app)
    restock_window.title("Restock Product")
    restock_window.geometry("400x300")
    restock_window.resizable(False, False)

    ctk.CTkLabel(
        restock_window,
        text="RESTOCK PRODUCT",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    ctk.CTkLabel(
        restock_window,
        text=f"{product_name}\nCurrent Stock: {current_stock}",
        font=("Arial", 15)
    ).pack(pady=10)

    quantity_entry = ctk.CTkEntry(
        restock_window,
        width=250,
        height=40,
        placeholder_text="Enter quantity to add"
    )
    quantity_entry.pack(pady=15)

    def save_restock():

        try:
            quantity = int(quantity_entry.get())

            if quantity <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Please enter a valid positive number."
            )
            return

        new_stock = current_stock + quantity

        if new_stock <= 5:
            status = "Low Stock"
        else:
            status = "Available"

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE products
                SET stock = %s,
                    status = %s
                WHERE product_id = %s
                """,
                (new_stock, status, product_id)
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Restock Successful",
                f"{product_name} stock updated!\n\n"
                f"Previous Stock: {current_stock}\n"
                f"Added: {quantity}\n"
                f"New Stock: {new_stock}"
            )

            restock_window.destroy()
            show_inventory()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Failed to update stock:\n{error}"
            )

    ctk.CTkButton(
        restock_window,
        text="SAVE RESTOCK",
        width=250,
        height=40,
        command=save_restock
    ).pack(pady=10)

    # =========================
# DEDUCT STOCK
# =========================
def deduct_stock(product_id, product_name, current_stock):

    deduct_window = ctk.CTkToplevel(app)
    deduct_window.title("Deduct Stock")
    deduct_window.geometry("400x300")
    deduct_window.resizable(False, False)

    ctk.CTkLabel(
        deduct_window,
        text="DEDUCT STOCK",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    ctk.CTkLabel(
        deduct_window,
        text=f"{product_name}\nCurrent Stock: {current_stock}",
        font=("Arial", 15)
    ).pack(pady=10)

    quantity_entry = ctk.CTkEntry(
        deduct_window,
        width=250,
        height=40,
        placeholder_text="Enter quantity to deduct"
    )
    quantity_entry.pack(pady=15)

    def save_deduct():

        try:
            quantity = int(quantity_entry.get())

            if quantity <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Please enter a valid positive number."
            )
            return

        if quantity > current_stock:
            messagebox.showerror(
                "Insufficient Stock",
                f"Cannot deduct {quantity}.\n\n"
                f"Current Stock: {current_stock}"
            )
            return

        new_stock = current_stock - quantity

        if new_stock <= 5:
            status = "Low Stock"
        else:
            status = "Available"

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE products
                SET stock = %s,
                    status = %s
                WHERE product_id = %s
                """,
                (new_stock, status, product_id)
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Stock Deducted",
                f"{product_name} stock updated!\n\n"
                f"Previous Stock: {current_stock}\n"
                f"Deducted: {quantity}\n"
                f"New Stock: {new_stock}"
            )

            deduct_window.destroy()
            show_inventory()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Failed to update stock:\n{error}"
            )

    ctk.CTkButton(
        deduct_window,
        text="DEDUCT STOCK",
        width=250,
        height=40,
        fg_color=RED,
        hover_color="#C0392B",
        command=save_deduct
    ).pack(pady=10)
# =========================
# INVENTORY
# =========================
def show_inventory():

    clear_screen()

    global products
    products = load_products_from_db()

    # =========================
    # MAIN BACKGROUND
    # =========================
    main = ctk.CTkFrame(
        app,
        fg_color="#071A2B",
        corner_radius=0
    )
    main.pack(fill="both", expand=True)

    # =========================
    # SIDEBAR
    # =========================
    sidebar = ctk.CTkFrame(
        main,
        width=230,
        corner_radius=0,
        fg_color="#061525"
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Logo
    ctk.CTkLabel(
        sidebar,
        text="▣",
        font=("Arial", 28, "bold"),
        text_color="#2F80FF"
    ).pack(pady=(25, 5))

    ctk.CTkLabel(
        sidebar,
        text="Inventory and Sales\nManagement System",
        font=("Arial", 13, "bold"),
        text_color=WHITE,
        justify="center"
    ).pack(pady=(0, 25))

    # =========================
    # MENU
    # =========================
    ctk.CTkLabel(
        sidebar,
        text="MAIN MENU",
        font=("Arial", 11, "bold"),
        text_color="#718096"
    ).pack(
        anchor="w",
        padx=25,
        pady=(5, 10)
    )

    # Dashboard
    ctk.CTkButton(
        sidebar,
        text="  Dashboard",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_dashboard
    ).pack(pady=4)

    # Products
    ctk.CTkButton(
        sidebar,
        text="  Products",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_products
    ).pack(pady=4)

    # Inventory - ACTIVE
    ctk.CTkButton(
        sidebar,
        text="  Inventory",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="#1769E0",
        hover_color="#1769E0",
        text_color=WHITE,
        font=("Arial", 13, "bold"),
        anchor="w",
        command=show_inventory
    ).pack(pady=4)

    # Sales
    ctk.CTkButton(
        sidebar,
        text="  Sales",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_sales
    ).pack(pady=4)

    # Reports
    ctk.CTkButton(
        sidebar,
        text="  Reports",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_reports
    ).pack(pady=4)

    # Logout
    ctk.CTkButton(
        sidebar,
        text="  Logout",
        width=190,
        height=40,
        corner_radius=8,
        fg_color="#C0392B",
        hover_color="#962D22",
        text_color=WHITE,
        font=("Arial", 13, "bold"),
        anchor="w",
        command=show_login
    ).pack(
        side="bottom",
        pady=25,
        padx=20
    )

    # =========================
    # CONTENT
    # =========================
    content = ctk.CTkFrame(
        main,
        fg_color="#071A2B",
        corner_radius=0
    )
    content.pack(
        side="right",
        fill="both",
        expand=True
    )

    # =========================
    # TOP HEADER
    # =========================
    header = ctk.CTkFrame(
        content,
        height=65,
        fg_color="#081E32",
        corner_radius=0
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    ctk.CTkLabel(
        header,
        text="Inventory Management",
        font=("Arial", 16, "bold"),
        text_color=WHITE
    ).pack(
        side="left",
        padx=25
    )

    ctk.CTkLabel(
        header,
        text="●  Admin",
        font=("Arial", 13, "bold"),
        text_color=WHITE
    ).pack(
        side="right",
        padx=30
    )

    # =========================
    # CONTENT AREA
    # =========================
    content_area = ctk.CTkFrame(
        content,
        fg_color="transparent"
    )
    content_area.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=25
    )

    # Title
    ctk.CTkLabel(
        content_area,
        text="Inventory",
        font=("Arial", 30, "bold"),
        text_color=WHITE
    ).pack(anchor="w")

    ctk.CTkLabel(
        content_area,
        text="Monitor and manage your stock levels",
        font=("Arial", 13),
        text_color="#718096"
    ).pack(
        anchor="w",
        pady=(3, 20)
    )

    # =========================
    # INVENTORY TABLE
    # =========================
    table = ctk.CTkFrame(
        content_area,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    table.pack(
        fill="both",
        expand=True
    )

    # Table Title
    ctk.CTkLabel(
        table,
        text="Inventory List",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    # Table Header
    table_header = ctk.CTkFrame(
        table,
        fg_color="#102D47",
        height=45,
        corner_radius=6
    )
    table_header.pack(
        fill="x",
        padx=15,
        pady=(0, 8)
    )

    headers = [
        "Product ID",
        "Product Name",
        "Category",
        "Stock",
        "Status",
        "Action"
    ]

    widths = [100, 190, 150, 80, 110, 180]

    for i, header_text in enumerate(headers):

        ctk.CTkLabel(
            table_header,
            text=header_text,
            width=widths[i],
            anchor="w",
            font=("Arial", 11, "bold"),
            text_color="#8FA3B8"
        ).grid(
            row=0,
            column=i,
            padx=8,
            pady=8,
            sticky="w"
        )

    
    # =========================
    # SCROLLABLE INVENTORY AREA
    # =========================
    inventory_scroll = ctk.CTkScrollableFrame(
        table,
        fg_color="transparent",
        corner_radius=6,
        height=400
    )
    inventory_scroll.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 10)
    )

    
    # =========================
    # PRODUCT ROWS
    # =========================
    for product in products:

        row = ctk.CTkFrame(
            inventory_scroll,
            fg_color="#0E2A42",
            corner_radius=6,
            height=55
        )
        row.pack(
            fill="x",
            padx=15,
            pady=3
        )
        row.pack_propagate(False)

        # Product ID
        ctk.CTkLabel(
            row,
            text=str(product[0]),
            width=100,
            anchor="w",
            text_color=WHITE
        ).pack(
            side="left",
            padx=8
        )

        # Product Name
        ctk.CTkLabel(
            row,
            text=str(product[1]),
            width=190,
            anchor="w",
            text_color=WHITE
        ).pack(
            side="left",
            padx=8
        )

        # Category
        ctk.CTkLabel(
            row,
            text=str(product[2]),
            width=150,
            anchor="w",
            text_color=WHITE
        ).pack(
            side="left",
            padx=8
        )

        # Stock
        ctk.CTkLabel(
            row,
            text=str(product[4]),
            width=80,
            anchor="w",
            text_color=WHITE
        ).pack(
            side="left",
            padx=8
        )

        # Status
        status_color = (
            "#F2A900"
            if str(product[5]) == "Low Stock"
            else "#27AE60"
        )

        ctk.CTkLabel(
            row,
            text=str(product[5]),
            width=110,
            anchor="w",
            text_color=status_color
        ).pack(
            side="left",
            padx=8
        )

        # =========================
        # ACTION BUTTONS
        # =========================
        action_frame = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )
        action_frame.pack(
            side="right",
            padx=8
        )

        # Restock
        ctk.CTkButton(
            action_frame,
            text="Restock",
            width=75,
            height=30,
            corner_radius=6,
            fg_color="#27AE60",
            hover_color="#1E8449",
            text_color=WHITE,
            font=("Arial", 11, "bold"),
            command=lambda p_id=product[0],
                           p_name=product[1],
                           stock=int(product[4]):
                           restock_product(
                               p_id,
                               p_name,
                               stock
                           )
        ).pack(
            side="left",
            padx=3
        )

        # Deduct
        ctk.CTkButton(
            action_frame,
            text="Deduct",
            width=75,
            height=30,
            corner_radius=6,
            fg_color="#C0392B",
            hover_color="#962D22",
            text_color=WHITE,
            font=("Arial", 11, "bold"),
            command=lambda p_id=product[0],
                           p_name=product[1],
                           stock=int(product[4]):
                           deduct_stock(
                               p_id,
                               p_name,
                               stock
                           )
        ).pack(
            side="left",
            padx=3
        )


 # =========================
# PRODUCTS
# =========================
def show_products(display_products=None):

    clear_screen()

    global products
    products = load_products_from_db()

    # Use filtered products if provided
    current_products = (
        display_products
        if display_products is not None
        else products
    )
    print("CURRENT PRODUCTS:", current_products)


    # =========================
    # MAIN BACKGROUND
    # =========================
    main = ctk.CTkFrame(
        app,
        fg_color="#071A2B",
        corner_radius=0
    )
    main.pack(fill="both", expand=True)

    # =========================
    # SIDEBAR
    # =========================
    sidebar = ctk.CTkFrame(
        main,
        width=230,
        corner_radius=0,
        fg_color="#061525"
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Logo
    ctk.CTkLabel(
        sidebar,
        text="▣",
        font=("Arial", 28, "bold"),
        text_color="#2F80FF"
    ).pack(pady=(25, 5))

    ctk.CTkLabel(
        sidebar,
        text="Inventory and Sales\nManagement System",
        font=("Arial", 13, "bold"),
        text_color=WHITE,
        justify="center"
    ).pack(pady=(0, 25))

    # Menu
    ctk.CTkLabel(
        sidebar,
        text="MAIN MENU",
        font=("Arial", 11, "bold"),
        text_color="#718096"
    ).pack(
        anchor="w",
        padx=25,
        pady=(5, 10)
    )

    # Dashboard
    ctk.CTkButton(
        sidebar,
        text="  Dashboard",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_dashboard
    ).pack(pady=4)

    # Products - ACTIVE
    ctk.CTkButton(
        sidebar,
        text="  Products",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="#1769E0",
        hover_color="#1769E0",
        text_color=WHITE,
        font=("Arial", 13, "bold"),
        anchor="w",
        command=show_products
    ).pack(pady=4)

    # Inventory
    ctk.CTkButton(
        sidebar,
        text="  Inventory",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_inventory
    ).pack(pady=4)

    # Sales
    ctk.CTkButton(
        sidebar,
        text="  Sales",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_sales
    ).pack(pady=4)

    # Reports
    ctk.CTkButton(
        sidebar,
        text="  Reports",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_reports
    ).pack(pady=4)

    # Logout
    ctk.CTkButton(
        sidebar,
        text="  Logout",
        width=190,
        height=40,
        corner_radius=8,
        fg_color="#C0392B",
        hover_color="#962D22",
        text_color=WHITE,
        font=("Arial", 13, "bold"),
        anchor="w",
        command=show_login
    ).pack(
        side="bottom",
        pady=25,
        padx=20
    )

    # =========================
    # CONTENT
    # =========================
    content = ctk.CTkFrame(
        main,
        fg_color="#071A2B",
        corner_radius=0
    )
    content.pack(
        side="right",
        fill="both",
        expand=True
    )

    # =========================
    # TOP HEADER
    # =========================
    header = ctk.CTkFrame(
        content,
        height=65,
        fg_color="#081E32",
        corner_radius=0
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    ctk.CTkLabel(
        header,
        text="Products Management",
        font=("Arial", 16, "bold"),
        text_color=WHITE
    ).pack(
        side="left",
        padx=25
    )

    ctk.CTkLabel(
        header,
        text="●  Admin",
        font=("Arial", 13, "bold"),
        text_color=WHITE
    ).pack(
        side="right",
        padx=30
    )

    # =========================
    # CONTENT AREA
    # =========================
    content_area = ctk.CTkFrame(
        content,
        fg_color="transparent"
    )
    content_area.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=25
    )

    # Title
    ctk.CTkLabel(
        content_area,
        text="Products",
        font=("Arial", 30, "bold"),
        text_color=WHITE
    ).pack(anchor="w")

    ctk.CTkLabel(
        content_area,
        text="Manage your products and stock information",
        font=("Arial", 13),
        text_color="#718096"
    ).pack(
        anchor="w",
        pady=(3, 20)
    )

    # =========================
    # TOOLBAR
    # =========================
    toolbar = ctk.CTkFrame(
        content_area,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    toolbar.pack(
        fill="x",
        pady=(0, 15)
    )

    # Search
    search_entry = ctk.CTkEntry(
        toolbar,
        width=300,
        height=40,
        corner_radius=8,
        fg_color="#102D47",
        border_width=1,
        border_color="#1C405D",
        text_color=WHITE,
        placeholder_text="Search ID, name, or category",
        placeholder_text_color="#718096"
    )
    search_entry.pack(
        side="left",
        padx=15,
        pady=15
    )

    ctk.CTkButton(
        toolbar,
        text="Search",
        width=90,
        height=40,
        corner_radius=8,
        fg_color="#1769E0",
        hover_color="#1255B5",
        text_color=WHITE,
        font=("Arial", 12, "bold"),
        command=lambda: search_products(search_entry.get())
    ).pack(
        side="left",
        padx=5
    )

    ctk.CTkButton(
        toolbar,
        text="Low Stock",
        width=100,
        height=40,
        corner_radius=8,
        fg_color="#C0392B",
        hover_color="#962D22",
        text_color=WHITE,
        font=("Arial", 12, "bold"),
        command=show_low_stock
    ).pack(
        side="left",
        padx=5
    )

    ctk.CTkButton(
        toolbar,
        text="+ Add Product",
        width=130,
        height=40,
        corner_radius=8,
        fg_color="#27AE60",
        hover_color="#1E8449",
        text_color=WHITE,
        font=("Arial", 12, "bold"),
        command=add_product
    ).pack(
        side="right",
        padx=15
    )

    # =========================
    # PRODUCT TABLE
    # =========================
    table = ctk.CTkFrame(
        content_area,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    table.pack(
        fill="both",
        expand=True
    )

    # Table title
    ctk.CTkLabel(
        table,
        text="Product List",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    # Header
    table_header = ctk.CTkFrame(
        table,
        fg_color="#102D47",
        height=45,
        corner_radius=6
    )
    table_header.pack(
        fill="x",
        padx=15,
        pady=(0, 8)
    )

    headers = [
        "Product ID",
        "Product Name",
        "Category",
        "Price",
        "Stock",
        "Status",
        "Action"
    ]

    widths = [100, 190, 150, 110, 80, 110, 150]

    for i, header_text in enumerate(headers):
        ctk.CTkLabel(
            table_header,
            text=header_text,
            width=widths[i],
            anchor="w",
            font=("Arial", 11, "bold"),
            text_color="#8FA3B8"
        ).grid(
            row=0,
            column=i,
            padx=8,
            pady=8,
            sticky="w"
        )

        
    
    # =========================
    # SCROLLABLE PRODUCT AREA
    # =========================
    products_scroll = ctk.CTkScrollableFrame(
        table,
        fg_color="transparent",
        corner_radius=6,
        height=400
    )
    products_scroll.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 10)
    )
    
    # =========================
    # PRODUCT ROWS
    # =========================
    for product in current_products:
        print("DISPLAYING PRODUCT:", product)

        
        row = ctk.CTkFrame(
            products_scroll,
            fg_color="#0E2A42",
            corner_radius=6,
            height=55
        )
        row.pack(fill="x", padx=15, pady=3)
        row.pack_propagate(False)

        ctk.CTkLabel(
            row,
            text=str(product[0]),
            width=100,
            anchor="w",
            text_color=WHITE
        ).pack(side="left", padx=8)

        ctk.CTkLabel(
            row,
            text=str(product[1]),
            width=190,
            anchor="w",
            text_color=WHITE
        ).pack(side="left", padx=8)

        ctk.CTkLabel(
            row,
            text=str(product[2]),
            width=150,
            anchor="w",
            text_color=WHITE
        ).pack(side="left", padx=8)

        ctk.CTkLabel(
                row,
            text=f"₱{float(str(product[3]).replace('₱', '').replace(',', '')):,.2f}",
            width=110,
            anchor="w",
            text_color=WHITE
        ).pack(side="left", padx=8)

        ctk.CTkLabel(
            row,
            text=str(product[4]),
            width=80,
            anchor="w",
            text_color=WHITE
        ).pack(side="left", padx=8)

        status_color = "#F2A900" if str(product[5]) == "Low Stock" else "#27AE60"

        ctk.CTkLabel(
            row,
            text=str(product[5]),
            width=110,
            anchor="w",
            text_color=status_color
        ).pack(side="left", padx=8)

        action_frame = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )
        action_frame.pack(side="right", padx=8)

        ctk.CTkButton(
            action_frame,
            text="Edit",
            width=60,
            height=30,
            command=lambda p_id=product[0]: edit_product_by_id(p_id)
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            action_frame,
            text="Delete",
            width=65,
            height=30,
            fg_color="#C0392B",
            hover_color="#962D22",
            command=lambda p_id=product[0]: delete_product_by_id(p_id)
        ).pack(side="left", padx=3)

# =========================
# GENERATE RECEIPT
# =========================
def generate_receipt(sale_id, product_id, product_name, quantity, price, total_price, sale_date):

    filename = f"Receipt_{sale_id}.pdf"

    pdf = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    y = height - 80

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(
        width / 2,
        y,
        "INVENTORY SALES SYSTEM"
    )

    y -= 35

    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(
        width / 2,
        y,
        "Sales Receipt"
    )

    y -= 45

    pdf.setFont("Helvetica", 11)

    pdf.drawString(80, y, f"Receipt No.: {sale_id}")
    y -= 20

    pdf.drawString(80, y, f"Date: {sale_date}")
    y -= 35

    pdf.drawString(80, y, f"Product ID: {product_id}")
    y -= 20

    pdf.drawString(80, y, f"Product: {product_name}")
    y -= 20

    pdf.drawString(80, y, f"Quantity: {quantity}")
    y -= 20

    pdf.drawString(80, y, f"Price: PHP {float(price):,.2f}")
    y -= 30

    pdf.line(80, y, width - 80, y)

    y -= 30

    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        80,
        y,
        f"TOTAL: PHP {float(total_price):,.2f}"
    )

    y -= 50

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawCentredString(
        width / 2,
        y,
        "THANK YOU!"
    )

    pdf.save()

    messagebox.showinfo(
        "Receipt Generated",
        f"Receipt saved successfully!\n\nFile: {filename}"
    )
# =========================
# RECORD SALE
# =========================
def record_sale(product_id, quantity):

    product_id = product_id.strip()
    quantity = quantity.strip()

    if not product_id or not quantity:
        messagebox.showerror(
            "Invalid Input",
            "Please enter Product ID and Quantity."
        )
        return

    try:
        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Quantity",
            "Quantity must be a positive whole number."
        )
        return

    db = None
    cursor = None

    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Get product information
        cursor.execute(
            """
            SELECT product_name, price, stock
            FROM products
            WHERE product_id = %s
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        if product is None:
            messagebox.showerror(
                "Product Not Found",
                "Product ID does not exist."
            )
            return

        product_name = product[0]
        price = float(product[1])
        stock = int(product[2])

        # Check stock
        if quantity > stock:
            messagebox.showerror(
                "Insufficient Stock",
                f"Available stock: {stock}"
            )
            return

        # Calculate total
        total = price * quantity

        # New stock
        new_stock = stock - quantity

        # Update status
        if new_stock <= 5:
            status = "Low Stock"
        else:
            status = "Available"

        # Save sale
        cursor.execute(
            """
            INSERT INTO sales
            (product_id, quantity, total_price)
            VALUES (%s, %s, %s)
            """,
            (product_id, quantity, total)
        )
        sale_id = cursor.lastrowid

        # Update product stock
        cursor.execute(
            """
            UPDATE products
            SET stock = %s,
                status = %s
            WHERE product_id = %s
            """,
            (new_stock, status, product_id)
        )

        db.commit()
        generate_receipt(
            sale_id=sale_id,
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            price=price,
            total_price=total,
            sale_date=__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        show_sales()

    except mysql.connector.Error as err:

        if db is not None:
            db.rollback()

        messagebox.showerror(
            "Database Error",
            f"Database error:\n{err}"
        )

    finally:

        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()
# =========================
# SALES SUMMARY
# =========================
def get_sales_summary():

    total_transactions = 0
    total_sales = 0

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(total_price), 0)
            FROM sales
        """)

        result = cursor.fetchone()

        total_transactions = result[0]
        total_sales = result[1]

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Failed to load sales summary:\n{error}"
        )

    return total_transactions, total_sales
# =========================
# SALES
# =========================
def show_sales():

    clear_screen()

    # =========================
    # GET SALES DATA
    # =========================
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            SELECT sale_id, product_id, quantity, total_price, sale_date
            FROM sales
            ORDER BY sale_id DESC
        """)

        sales = cursor.fetchall()

        cursor.close()
        db.close()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Failed to load sales:\n{error}"
        )

        sales = []

    total_transactions, total_sales = get_sales_summary()

    # =========================
    # MAIN BACKGROUND
    # =========================
    main = ctk.CTkFrame(
        app,
        fg_color="#071A2B",
        corner_radius=0
    )
    main.pack(fill="both", expand=True)

    # =========================
    # SIDEBAR
    # =========================
    sidebar = ctk.CTkFrame(
        main,
        width=230,
        corner_radius=0,
        fg_color="#061525"
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Logo
    ctk.CTkLabel(
        sidebar,
        text="▣",
        font=("Arial", 28, "bold"),
        text_color="#2F80FF"
    ).pack(pady=(25, 5))

    ctk.CTkLabel(
        sidebar,
        text="Inventory and Sales\nManagement System",
        font=("Arial", 13, "bold"),
        text_color=WHITE,
        justify="center"
    ).pack(pady=(0, 25))

    # =========================
    # MENU
    # =========================
    ctk.CTkLabel(
        sidebar,
        text="MAIN MENU",
        font=("Arial", 11, "bold"),
        text_color="#718096"
    ).pack(
        anchor="w",
        padx=25,
        pady=(5, 10)
    )

    # Dashboard
    ctk.CTkButton(
        sidebar,
        text="  Dashboard",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_dashboard
    ).pack(pady=4)

    # Products
    ctk.CTkButton(
        sidebar,
        text="  Products",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_products
    ).pack(pady=4)

    # Inventory
    ctk.CTkButton(
        sidebar,
        text="  Inventory",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_inventory
    ).pack(pady=4)

    # Sales - ACTIVE
    ctk.CTkButton(
        sidebar,
        text="  Sales",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="#1769E0",
        hover_color="#1769E0",
        text_color=WHITE,
        font=("Arial", 13, "bold"),
        anchor="w",
        command=show_sales
    ).pack(pady=4)

    # Reports
    ctk.CTkButton(
        sidebar,
        text="  Reports",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_reports
    ).pack(pady=4)

    # Logout
    ctk.CTkButton(
        sidebar,
        text="  Logout",
        width=190,
        height=40,
        corner_radius=8,
        fg_color="#C0392B",
        hover_color="#962D22",
        text_color=WHITE,
        font=("Arial", 13, "bold"),
        anchor="w",
        command=show_login
    ).pack(
        side="bottom",
        pady=25,
        padx=20
    )

    # =========================
    # CONTENT
    # =========================
    content = ctk.CTkFrame(
        main,
        fg_color="#071A2B",
        corner_radius=0
    )
    content.pack(
        side="right",
        fill="both",
        expand=True
    )

    # =========================
    # HEADER
    # =========================
    header = ctk.CTkFrame(
        content,
        height=65,
        fg_color="#081E32",
        corner_radius=0
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    ctk.CTkLabel(
        header,
        text="Sales Management",
        font=("Arial", 16, "bold"),
        text_color=WHITE
    ).pack(
        side="left",
        padx=25
    )

    ctk.CTkLabel(
        header,
        text="●  Admin",
        font=("Arial", 13, "bold"),
        text_color=WHITE
    ).pack(
        side="right",
        padx=30
    )

    # =========================
    # CONTENT AREA
    # =========================
    content_area = ctk.CTkFrame(
        content,
        fg_color="transparent"
    )
    content_area.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=25
    )

    # Title
    ctk.CTkLabel(
        content_area,
        text="Sales",
        font=("Arial", 30, "bold"),
        text_color=WHITE
    ).pack(anchor="w")

    ctk.CTkLabel(
        content_area,
        text="Record sales and view transaction history",
        font=("Arial", 13),
        text_color="#718096"
    ).pack(
        anchor="w",
        pady=(3, 20)
    )

    # =========================
    # SUMMARY CARDS
    # =========================
    summary_frame = ctk.CTkFrame(
        content_area,
        fg_color="transparent"
    )
    summary_frame.pack(
        fill="x",
        pady=(0, 15)
    )

    # Transactions
    transaction_card = ctk.CTkFrame(
        summary_frame,
        height=105,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    transaction_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 6)
    )
    transaction_card.pack_propagate(False)

    ctk.CTkLabel(
        transaction_card,
        text="Total Transactions",
        font=("Arial", 12, "bold"),
        text_color="#8FA3B8"
    ).pack(
        anchor="w",
        padx=18,
        pady=(17, 3)
    )

    ctk.CTkLabel(
        transaction_card,
        text=str(total_transactions),
        font=("Arial", 25, "bold"),
        text_color="#2F80FF"
    ).pack(
        anchor="w",
        padx=18
    )

    # Total Sales
    sales_card = ctk.CTkFrame(
        summary_frame,
        height=105,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    sales_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(6, 0)
    )
    sales_card.pack_propagate(False)

    ctk.CTkLabel(
        sales_card,
        text="Total Sales",
        font=("Arial", 12, "bold"),
        text_color="#8FA3B8"
    ).pack(
        anchor="w",
        padx=18,
        pady=(17, 3)
    )

    ctk.CTkLabel(
        sales_card,
        text=f"₱{float(total_sales):,.2f}",
        font=("Arial", 25, "bold"),
        text_color="#27AE60"
    ).pack(
        anchor="w",
        padx=18
    )

    # =========================
    # RECORD SALE
    # =========================
    sale_form = ctk.CTkFrame(
        content_area,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    sale_form.pack(
        fill="x",
        pady=(0, 15)
    )

    ctk.CTkLabel(
        sale_form,
        text="Record New Sale",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    form_frame = ctk.CTkFrame(
        sale_form,
        fg_color="transparent"
    )
    form_frame.pack(
        fill="x",
        padx=20,
        pady=(0, 18)
    )

    # Product ID
    ctk.CTkLabel(
        form_frame,
        text="Product ID",
        font=("Arial", 11, "bold"),
        text_color="#8FA3B8"
    ).pack(
        side="left",
        padx=(0, 8)
    )

    product_entry = ctk.CTkEntry(
        form_frame,
        width=150,
        height=40,
        corner_radius=8,
        fg_color="#102D47",
        border_width=1,
        border_color="#1C405D",
        text_color=WHITE,
        placeholder_text="e.g. P001",
        placeholder_text_color="#718096"
    )
    product_entry.pack(
        side="left",
        padx=(0, 20)
    )

    # Quantity
    ctk.CTkLabel(
        form_frame,
        text="Quantity",
        font=("Arial", 11, "bold"),
        text_color="#8FA3B8"
    ).pack(
        side="left",
        padx=(0, 8)
    )

    quantity_entry = ctk.CTkEntry(
        form_frame,
        width=120,
        height=40,
        corner_radius=8,
        fg_color="#102D47",
        border_width=1,
        border_color="#1C405D",
        text_color=WHITE,
        placeholder_text="Quantity",
        placeholder_text_color="#718096"
    )
    quantity_entry.pack(
        side="left",
        padx=(0, 20)
    )
    
    # Press Enter to record sale
    quantity_entry.bind(
        "<Return>",
        lambda event: record_sale(
            product_entry.get(),
            quantity_entry.get()
        )
    )

    # Record Button
    ctk.CTkButton(
        form_frame,
        text="Record Sale",
        width=140,
        height=40,
        corner_radius=8,
        fg_color="#27AE60",
        hover_color="#1E8449",
        text_color=WHITE,
        font=("Arial", 12, "bold"),
        command=lambda: record_sale(
            product_entry.get(),
            quantity_entry.get()
        )
    ).pack(
        side="left"
    )

    # =========================
    # TRANSACTION HISTORY
    # =========================
    table = ctk.CTkFrame(
        content_area,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    table.pack(
        fill="both",
        expand=True,
        pady=(0, 10)
    )

    ctk.CTkLabel(
        table,
        text="Transaction History",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    # Header
    table_header = ctk.CTkFrame(
        table,
        fg_color="#102D47",
        height=45,
        corner_radius=6
    )
    table_header.pack(
        fill="x",
        padx=15,
        pady=(0, 8)
    )

    headers = [
        "Sale ID",
        "Product ID",
        "Quantity",
        "Total Price",
        "Sale Date"
    ]

    widths = [
        100,
        130,
        110,
        150,
        220
    ]

    for i, header_text in enumerate(headers):

        ctk.CTkLabel(
            table_header,
            text=header_text,
            width=widths[i],
            anchor="w",
            font=("Arial", 11, "bold"),
            text_color="#8FA3B8"
        ).grid(
            row=0,
            column=i,
            padx=8,
            pady=8,
            sticky="w"
        )
        
    sales_scroll = ctk.CTkScrollableFrame(
        table,
        height=300,
        fg_color="transparent",
        corner_radius=6
    )

    sales_scroll.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 15)
    )
     # =========================
    # SALES ROWS
    # =========================
    for sale in sales:

        row = ctk.CTkFrame(
            sales_scroll,
            fg_color="#0E2A42",
            corner_radius=6,
            height=48
        )
        row.pack(
            fill="x",
            padx=15,
            pady=3
        )
        row.pack_propagate(False)

        values = [
            sale[0],
            sale[1],
            sale[2],
            f"₱{float(sale[3]):,.2f}",
            sale[4]
        ]

        for i, value in enumerate(values):

            ctk.CTkLabel(
                row,
                text=str(value),
                width=widths[i],
                anchor="w",
                font=("Arial", 11),
                text_color=WHITE
            ).pack(
                side="left",
                padx=8
            )

        # DELETE BUTTON
        ctk.CTkButton(
            row,
            text="Delete",
            width=80,
            height=32,
            corner_radius=7,
            fg_color="#C0392B",
            hover_color="#962D22",
            text_color=WHITE,
            font=("Arial", 11, "bold"),
            command=lambda sale_id=sale[0]: delete_transaction(sale_id)
        ).pack(
            side="right",
            padx=10
        )

def delete_transaction(sale_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM sales WHERE sale_id = %s",
            (sale_id,)
        )

        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo(
            "Success",
            "Transaction deleted successfully!"
        )

        show_sales()

    except mysql.connector.Error as err:
        messagebox.showerror(
            "Database Error",
            f"Failed to delete transaction:\n{err}"
        )
# =========================
# REPORTS
# =========================
def show_reports():

    clear_screen()

    # =========================
    # GET REPORT DATA
    # =========================
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Total Products
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]

        # Total Stock
        cursor.execute(
            "SELECT COALESCE(SUM(stock), 0) FROM products"
        )
        total_stock = cursor.fetchone()[0]

        # Low Stock
        cursor.execute(
            "SELECT COUNT(*) FROM products WHERE stock <= 5"
        )
        low_stock = cursor.fetchone()[0]

        # Sales Summary
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(total_price), 0)
            FROM sales
        """)
        total_transactions, total_sales = cursor.fetchone()

        # Sales Records
        cursor.execute("""
            SELECT sale_id, product_id, quantity, total_price, sale_date
            FROM sales
            ORDER BY sale_id DESC
        """)
        sales = cursor.fetchall()

        cursor.close()
        db.close()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Failed to load reports:\n{error}"
        )

        total_products = 0
        total_stock = 0
        low_stock = 0
        total_transactions = 0
        total_sales = 0
        sales = []

    # =========================
    # MAIN BACKGROUND
    # =========================
    main = ctk.CTkFrame(
        app,
        fg_color="#071A2B",
        corner_radius=0
    )
    main.pack(fill="both", expand=True)

    # =========================
    # SIDEBAR
    # =========================
    sidebar = ctk.CTkFrame(
        main,
        width=230,
        corner_radius=0,
        fg_color="#061525"
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Logo
    ctk.CTkLabel(
        sidebar,
        text="▣",
        font=("Arial", 28, "bold"),
        text_color="#2F80FF"
    ).pack(pady=(25, 5))

    ctk.CTkLabel(
        sidebar,
        text="Inventory and Sales\nManagement System",
        font=("Arial", 13, "bold"),
        text_color=WHITE,
        justify="center"
    ).pack(pady=(0, 25))

    # Main Menu
    ctk.CTkLabel(
        sidebar,
        text="MAIN MENU",
        font=("Arial", 11, "bold"),
        text_color="#718096"
    ).pack(
        anchor="w",
        padx=25,
        pady=(5, 10)
    )

    # Dashboard
    ctk.CTkButton(
        sidebar,
        text="  Dashboard",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_dashboard
    ).pack(pady=4)

    # Products
    ctk.CTkButton(
        sidebar,
        text="  Products",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_products
    ).pack(pady=4)

    # Inventory
    ctk.CTkButton(
        sidebar,
        text="  Inventory",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_inventory
    ).pack(pady=4)

    # Sales
    ctk.CTkButton(
        sidebar,
        text="  Sales",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#102D47",
        text_color=WHITE,
        font=("Arial", 13),
        anchor="w",
        command=show_sales
    ).pack(pady=4)

    # Reports - ACTIVE
    ctk.CTkButton(
        sidebar,
        text="  Reports",
        width=190,
        height=42,
        corner_radius=8,
        fg_color="#1769E0",
        hover_color="#1769E0",
        text_color=WHITE,
        font=("Arial", 13, "bold"),
        anchor="w",
        command=show_reports
    ).pack(pady=4)

    # Logout
    ctk.CTkButton(
        sidebar,
        text="  Logout",
        width=190,
        height=40,
        corner_radius=8,
        fg_color="#C0392B",
        hover_color="#962D22",
        text_color=WHITE,
        font=("Arial", 13, "bold"),
        anchor="w",
        command=show_login
    ).pack(
        side="bottom",
        pady=25,
        padx=20
    )

    # =========================
    # CONTENT
    # =========================
    content = ctk.CTkFrame(
        main,
        fg_color="#071A2B",
        corner_radius=0
    )
    content.pack(
        side="right",
        fill="both",
        expand=True
    )

    # =========================
    # TOP HEADER
    # =========================
    header = ctk.CTkFrame(
        content,
        height=65,
        fg_color="#081E32",
        corner_radius=0
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    ctk.CTkLabel(
        header,
        text="Reports and Analytics",
        font=("Arial", 16, "bold"),
        text_color=WHITE
    ).pack(
        side="left",
        padx=25
    )

    ctk.CTkLabel(
        header,
        text="●  Admin",
        font=("Arial", 13, "bold"),
        text_color=WHITE
    ).pack(
        side="right",
        padx=30
    )

    # =========================
    # CONTENT AREA
    # =========================
    content_area = ctk.CTkFrame(
        content,
        fg_color="transparent"
    )
    content_area.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=25
    )

    # Title
    ctk.CTkLabel(
        content_area,
        text="Reports",
        font=("Arial", 30, "bold"),
        text_color=WHITE
    ).pack(anchor="w")

    ctk.CTkLabel(
        content_area,
        text="View inventory and sales performance",
        font=("Arial", 13),
        text_color="#718096"
    ).pack(
        anchor="w",
        pady=(3, 20)
    )

    # =========================
    # SUMMARY CARDS
    # =========================
    summary_frame = ctk.CTkFrame(
        content_area,
        fg_color="transparent"
    )
    summary_frame.pack(
        fill="x",
        pady=(0, 15)
    )

    # Products Card
    card1 = ctk.CTkFrame(
        summary_frame,
        height=105,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    card1.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 6)
    )
    card1.pack_propagate(False)

    ctk.CTkLabel(
        card1,
        text="Total Products",
        font=("Arial", 12, "bold"),
        text_color="#8FA3B8"
    ).pack(
        anchor="w",
        padx=18,
        pady=(17, 3)
    )

    ctk.CTkLabel(
        card1,
        text=str(total_products),
        font=("Arial", 25, "bold"),
        text_color="#2F80FF"
    ).pack(
        anchor="w",
        padx=18
    )

    # Stock Card
    card2 = ctk.CTkFrame(
        summary_frame,
        height=105,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    card2.pack(
        side="left",
        fill="both",
        expand=True,
        padx=6
    )
    card2.pack_propagate(False)

    ctk.CTkLabel(
        card2,
        text="Total Stock",
        font=("Arial", 12, "bold"),
        text_color="#8FA3B8"
    ).pack(
        anchor="w",
        padx=18,
        pady=(17, 3)
    )

    ctk.CTkLabel(
        card2,
        text=str(total_stock),
        font=("Arial", 25, "bold"),
        text_color="#27AE60"
    ).pack(
        anchor="w",
        padx=18
    )

    # Low Stock Card
    card3 = ctk.CTkFrame(
        summary_frame,
        height=105,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    card3.pack(
        side="left",
        fill="both",
        expand=True,
        padx=6
    )
    card3.pack_propagate(False)

    ctk.CTkLabel(
        card3,
        text="Low Stock Items",
        font=("Arial", 12, "bold"),
        text_color="#8FA3B8"
    ).pack(
        anchor="w",
        padx=18,
        pady=(17, 3)
    )

    ctk.CTkLabel(
        card3,
        text=str(low_stock),
        font=("Arial", 25, "bold"),
        text_color="#F2A900"
    ).pack(
        anchor="w",
        padx=18
    )

    # Sales Card
    card4 = ctk.CTkFrame(
        summary_frame,
        height=105,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    card4.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(6, 0)
    )
    card4.pack_propagate(False)

    ctk.CTkLabel(
        card4,
        text="Total Sales",
        font=("Arial", 12, "bold"),
        text_color="#8FA3B8"
    ).pack(
        anchor="w",
        padx=18,
        pady=(17, 3)
    )

    ctk.CTkLabel(
        card4,
        text=f"₱{float(total_sales):,.2f}",
        font=("Arial", 23, "bold"),
        text_color="#27AE60"
    ).pack(
        anchor="w",
        padx=18
    )

    # =========================
    # SALES REPORT TABLE
    # =========================
    report_table = ctk.CTkFrame(
        content_area,
        fg_color="#0B243A",
        corner_radius=12,
        border_width=1,
        border_color="#153A56"
    )
    report_table.pack(
        fill="both",
        expand=True
    )

    ctk.CTkLabel(
        report_table,
        text="Sales Report",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    # Table Header
    table_header = ctk.CTkFrame(
        report_table,
        fg_color="#102D47",
        height=45,
        corner_radius=6
    )
    table_header.pack(
        fill="x",
        padx=15,
        pady=(0, 8)
    )

    headers = [
        "Sale ID",
        "Product ID",
        "Quantity",
        "Total Price",
        "Sale Date"
    ]

    widths = [
        100,
        130,
        110,
        150,
        220
    ]

    for i, header_text in enumerate(headers):

        ctk.CTkLabel(
            table_header,
            text=header_text,
            width=widths[i],
            anchor="w",
            font=("Arial", 11, "bold"),
            text_color="#8FA3B8"
        ).grid(
            row=0,
            column=i,
            padx=8,
            pady=8,
            sticky="w"
        )

    
    # =========================
    # SCROLLABLE SALES ROWS
    # =========================
    sales_scroll = ctk.CTkScrollableFrame(
        report_table,
        height=300,
        fg_color="transparent",
        corner_radius=6
    )
    sales_scroll.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 15)
    )

    for sale in sales:
        row = ctk.CTkFrame(
            sales_scroll,
            fg_color="#0E2A42",
            corner_radius=6,
            height=48
        )
        row.pack(
            fill="x",
            padx=5,
            pady=3
        )
        row.pack_propagate(False)

        values = [
            sale[0],
            sale[1],
            sale[2],
            f"₱{float(sale[3]):,.2f}",
            sale[4]
        ]

        for i, value in enumerate(values):
            ctk.CTkLabel(
                row,
                text=str(value),
                width=widths[i],
                anchor="w",
                font=("Arial", 11),
                text_color=WHITE
            ).pack(
                side="left",
                padx=8
            )
def show_login():
    clear_screen()

    # =========================
    # BACKGROUND
    # =========================
    background = ctk.CTkFrame(
        app,
        fg_color=DARK_BLUE,
        corner_radius=0
    )
    background.pack(fill="both", expand=True)

    # =========================
    # DECORATIVE BACKGROUND SHAPES
    # =========================

    # Top-left decorative shape
    deco1 = ctk.CTkFrame(
        background,
        width=280,
        height=280,
        corner_radius=140,
        fg_color="#08698F"
    )
    deco1.place(x=-120, y=-100)

    # Bottom-right decorative shape
    deco2 = ctk.CTkFrame(
        background,
        width=350,
        height=350,
        corner_radius=175,
        fg_color="#0A6689"
    )
    deco2.place(
        relx=1.0,
        rely=1.0,
        x=-120,
        y=-130,
        anchor="center"
    )

    # Small decorative circles
    deco3 = ctk.CTkFrame(
        background,
        width=90,
        height=90,
        corner_radius=45,
        fg_color="#1580A8"
    )
    deco3.place(relx=0.08, rely=0.75)

    deco4 = ctk.CTkFrame(
        background,
        width=70,
        height=70,
        corner_radius=35,
        fg_color="#1580A8"
    )
    deco4.place(relx=0.87, rely=0.18)

    # =========================
    # LOGIN CARD SHADOW
    # =========================

    shadow = ctk.CTkFrame(
        background,
        width=470,
        height=535,
        corner_radius=24,
        fg_color="#004867"
    )
    shadow.place(
        relx=0.5,
        rely=0.5,
        x=8,
        y=8,
        anchor="center"
    )

    # =========================
    # LOGIN CARD
    # =========================

    login_card = ctk.CTkFrame(
        background,
        width=470,
        height=535,
        fg_color=WHITE,
        corner_radius=24
    )
    login_card.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )
    login_card.pack_propagate(False)

    # =========================
    # TOP ACCENT
    # =========================

    accent = ctk.CTkFrame(
        login_card,
        width=90,
        height=6,
        corner_radius=3,
        fg_color=MID_BLUE
    )
    accent.pack(pady=(28, 15))

    # =========================
    # APP ICON
    # =========================

    icon_frame = ctk.CTkFrame(
        login_card,
        width=70,
        height=70,
        corner_radius=20,
        fg_color=VERY_LIGHT_BLUE
    )
    icon_frame.pack()
    icon_frame.pack_propagate(False)

    ctk.CTkLabel(
        icon_frame,
        text="▣",
        font=("Arial", 34, "bold"),
        text_color=DARK_BLUE
    ).place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    # =========================
    # TITLE
    # =========================

    title = ctk.CTkLabel(
        login_card,
        text="Inventory Sales System",
        font=("Arial", 27, "bold"),
        text_color=DARK_BLUE
    )
    title.pack(pady=(15, 4))

    welcome = ctk.CTkLabel(
        login_card,
        text="Welcome back! Sign in to continue.",
        font=("Arial", 14),
        text_color=GRAY
    )
    welcome.pack(pady=(0, 25))

    # =========================
    # USERNAME
    # =========================

    username_label = ctk.CTkLabel(
        login_card,
        text="USERNAME",
        font=("Arial", 11, "bold"),
        text_color=TEXT
    )
    username_label.pack(
        anchor="w",
        padx=65
    )

    global username_entry

    username_entry = ctk.CTkEntry(
        login_card,
        width=340,
        height=44,
        corner_radius=10,
        border_width=1,
        border_color="#AAB7BE",
        fg_color="#F8FAFB",
        text_color=TEXT,
        placeholder_text="Enter username",
        placeholder_text_color="#9AA6AD"
    )
    username_entry.pack(pady=(6, 16))

    # =========================
    # PASSWORD
    # =========================

    password_label = ctk.CTkLabel(
        login_card,
        text="PASSWORD",
        font=("Arial", 11, "bold"),
        text_color=TEXT
    )
    password_label.pack(
        anchor="w",
        padx=65
    )

    global password_entry

    password_entry = ctk.CTkEntry(
        login_card,
        width=340,
        height=44,
        corner_radius=10,
        border_width=1,
        border_color="#AAB7BE",
        fg_color="#F8FAFB",
        text_color=TEXT,
        placeholder_text="Enter password",
        placeholder_text_color="#9AA6AD",
        show="*"
    )
    password_entry.pack(pady=(6, 5))

    # =========================
    # ERROR MESSAGE
    # =========================

    global error_label

    error_label = ctk.CTkLabel(
        login_card,
        text="",
        font=("Arial", 12),
        text_color=RED
    )
    error_label.pack(
        pady=(2, 2)
    )

    # =========================
    # LOGIN BUTTON
    # =========================

    login_button = ctk.CTkButton(
        login_card,
        text="LOGIN  →",
        width=340,
        height=46,
        corner_radius=10,
        fg_color=DARK_BLUE,
        hover_color=MID_BLUE,
        text_color=WHITE,
        font=("Arial", 14, "bold"),
        command=login
    )
    login_button.pack(pady=(12, 15))

    
    # Allow Enter key to log in
    username_entry.bind("<Return>", lambda event: login())
    password_entry.bind("<Return>", lambda event: login())
    login_button.bind("<Return>", lambda event: login())

    # =========================
    # DIVIDER
    # =========================

    divider = ctk.CTkFrame(
        login_card,
        width=340,
        height=1,
        fg_color="#D9E2E7"
    )
    divider.pack()

    # =========================
    # FOOTER
    # =========================

    footer = ctk.CTkLabel(
        login_card,
        text="Inventory & Sales Management",
        font=("Arial", 11),
        text_color=GRAY
    )
    footer.pack(pady=(12, 2))

    version = ctk.CTkLabel(
        login_card,
        text="Secure Management System",
        font=("Arial", 10),
        text_color="#9AA6AD"
    )
    version.pack()

# =========================
# LOGIN FUNCTION
# =========================
def login():

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "admin" and password == "admin123":
        error_label.configure(text="")
        show_dashboard()

    else:
        error_label.configure(
            text="Invalid username or password."
        )
# =========================
# START APPLICATION
# =========================
try:
    db = get_db_connection()
    print("MySQL connection successful!")
    db.close()
except mysql.connector.Error as err:
    print("MySQL connection failed:", err)

show_login()
app.mainloop()