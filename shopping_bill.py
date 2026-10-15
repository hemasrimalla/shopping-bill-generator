"""
Shopping Bill Generator
-----------------------
A beginner-friendly command-line application that collects product details
(name, quantity, price), validates user input, calculates subtotal, tiered
discounts, GST tax, and prints an itemized bill formatted in Indian Rupees (₹).
"""

import sys

# Ensure UTF-8 output encoding for terminals on Windows that default to cp1252
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def get_product_input():
    """
    Prompt the user to enter details for a single product with input validation.

    Prompts for:
    - Product name: Non-empty string. Typing 'done' finishes product entry.
    - Quantity: Must be a positive whole number (integer > 0).
    - Price: Must be a positive number (float > 0).

    Uses try-except blocks to catch ValueError on invalid conversions and
    prompts the user again until valid values are provided.

    Returns:
        dict: Product record containing 'name' (str), 'quantity' (int), 'price' (float).
        None: If the user inputs 'done' to indicate they are finished adding items.
    """
    # 1. Prompt for product name
    while True:
        name = input("Enter product name (or type 'done' to finish): ").strip()

        # Check if the user is finished
        if name.lower() == "done":
            return None

        # Validate that product name is not empty
        if not name:
            print("Error: Product name cannot be empty. Please enter a valid name.\n")
            continue

        break

    # 2. Prompt for quantity (must be positive integer)
    while True:
        qty_input = input(f"Enter quantity for '{name}': ").strip()
        try:
            quantity = int(qty_input)
            if quantity <= 0:
                print("Error: Quantity must be a positive whole number (> 0). Please try again.\n")
                continue
            break
        except ValueError:
            print("Error: Invalid quantity. Please enter a whole number (e.g., 1, 2, 3).\n")

    # 3. Prompt for price per unit (must be positive float)
    while True:
        price_input = input(f"Enter price per unit for '{name}' (₹): ").strip()
        try:
            price = float(price_input)
            if price <= 0:
                print("Error: Price must be a positive number (> 0). Please try again.\n")
                continue
            break
        except ValueError:
            print("Error: Invalid price. Please enter a valid numeric value (e.g., 60.00).\n")

    # Return product dictionary
    return {
        "name": name,
        "quantity": quantity,
        "price": price,
    }


def calculate_subtotal(products):
    """
    Calculate the subtotal amount for all items in the products list.

    Iterates through the list of product dictionaries and computes
    the sum of (quantity * price) for each product.

    Args:
        products (list): A list of dictionaries, each containing
                         'quantity' (int) and 'price' (float).

    Returns:
        float: The sum of (quantity * price) rounded to 2 decimal places.
    """
    subtotal = sum(item["quantity"] * item["price"] for item in products)
    return round(subtotal, 2)


def calculate_discount(subtotal):
    """
    Calculate the discount amount based on the subtotal.

    Tiered discount logic:
    - 10% discount for orders of ₹5,000 or above.
    - 5% discount for orders of ₹1,000 or above (up to ₹4,999.99).
    - 0% discount for orders below ₹1,000.

    Args:
        subtotal (float): The total price before discounts and taxes.

    Returns:
        float: The calculated discount amount rounded to 2 decimal places.
    """
    if subtotal >= 5000.0:
        rate = 0.10
    elif subtotal >= 1000.0:
        rate = 0.05
    else:
        rate = 0.00

    return round(subtotal * rate, 2)


def calculate_tax(amount, rate=0.18):
    """
    Calculate the tax (GST) on the given taxable amount.

    Tax is calculated on the discounted amount (subtotal - discount).

    Args:
        amount (float): The taxable amount after applying discount.
        rate (float, optional): Tax rate as a decimal. Defaults to 0.18 (18% GST).

    Returns:
        float: The calculated tax amount rounded to 2 decimal places.
    """
    if amount <= 0:
        return 0.0
    return round(amount * rate, 2)


def calculate_final_amount(subtotal, discount, tax):
    """
    Calculate the final payable amount after applying discount and adding tax.

    Formula: final_amount = subtotal - discount + tax

    Args:
        subtotal (float): Total price of items before discount.
        discount (float): Discount amount deducted from subtotal.
        tax (float): Tax amount added to the discounted subtotal.

    Returns:
        float: The final payable amount rounded to 2 decimal places.
    """
    return round(subtotal - discount + tax, 2)


