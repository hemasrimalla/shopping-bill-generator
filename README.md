# Shopping Bill Generator (Level 1, Day 15 Internship Task)

A beginner-friendly, interactive command-line application that collects product details, validates user inputs, computes tiered discounts, applies Goods and Services Tax (GST), and prints a formatted itemized receipt in Indian Rupees (₹).

This project relies purely on Python's **Standard Library** with **zero external dependencies**.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Concepts Practiced](#concepts-practiced)
- [Features](#features)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
  - [Prerequisites](#prerequisites)
  - [Running the Program](#running-the-program)
  - [Running the Test Suite](#running-the-test-suite)
- [Pricing & Discount Rules](#pricing--discount-rules)
- [Sample Runs & Outputs](#sample-runs--outputs)
  - [Sample 1: Standard Cart (Rice, Milk, Oil)](#sample-1-standard-cart-rice-milk-oil)
  - [Sample 2: Tier 1 Discount (5% Off for Orders ≥ ₹1,000)](#sample-2-tier-1-discount-5-off-for-orders--1000)
  - [Sample 3: Tier 2 Discount (10% Off for Orders ≥ ₹5,000)](#sample-3-tier-2-discount-10-off-for-orders--5000)
  - [Sample 4: Input Validation & Error Handling](#sample-4-input-validation--error-handling)
  - [Sample 5: Edge Case — Empty Cart](#sample-5-edge-case--empty-cart)
- [Interview Questions & Answers](#interview-questions--answers)
  - [1. Which data structure would you use for product records?](#1-which-data-structure-would-you-use-for-product-records)
  - [2. Why should calculations be separated into functions?](#2-why-should-calculations-be-separated-into-functions)
  - [3. How would you handle invalid quantities?](#3-how-would-you-handle-invalid-quantities)

---

## Project Overview

In retail and point-of-sale (POS) systems, collecting item details, verifying customer input, applying business rules (discounts and taxes), and presenting clear summaries are essential fundamentals.

The **Shopping Bill Generator** models this workflow cleanly in Python:
1. It records items in memory as structured dictionaries inside a list.
2. It interacts through a continuous loop until the user types `done`.
3. It validates product names, quantities, and prices, gracefully recovering from bad inputs using `try-except` blocks.
4. It breaks down subtotal, discount, tax, and final amount into dedicated functions.
5. It formats monetary values consistently with two decimal places and the `₹` symbol.

---

## Concepts Practiced

- **Dictionaries (`dict`):** Used to represent individual product records with descriptive key-value pairs (`name`, `quantity`, `price`).
- **Lists (`list`):** Used as an ordered in-memory cart holding all product dictionaries.
- **Loops (`while`):** Powers the continuous interactive input loop and validation re-prompt loops.
- **Functions & Docstrings:** Clean separation of concerns with modular functions, clear type descriptions, and docstrings.
- **Exception Handling (`try-except`):** Catching `ValueError` when converting strings to integers or floats to prevent runtime crashes.
- **String Formatting:** f-strings with alignment (`<`, `>`), fixed-width columns, and float precision formatting (`:.2f`).

---

## Features

- **No Third-Party Dependencies:** Implemented strictly using the Python Standard Library.
- **Structured Data Model:** Each item is stored as `{"name": str, "quantity": int, "price": float}` in a list.
- **Robust Input Validation:**
  - Names cannot be empty or pure whitespace.
  - Quantity must be a positive whole integer ($> 0$).
  - Price must be a positive number ($> 0$).
  - Non-numeric input raises a handled `ValueError` with an informative error message instead of crashing.
- **Tiered Discount Engine:**
  - Orders $\ge ₹5,000$: **10% discount**
  - Orders $\ge ₹1,000$ (and $< ₹5,000$): **5% discount**
  - Orders $< ₹1,000$: **0% discount**
- **Tax Calculation (GST):**
  - Calculates 18% GST on the discounted taxable amount ($(\text{subtotal} - \text{discount}) \times 0.18$).
- **Formatted Itemized Bill:** Aligns column headers, item numbers, names, quantities, individual prices, row totals, and summary totals across a consistent 47-character width.
- **Graceful Edge-Case Handling:** Safely handles empty shopping carts when the user inputs `done` immediately.
- **Cross-Platform UTF-8 Compatibility:** Reconfigures console stdout on Windows to guarantee correct rendering of the Indian Rupee (`₹`) symbol.
- **Automated Test Suite:** Complete test suite covering math calculations, discount boundaries, input validation retries, and formatting.

---

## Project Structure

```text
shopping-bill-generator/
├── .gitignore             # Ignores Python bytecode, cache, and virtual environments
├── README.md              # Documentation, formulas, usage examples, and interview Q&A
├── shopping_bill.py       # Main program and calculation logic
└── test_shopping_bill.py  # Automated unit test suite (16 tests)
```

---

## How to Run

### Prerequisites
- Python 3.8 or higher installed on your computer.
- Terminal or command prompt (PowerShell, Command Prompt, bash, or zsh).

### Running the Program
Open your terminal, navigate to the project directory, and run:

```bash
python shopping_bill.py
```

Follow the prompts on your screen:
1. Enter the product name (e.g., `Rice`).
2. Enter the quantity as a positive integer (e.g., `2`).
3. Enter the unit price (e.g., `60.00`).
4. Repeat for other products.
5. When finished, enter `done` as the product name to generate the bill.

### Running the Test Suite
To run all 16 automated unit tests:

```bash
python test_shopping_bill.py
```

Expected output:
```text
................
----------------------------------------------------------------------
Ran 16 tests in 0.002s

OK
```

---

## Pricing & Discount Rules

| Rule | Formula / Condition | Rate |
| :--- | :--- | :--- |
| **Subtotal** | $\sum (\text{quantity}_i \times \text{price}_i)$ | — |
| **Tier 1 Discount** | $\text{Subtotal} \ge ₹5,000$ | $10\%$ of Subtotal |
| **Tier 2 Discount** | $₹1,000 \le \text{Subtotal} < ₹5,000$ | $5\%$ of Subtotal |
| **Base Discount** | $\text{Subtotal} < ₹1,000$ | $0\%$ |
| **Taxable Amount** | $\text{Subtotal} - \text{Discount}$ | — |
| **GST Tax** | $\text{Taxable Amount} \times 0.18$ | $18\%$ GST |
| **Final Amount** | $\text{Subtotal} - \text{Discount} + \text{Tax}$ | Rounded to 2 decimals |

---

## Sample Runs & Outputs

### Sample 1: Standard Cart (Rice, Milk, Oil)
Sample input:
- Rice: 2 units @ ₹60.00 = ₹120.00
- Milk: 3 units @ ₹25.00 = ₹75.00
- Oil: 1 unit @ ₹150.00 = ₹150.00

```text
===============================================
       WELCOME TO SHOPPING BILL GENERATOR      
===============================================
Add items to your cart.
Type 'done' as the product name when you are finished.

Enter product name (or type 'done' to finish): Rice
Enter quantity for 'Rice': 2
Enter price per unit for 'Rice' (₹): 60
-> Added 2x 'Rice' @ ₹60.00 each.

Enter product name (or type 'done' to finish): Milk
Enter quantity for 'Milk': 3
Enter price per unit for 'Milk' (₹): 25
-> Added 3x 'Milk' @ ₹25.00 each.

Enter product name (or type 'done' to finish): Oil
Enter quantity for 'Oil': 1
Enter price per unit for 'Oil' (₹): 150
-> Added 1x 'Oil' @ ₹150.00 each.

Enter product name (or type 'done' to finish): done

================ SHOPPING BILL ================
No.  Item             Qty      Price      Total
1    Rice               2     ₹60.00    ₹120.00
2    Milk               3     ₹25.00     ₹75.00
3    Oil                1    ₹150.00    ₹150.00
-----------------------------------------------
Subtotal:                               ₹345.00
Discount (0%):                           -₹0.00
Tax (18%):                               ₹62.10
FINAL AMOUNT:                           ₹407.10
===============================================
Thank you for shopping with us!
```

---

### Sample 2: Tier 1 Discount (5% Off for Orders ≥ ₹1,000)
Sample input:
- Basmati Rice: 10 units @ ₹120.00 = ₹1,200.00
- Olive Oil: 2 units @ ₹850.00 = ₹1,700.00
- Subtotal: ₹2,900.00 ($\ge ₹1,000 \implies 5\%$ discount = ₹145.00)
- Taxable amount: ₹2,755.00
- GST (18%): ₹495.90
- Final Amount: ₹3,250.90

```text
================ SHOPPING BILL ================
No.  Item             Qty      Price      Total
1    Basmati Rice      10    ₹120.00   ₹1200.00
2    Olive Oil          2    ₹850.00   ₹1700.00
-----------------------------------------------
Subtotal:                              ₹2900.00
Discount (5%):                         -₹145.00
Tax (18%):                              ₹495.90
FINAL AMOUNT:                          ₹3250.90
===============================================
Thank you for shopping with us!
```

---

### Sample 3: Tier 2 Discount (10% Off for Orders ≥ ₹5,000)
Sample input:
- Smartphone: 1 unit @ ₹6,000.00
- Subtotal: ₹6,000.00 ($\ge ₹5,000 \implies 10\%$ discount = ₹600.00)
- Taxable amount: ₹5,400.00
- GST (18%): ₹972.00
- Final Amount: ₹6,372.00

```text
================ SHOPPING BILL ================
No.  Item             Qty      Price      Total
1    Smartphone         1   ₹6000.00   ₹6000.00
-----------------------------------------------
Subtotal:                              ₹6000.00
Discount (10%):                        -₹600.00
Tax (18%):                              ₹972.00
FINAL AMOUNT:                          ₹6372.00
===============================================
Thank you for shopping with us!
```

---

### Sample 4: Input Validation & Error Handling
Demonstrating resilience against empty names, letters, negative numbers, and zeros:

```text
Enter product name (or type 'done' to finish):    
Error: Product name cannot be empty. Please enter a valid name.

Enter product name (or type 'done' to finish): Apple
Enter quantity for 'Apple': abc
Error: Invalid quantity. Please enter a whole number (e.g., 1, 2, 3).

Enter quantity for 'Apple': -2
Error: Quantity must be a positive whole number (> 0). Please try again.

Enter quantity for 'Apple': 0
Error: Quantity must be a positive whole number (> 0). Please try again.

Enter quantity for 'Apple': 4
Enter price per unit for 'Apple' (₹): xyz
Error: Invalid price. Please enter a valid numeric value (e.g., 60.00).

Enter price per unit for 'Apple' (₹): -10
Error: Price must be a positive number (> 0). Please try again.

Enter price per unit for 'Apple' (₹): 25.50
-> Added 4x 'Apple' @ ₹25.50 each.
```

---

### Sample 5: Edge Case — Empty Cart
If the user starts the program and immediately types `done`:

```text
===============================================
       WELCOME TO SHOPPING BILL GENERATOR      
===============================================
Add items to your cart.
Type 'done' as the product name when you are finished.

Enter product name (or type 'done' to finish): done

No products were entered. No bill to generate.
Thank you for shopping with us!
```

---

## Interview Questions & Answers

### 1. Which data structure would you use for product records?
> **Answer:**
> For an individual product record, a **Python dictionary (`dict`)** is the ideal data structure. Dictionaries use key-value pairs (e.g., `{"name": "Rice", "quantity": 2, "price": 60.0}`), allowing each property to be labeled clearly with self-documenting semantic keys. This avoids the ambiguity of tuples or lists where data must be accessed by arbitrary indices (like `product[0]` or `product[2]`).
>
> To store the complete collection of product records, a **Python list (`list`)** is the best container. Lists maintain insertion order, dynamically expand as the user adds new items, allow duplicates if needed, and are easily iterable for computing sums and printing itemized rows.
>
> *(In production-grade applications, Python's `dataclass` or `typing.NamedTuple` can also be used for static type checking, immutability, and dot-notation access like `product.price`.)*

---

### 2. Why should calculations be separated into functions?
> **Answer:**
> 1. **Single Responsibility Principle (SRP):** Each function (`calculate_subtotal`, `calculate_discount`, `calculate_tax`, `calculate_final_amount`) is responsible for exactly one mathematical task, making the codebase clean, readable, and easy to reason about.
> 2. **Reusability:** A tax or discount calculation function can be reused throughout an entire application (e.g., cart preview, order confirmation, invoice generation, checkout API) without duplicating formulas.
> 3. **Isolated Testability:** Dedicated pure calculation functions with explicit inputs and return values can be thoroughly unit tested with automated assertions across boundaries and edge cases, without needing mock user input or capturing console text.
> 4. **Maintainability:** When business rules change (such as a promotional discount tier update or a GST rate revision from 18% to 12%), developers only modify a single isolated function without risking regressions in UI rendering or data collection logic.

---

### 3. How would you handle invalid quantities?
> **Answer:**
> Handling invalid quantities requires a two-step validation approach combined with a friendly user experience:
> 1. **Type Validation with `try-except`:** Wrap the conversion `int(input_string)` in a `try...except ValueError` block. This catches non-numeric inputs (such as `"five"`, `"abc"`, symbols, or floating-point numbers like `"2.5"`).
> 2. **Business Rule / Range Validation:** Once parsed successfully as an integer, verify that `quantity > 0`. Zero and negative numbers are rejected because a purchase quantity must be a positive whole number.
> 3. **Non-Crashing Re-Prompt Loop:** Instead of letting the program crash with an unhandled exception or aborting the entire session, enclose the prompt in a `while True:` loop. Display an informative error message explaining the expected format (e.g., `"Error: Quantity must be a positive whole number (> 0). Please try again."`) and re-prompt the user until valid input is received.
