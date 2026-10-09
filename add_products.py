
import getpass
import mysql.connector
from itertools import product

TARGET_TOTAL = 300

# Product categories and items
catalog = {
    "HeadWear": [
        "Cap", "Beanie", "Bucket Hat", "Snapback", "Visor",
    ],
    "Clothes": [
        "T-Shirt", "Polo Shirt", "Hoodie", "Jacket", "Sweatshirt",
        "Jeans", "Shorts", "Joggers", "Track Pants", "Uniform",
    ],
    "Shoes": [
        "Running Shoes", "Basketball Shoes", "Sneakers", "Sandals",
        "Slippers", "Training Shoes", "Walking Shoes", "Boots",
    ],
    "Supplies": [
        "Keyboard", "Mouse", "USB Cable", "Flash Drive", "Mouse Pad",
        "Headset", "Webcam", "HDMI Cable", "USB Hub", "Laptop Stand",
    ],
    "Accessories": [
        "Backpack", "Wallet", "Belt", "Socks", "Water Bottle",
        "Sports Bag", "Wristband", "Phone Holder", "Umbrella",
        "Lunch Box",
    ],
}

descriptors = [
    "Classic", "Premium", "Modern", "Sport", "Casual",
    "Pro", "Deluxe", "Basic", "Urban", "Comfort",
    "Active", "Everyday", "Essential", "Flex", "Ultra",
    "Performance", "Lightweight", "Durable", "Standard",
    "Advanced", "Original", "Smart", "Elite", "Eco",
    "Compact", "Professional", "Classic Plus", "Max",
    "Versatile", "Signature",
]

def get_status(stock):
    if stock <= 0:
        return "Out of Stock"
    elif stock <= 10:
        return "Low Stock"
    return "Available"

def main():
    password = getpass.getpass("Enter your MySQL password: ")

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vincecandil!2003",
            database="inventory_system"
        )
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM products")
        total = cursor.fetchone()[0]

        if total >= TARGET_TOTAL:
            print(f"You already have {total} products.")
            return

        cursor.execute(
            "SELECT product_id, product_name FROM products"
        )
        existing = cursor.fetchall()
        existing_ids = {row[0] for row in existing}
        existing_names = {row[1].casefold() for row in existing}

        items = []
        for category, names in catalog.items():
            for descriptor, name in product(
                descriptors, names
            ):
                items.append(
                    (f"{descriptor} {name}", category)
                )

        added = 0
        product_number = 1

        for name, category in items:
            if total + added >= TARGET_TOTAL:
                break

            if name.casefold() in existing_names:
                continue

            # Find an unused product ID
            while True:
                product_id = f"P{product_number:03d}"
                product_number += 1

                if product_id not in existing_ids:
                    break

            # Keep the original five products untouched
            if product_id in {"P001", "P002", "P003",
                              "P004", "P005"}:
                continue

            price = 100 + ((product_number * 137) % 4901)
            stock = (product_number * 7) % 101
            status = get_status(stock)

            cursor.execute(
                """
                INSERT INTO products
                    (product_id, product_name, category,
                     price, stock, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (product_id, name, category,
                 price, stock, status)
            )

            existing_ids.add(product_id)
            existing_names.add(name.casefold())
            added += 1

        connection.commit()

        cursor.execute("SELECT COUNT(*) FROM products")
        final_total = cursor.fetchone()[0]

        print(f"Products added: {added}")
        print(f"Total products now: {final_total}")

    except mysql.connector.Error as error:
        if connection and connection.is_connected():
            connection.rollback()
        print("Database error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()