def print_bill(products, subtotal, discount, tax, final_amount):
    """
    Print an itemized, beautifully formatted shopping bill to the console.

    Formats all monetary values to 2 decimal places with the Indian Rupee (₹) symbol.
    Displays:
    - Header banner
    - Table column headers (No., Item, Qty, Price, Total)
    - Itemized rows
    - Divider
    - Subtotal
    - Discount with percentage
    - Tax (18% GST)
    - Final Amount
    - Footer thank you note

    Args:
        products (list): List of product dictionaries with 'name', 'quantity', 'price'.
        subtotal (float): Subtotal before discount and tax.
        discount (float): Discount amount deducted.
        tax (float): Tax amount added.
        final_amount (float): Net total payable amount.
    """
    bill_width = 47
    header_banner = "================ SHOPPING BILL ================"
    divider = "-" * bill_width
    footer_banner = "=" * bill_width

    # Print header
    print(header_banner)

    # Column header line (width 47)
    # No.(5) + Item(14) + Qty(6) + Price(11) + Total(11) = 47
    print(f"{'No.':<5}{'Item':<14}{'Qty':>6}{'Price':>11}{'Total':>11}")

    # Print item rows
    for index, item in enumerate(products, start=1):
        name = item["name"]
        # Truncate very long names with ellipsis so table alignment is preserved
        display_name = (name[:11] + "..") if len(name) > 13 else name
        qty = item["quantity"]
        price_str = f"₹{item['price']:.2f}"
        item_total = qty * item["price"]
        item_total_str = f"₹{item_total:.2f}"

        print(f"{index:<5}{display_name:<14}{qty:>6}{price_str:>11}{item_total_str:>11}")

    # Print divider
    print(divider)

    # Determine discount percentage label
    if subtotal > 0 and discount > 0:
        discount_pct = int(round((discount / subtotal) * 100))
        discount_label = f"Discount ({discount_pct}%):"
    else:
        discount_label = "Discount (0%):"

    # Format monetary summary lines
    subtotal_str = f"₹{subtotal:.2f}"
    discount_str = f"-₹{discount:.2f}"
    tax_str = f"₹{tax:.2f}"
    final_str = f"₹{final_amount:.2f}"

    # Print summary rows aligned to right margin
    print(f"{'Subtotal:':<25}{subtotal_str:>22}")
    print(f"{discount_label:<25}{discount_str:>22}")
    print(f"{'Tax (18%):':<25}{tax_str:>22}")
    print(f"{'FINAL AMOUNT:':<25}{final_str:>22}")

    # Print footer banner
    print(footer_banner)
    print("Thank you for shopping with us!")


def main():
    """
    Main execution entry point for the Shopping Bill Generator application.

    Orchestrates the entire shopping workflow:
    1. Welcomes the user and explains input conventions.
    2. Repeatedly prompts for product items until user types 'done'.
    3. Handles the edge case of no products entered.
    4. Computes subtotal, discount, tax, and final amount.
    5. Prints the itemized receipt.
    """
    print("===============================================")
    print("       WELCOME TO SHOPPING BILL GENERATOR      ")
    print("===============================================")
    print("Add items to your cart.")
    print("Type 'done' as the product name when you are finished.\n")

    products = []

    # Loop to continuously add products
    while True:
        product = get_product_input()
        if product is None:
            # User typed 'done'
            break

        products.append(product)
        print(f"-> Added {product['quantity']}x '{product['name']}' @ ₹{product['price']:.2f} each.\n")

    # Edge case: No products entered
    if not products:
        print("\nNo products were entered. No bill to generate.")
        print("Thank you for shopping with us!")
        return

    # Calculations
    subtotal = calculate_subtotal(products)
    discount = calculate_discount(subtotal)
    discounted_amount = subtotal - discount
    tax = calculate_tax(discounted_amount, rate=0.18)
    final_amount = calculate_final_amount(subtotal, discount, tax)

    # Output formatted bill
    print()
    print_bill(products, subtotal, discount, tax, final_amount)


if __name__ == "__main__":
    main()
