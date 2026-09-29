# Online Food Ordering Simulation System
# main.py

from datetime import datetime


# -----------------------------
# Sample Food Menu
# -----------------------------

FOOD_MENU = {
    1: {"name": "Veg Burger", "category": "Fast Food", "price": 80},
    2: {"name": "Pizza", "category": "Fast Food", "price": 150},
    3: {"name": "French Fries", "category": "Snacks", "price": 70},
    4: {"name": "Veg Biryani", "category": "Main Course", "price": 180},
    5: {"name": "Paneer Butter Masala", "category": "Main Course", "price": 200},
    6: {"name": "Masala Dosa", "category": "South Indian", "price": 100},
    7: {"name": "Manchurian", "category": "Chinese", "price": 120},
    8: {"name": "Cold Drink", "category": "Beverage", "price": 50},
    9: {"name": "Ice Cream", "category": "Dessert", "price": 60},
}


# -----------------------------
# Users and Orders
# -----------------------------

users = {}
orders = {}


# -----------------------------
# Utility Functions
# -----------------------------

def line():
    print("-" * 60)


def pause():
    input("\nPress Enter to continue...")


# -----------------------------
# User Registration
# -----------------------------

def register():
    print("\n===== USER REGISTRATION =====")
    line()

    username = input("Enter username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    if username in users:
        print("Username already exists.")
        return

    password = input("Enter password: ").strip()

    if not password:
        print("Password cannot be empty.")
        return

    users[username] = {
        "password": password,
        "orders": []
    }

    print("\nRegistration successful!")
    print("You can now login with your username and password.")


# -----------------------------
# User Login
# -----------------------------

def login():
    print("\n===== USER LOGIN =====")
    line()

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username in users and users[username]["password"] == password:
        print(f"\nWelcome, {username}!")
        return username

    print("\nInvalid username or password.")
    return None


# -----------------------------
# Display Food Menu
# -----------------------------

def display_menu():
    print("\n================ FOOD MENU ================")
    print(f"{'ID':<5}{'Food Item':<25}{'Category':<18}{'Price':>10}")
    line()

    for food_id, food in FOOD_MENU.items():
        print(
            f"{food_id:<5}"
            f"{food['name']:<25}"
            f"{food['category']:<18}"
            f"₹{food['price']:>8}"
        )

    line()


# -----------------------------
# Search Food
# -----------------------------

def search_food():
    print("\n===== SEARCH FOOD =====")

    keyword = input("Enter food name to search: ").strip().lower()

    found = False

    print()
    for food_id, food in FOOD_MENU.items():
        if keyword in food["name"].lower():
            print(
                f"{food_id}. {food['name']} - "
                f"₹{food['price']} ({food['category']})"
            )
            found = True

    if not found:
        print("No food item found.")


# -----------------------------
# Add Item to Cart
# -----------------------------

def add_to_cart(cart):
    display_menu()

    try:
        food_id = int(input("Enter food ID: "))

        if food_id not in FOOD_MENU:
            print("Invalid food ID.")
            return

        quantity = int(input("Enter quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        if food_id in cart:
            cart[food_id] += quantity
        else:
            cart[food_id] = quantity

        print(
            f"{quantity} x {FOOD_MENU[food_id]['name']} "
            "added to cart."
        )

    except ValueError:
        print("Please enter a valid number.")


# -----------------------------
# View Cart
# -----------------------------

def view_cart(cart):
    print("\n================ YOUR CART ================")

    if not cart:
        print("Your cart is empty.")
        return 0

    print(f"{'Food Item':<25}{'Qty':<8}{'Price':<12}{'Total':>10}")
    line()

    subtotal = 0

    for food_id, quantity in cart.items():
        food = FOOD_MENU[food_id]

        item_total = food["price"] * quantity
        subtotal += item_total

        print(
            f"{food['name']:<25}"
            f"{quantity:<8}"
            f"₹{food['price']:<11}"
            f"₹{item_total:>9}"
        )

    line()
    print(f"{'Subtotal':<45}₹{subtotal:>9}")

    delivery_charge = 40 if subtotal > 0 else 0
    print(f"{'Delivery Charge':<45}₹{delivery_charge:>9}")

    total = subtotal + delivery_charge

    print(f"{'Total Amount':<45}₹{total:>9}")

    return total


# -----------------------------
# Remove Item from Cart
# -----------------------------

def remove_from_cart(cart):
    if not cart:
        print("\nYour cart is empty.")
        return

    view_cart(cart)

    try:
        food_id = int(input("\nEnter food ID to remove: "))

        if food_id not in cart:
            print("This item is not in your cart.")
            return

        quantity = int(input("Enter quantity to remove: "))

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        if quantity >= cart[food_id]:
            del cart[food_id]
            print("Item removed from cart.")
        else:
            cart[food_id] -= quantity
            print("Quantity updated successfully.")

    except ValueError:
        print("Please enter a valid number.")


# -----------------------------
# Checkout
# -----------------------------

def checkout(username, cart):
    if not cart:
        print("\nYour cart is empty.")
        print("Add some food before checkout.")
        return

    total = view_cart(cart)

    print("\n===== CHECKOUT =====")
    line()

    print("Delivery Details")

    name = input("Enter your name: ").strip()
    address = input("Enter delivery address: ").strip()
    phone = input("Enter phone number: ").strip()

    if not name or not address or not phone:
        print("All delivery details are required.")
        return

    print("\nPayment Method")
    print("1. Cash on Delivery")
    print("2. UPI")
    print("3. Card")

    payment_choice = input("Choose payment method: ").strip()

    payment_methods = {
        "1": "Cash on Delivery",
        "2": "UPI",
        "3": "Card"
    }

    if payment_choice not in payment_methods:
        print("Invalid payment method.")
        return

    payment_method = payment_methods[payment_choice]

    order_id = len(orders) + 1001

    order_items = []

    for food_id, quantity in cart.items():
        food = FOOD_MENU[food_id]

        order_items.append({
            "name": food["name"],
            "quantity": quantity,
            "price": food["price"],
            "total": food["price"] * quantity
        })

    order = {
        "order_id": order_id,
        "username": username,
        "items": order_items,
        "total": total,
        "name": name,
        "address": address,
        "phone": phone,
        "payment": payment_method,
        "status": "Confirmed",
        "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    orders[order_id] = order
    users[username]["orders"].append(order_id)

    cart.clear()

    print("\n============================================")
    print("          ORDER PLACED SUCCESSFULLY!")
    print("============================================")
    print(f"Order ID       : {order_id}")
    print(f"Customer       : {name}")
    print(f"Total Amount   : ₹{total}")
    print(f"Payment Method : {payment_method}")
    print(f"Order Status   : Confirmed")
    print("============================================")


# -----------------------------
# Order History
# -----------------------------

def order_history(username):
    print("\n=========== ORDER HISTORY ===========")

    user_orders = users[username]["orders"]

    if not user_orders:
        print("No orders found.")
        return

    for order_id in user_orders:
        order = orders[order_id]

        print(f"\nOrder ID: {order['order_id']}")
        print(f"Date: {order['date']}")
        print(f"Status: {order['status']}")
        print(f"Payment: {order['payment']}")
        print(f"Total: ₹{order['total']}")

        print("Items:")

        for item in order["items"]:
            print(
                f"  - {item['name']} x {item['quantity']} "
                f"= ₹{item['total']}"
            )

        line()


# -----------------------------
# View Order Details
# -----------------------------

def view_order():
    print("\n===== VIEW ORDER =====")

    try:
        order_id = int(input("Enter Order ID: "))

        if order_id not in orders:
            print("Order not found.")
            return

        order = orders[order_id]

        print("\n------------- ORDER DETAILS -------------")
        print(f"Order ID       : {order['order_id']}")
        print(f"Customer       : {order['name']}")
        print(f"Phone          : {order['phone']}")
        print(f"Address        : {order['address']}")
        print(f"Date           : {order['date']}")
        print(f"Payment        : {order['payment']}")
        print(f"Status         : {order['status']}")

        print("\nItems:")

        for item in order["items"]:
            print(
                f"{item['name']} x {item['quantity']} "
                f"= ₹{item['total']}"
            )

        print(f"\nTotal Amount: ₹{order['total']}")
        line()

    except ValueError:
        print("Please enter a valid order ID.")


# -----------------------------
# User Dashboard
# -----------------------------

def user_dashboard(username):
    cart = {}

    while True:
        print("\n")
        print("============================================")
        print("       ONLINE FOOD ORDERING SYSTEM")
        print("============================================")
        print(f"Logged in as: {username}")
        line()

        print("1. View Food Menu")
        print("2. Search Food")
        print("3. Add Food to Cart")
        print("4. View Cart")
        print("5. Remove Food from Cart")
        print("6. Checkout / Place Order")
        print("7. Order History")
        print("8. View Order")
        print("9. Logout")

        line()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_menu()
            pause()

        elif choice == "2":
            search_food()
            pause()

        elif choice == "3":
            add_to_cart(cart)
            pause()

        elif choice == "4":
            view_cart(cart)
            pause()

        elif choice == "5":
            remove_from_cart(cart)
            pause()

        elif choice == "6":
            checkout(username, cart)
            pause()

        elif choice == "7":
            order_history(username)
            pause()

        elif choice == "8":
            view_order()
            pause()

        elif choice == "9":
            print("\nLogged out successfully.")
            break

        else:
            print("\nInvalid choice. Please try again.")


# -----------------------------
# Main Program
# -----------------------------

def main():
    while True:
        print("\n")
        print("============================================")
        print("    ONLINE FOOD ORDERING SIMULATION SYSTEM")
        print("============================================")
        print("1. Register")
        print("2. Login")
        print("3. View Food Menu")
        print("4. Exit")
        line()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register()
            pause()

        elif choice == "2":
            username = login()

            if username:
                user_dashboard(username)

        elif choice == "3":
            display_menu()
            pause()

        elif choice == "4":
            print("\nThank you for using the Online Food Ordering System!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1-4.")


# -----------------------------
# Program Entry Point
# -----------------------------

if __name__ == "__main__":
    main()
