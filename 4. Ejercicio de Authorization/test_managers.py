from datetime import datetime
from decimal import Decimal

from managers.product_manager import ProductManager
from managers.user_manager import UserManager
from managers.invoice_manager import InvoiceManager

import dbSetup

def test_user_manager():
    print("\n=== Testing UserManager ===")
    u = UserManager()

    # Create a new user
    print("\n Creating a new user...")
    new_user = u.Create_user("Roberto Almada", "Rober.@gmail.com", "123456", "ADMIN")
    if new_user:
        print(f"New user created: {new_user.name}, Email: {new_user.email}, Role: {new_user.role}")
    else:
        print("Failed to create new user.")
        return

    # Get Users by ID
    print("\n Getting user by ID...")
    fetched = u.get_user_by_id(new_user.id)
    if fetched:
        print(f"User found by ID {new_user.id}: {fetched.name}, Email: {fetched.email}, Role: {fetched.role}")
    else:
        print(f"No user found with ID {new_user.id}")

    # Update user
    print("\n Updating user...")
    updated_user = u.update_user(new_user.id, name="Roberto A.", role="USER")
    if updated_user:
        print(f"User updated: {updated_user.name}, Email: {updated_user.email}, Role: {updated_user.role}")
    else:
        print(f"Failed to update user with ID {new_user.id}")

    # Get all users
    print("\n Listing all users...")
    all_users = u.get_users()
    print(f"Total users: {len(all_users)}")
    for user in all_users:
        print(f"User ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role}")

    return user

def test_product_manager():
    print("\n=== Testing ProductManager ===")
    p = ProductManager()

    # Create a new product
    print("\n Creating a new product...")
    new_products = [
        ("Red Apple", 2.50, "2026-07-01", 100),
        ("Banana", 1.20, "2026-07-02", 70),
        ("Orange", 1.80, "2026-07-03", 200)
    ]

    created_products = []
    for name, price, entry_date, quantity in new_products:
        product = p.create_product(name, price, entry_date, quantity)
        if product:
            print(f"Product created: {product.name}, Price: {product.price}, Entry Date: {product.entry_date}, Quantity: {product.quantity}")
            created_products.append(product)
        else:
            print(f"Failed to create product: {name}")

    # Get all products
    print("\n Listing all products...")
    all_products = p.get_products()
    print(f"Total products: {len(all_products)}")
    for product in all_products:
        print(f"Product ID: {product.id}, Name: {product.name}, Price: {product.price}, Entry Date: {product.entry_date}, Quantity: {product.quantity}")

    # Update a product
    if created_products:
        print("\n Updating a product...")
        product_to_update = p.update_product(created_products[0].id, price=2.75, quantity=300)
        if product_to_update:
            print(f"Product updated: {product_to_update.name}, Price: {product_to_update.price}, Quantity: {product_to_update.quantity}")
        else:
            print(f"Failed to update product with ID {created_products[0].id}")

    # Get product by ID
    if created_products:
        print("\n Getting product by ID...")
        fetched_product = p.get_product_by_id(created_products[0].id)
        if fetched_product:
            print(f"Product found by ID {created_products[0].id}: {fetched_product.name}, Price: {fetched_product.price}, Entry Date: {fetched_product.entry_date}, Quantity: {fetched_product.quantity}")
        else:
            print(f"No product found with ID {created_products[0].id}")

    return created_products

def test_invoice_manager(user, products):
    print("\n=== Testing InvoiceManager ===")
    i = InvoiceManager()

    # Create a new invoice
    print("\n Creating a new invoice...")
    item_data = [
        {"product_id": products[0].id, "quantity": 5},
        {"product_id": products[1].id, "quantity": 10}
    ]

    invoice = i.create_invoice(user.id, item_data)
    if invoice:
        print(f"Invoice created: ID: {invoice.id}, User ID: {invoice.user_id}, Total: {invoice.total}")
    else:
        print("Failed to create invoice.")
        return

    # Get invoices by user
    print("\n Getting invoices by user...")
    user_invoices = i.get_invoices_by_user_id(user.id)
    print(f"Total invoices for user ID {user.id}: {len(user_invoices)}")
    for inv in user_invoices:
        print(f"Invoice ID: {inv.id}, Total: {inv.total}, Created At: {inv.created_at}")

    # Get all invoices
    print("\n Getting all invoices...")
    all_invoices = i.get_invoices()
    print(f"Total invoices: {len(all_invoices)}")

    # Get invoice by ID
    print("\n Getting invoice by ID...")
    fetched_invoice = i.get_invoice_by_id(invoice.id)
    if fetched_invoice:
        print(f"Invoice found by ID {invoice.id}: User ID: {fetched_invoice.user_id}, Total: {fetched_invoice.total}, Created At: {fetched_invoice.created_at}")
        print("Invoice Items:")
        for item in fetched_invoice.items:
            print(f"Item ID: {item.id}, Product ID: {item.product_id}, Quantity: {item.quantity}, Unit Price: {item.unit_price}")

    else:
        print(f"No invoice found with ID {invoice.id}") 



if __name__ == "__main__":
    print("Manager and DbSetUp Testing...")

    dbSetup.validate_connection()
    dbSetup.validate_and_create_schema()
    dbSetup.validate_and_create_tables()

    user = test_user_manager()
    products = test_product_manager()
    test_invoice_manager(user, products)

    print("\nAll tests completed.")