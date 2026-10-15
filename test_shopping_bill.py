"""
Test Suite for Shopping Bill Generator
--------------------------------------
Validates subtotal calculations, tiered discount thresholds, GST tax computation,
final amount formulas, edge cases (empty cart), and input validation routines.
"""

import unittest
from unittest.mock import patch
import io
import sys

from shopping_bill import (
    calculate_subtotal,
    calculate_discount,
    calculate_tax,
    calculate_final_amount,
    get_product_input,
    print_bill,
    main,
)


class TestShoppingBillCalculations(unittest.TestCase):
    """Test suite for mathematical and business logic calculations."""

    def test_calculate_subtotal_empty(self):
        """Empty products list should yield a subtotal of 0.0."""
        self.assertEqual(calculate_subtotal([]), 0.0)

    def test_calculate_subtotal_single_item(self):
        """Single item subtotal calculation."""
        products = [{"name": "Rice", "quantity": 2, "price": 60.0}]
        self.assertEqual(calculate_subtotal(products), 120.0)

    def test_calculate_subtotal_multiple_items(self):
        """Multiple items subtotal matching prompt sample data."""
        products = [
            {"name": "Rice", "quantity": 2, "price": 60.0},
            {"name": "Milk", "quantity": 3, "price": 25.0},
            {"name": "Oil", "quantity": 1, "price": 150.0},
        ]
        # (2 * 60) + (3 * 25) + (1 * 150) = 120 + 75 + 150 = 345.0
        self.assertEqual(calculate_subtotal(products), 345.0)

    def test_calculate_discount_below_1000(self):
        """Subtotals under ₹1000 receive 0% discount."""
        self.assertEqual(calculate_discount(0.0), 0.0)
        self.assertEqual(calculate_discount(345.0), 0.0)
        self.assertEqual(calculate_discount(999.99), 0.0)

    def test_calculate_discount_5_percent_tier(self):
        """Subtotals between ₹1000 and ₹4999.99 receive 5% discount."""
        # Exact boundary at 1000: 5% of 1000 = 50.0
        self.assertEqual(calculate_discount(1000.0), 50.0)
        # Mid-tier: 5% of 2500 = 125.0
        self.assertEqual(calculate_discount(2500.0), 125.0)
        # Upper boundary: 5% of 4999.0 = 249.95
        self.assertEqual(calculate_discount(4999.0), 249.95)

    def test_calculate_discount_10_percent_tier(self):
        """Subtotals of ₹5000 or more receive 10% discount."""
        # Exact boundary at 5000: 10% of 5000 = 500.0
        self.assertEqual(calculate_discount(5000.0), 500.0)
        # Higher values: 10% of 10000 = 1000.0
        self.assertEqual(calculate_discount(10000.0), 1000.0)

    def test_calculate_tax_default_gst(self):
        """Tax should default to 18% of taxable amount."""
        self.assertEqual(calculate_tax(0.0), 0.0)
        self.assertEqual(calculate_tax(100.0), 18.0)
        # 345.0 * 0.18 = 62.10
        self.assertEqual(calculate_tax(345.0), 62.10)
        # Taxable amount with discount: 1000 - 50 = 950 -> 950 * 0.18 = 171.0
        self.assertEqual(calculate_tax(950.0), 171.0)

    def test_calculate_tax_custom_rate(self):
        """Tax should correctly apply custom rate when specified."""
        self.assertEqual(calculate_tax(200.0, rate=0.05), 10.0)
        self.assertEqual(calculate_tax(200.0, rate=0.12), 24.0)

    def test_calculate_tax_negative_amount(self):
        """Negative amount should yield 0.0 tax."""
        self.assertEqual(calculate_tax(-50.0), 0.0)

    def test_calculate_final_amount(self):
        """Final amount formula: subtotal - discount + tax."""
        # Case 1: No discount
        # 345.0 - 0.0 + 62.10 = 407.10
        self.assertEqual(calculate_final_amount(345.0, 0.0, 62.10), 407.10)

        # Case 2: 5% discount
        # 1000.0 - 50.0 + 171.0 = 1121.00
        self.assertEqual(calculate_final_amount(1000.0, 50.0, 171.0), 1121.00)

        # Case 3: 10% discount
        # 5000.0 - 500.0 + 810.0 = 5310.00
        self.assertEqual(calculate_final_amount(5000.0, 500.0, 810.0), 5310.00)


class TestShoppingBillOutputAndInput(unittest.TestCase):
    """Test suite for user input handling, validation, and bill output."""

    @patch("builtins.input", side_effect=["done"])
    def test_get_product_input_immediate_done(self, mock_input):
        """Typing 'done' immediately should return None."""
        result = get_product_input()
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["Rice", "2", "60.0"])
    def test_get_product_input_valid(self, mock_input):
        """Valid inputs should produce a correctly-typed product dictionary."""
        result = get_product_input()
        self.assertEqual(
            result,
            {"name": "Rice", "quantity": 2, "price": 60.0}
        )
        self.assertIsInstance(result["quantity"], int)
        self.assertIsInstance(result["price"], float)

    @patch("builtins.input", side_effect=[
        "", "   ", "Wheat Flour",   # Empty names then valid
        "abc", "-5", "0", "3",      # Invalid quantities then valid
        "xyz", "-20", "0", "45.5"   # Invalid prices then valid
    ])
    def test_get_product_input_validation_retry(self, mock_input):
        """Re-prompts on empty name, non-positive or non-numeric quantities and prices."""
        captured_output = io.StringIO()
        with patch("sys.stdout", captured_output):
            result = get_product_input()
        self.assertEqual(
            result,
            {"name": "Wheat Flour", "quantity": 3, "price": 45.5}
        )
        output = captured_output.getvalue()
        self.assertIn("Error: Product name cannot be empty", output)
        self.assertIn("Error: Invalid quantity", output)
        self.assertIn("Error: Quantity must be a positive whole number", output)
        self.assertIn("Error: Invalid price", output)
        self.assertIn("Error: Price must be a positive number", output)

    def test_print_bill_formatting(self):
        """Verify that print_bill generates the expected format and content."""
        products = [
            {"name": "Rice", "quantity": 2, "price": 60.0},
            {"name": "Milk", "quantity": 3, "price": 25.0},
            {"name": "Oil", "quantity": 1, "price": 150.0},
        ]
        subtotal = 345.0
        discount = 0.0
        tax = 62.10
        final_amount = 407.10

        captured_output = io.StringIO()
        with patch("sys.stdout", captured_output):
            print_bill(products, subtotal, discount, tax, final_amount)

        output = captured_output.getvalue()
        self.assertIn("================ SHOPPING BILL ================", output)
        self.assertIn("No.  Item", output)
        self.assertIn("Rice", output)
        self.assertIn("Milk", output)
        self.assertIn("Oil", output)
        self.assertIn("Subtotal:", output)
        self.assertIn("₹345.00", output)
        self.assertIn("Discount (0%):", output)
        self.assertIn("-₹0.00", output)
        self.assertIn("Tax (18%):", output)
        self.assertIn("₹62.10", output)
        self.assertIn("FINAL AMOUNT:", output)
        self.assertIn("₹407.10", output)
        self.assertIn("Thank you for shopping with us!", output)

    @patch("builtins.input", side_effect=["done"])
    def test_main_empty_cart(self, mock_input):
        """main() handles empty cart by exiting gracefully without generating bill."""
        captured_output = io.StringIO()
        with patch("sys.stdout", captured_output):
            main()
        output = captured_output.getvalue()
        self.assertIn("No products were entered. No bill to generate.", output)

    @patch("builtins.input", side_effect=[
        "Rice", "2", "60",
        "Milk", "3", "25",
        "Oil", "1", "150",
        "done"
    ])
    def test_main_full_workflow_sample(self, mock_input):
        """main() correctly executes full sample workflow with 3 products."""
        captured_output = io.StringIO()
        with patch("sys.stdout", captured_output):
            main()
        output = captured_output.getvalue()
        self.assertIn("SHOPPING BILL", output)
        self.assertIn("₹345.00", output)
        self.assertIn("₹407.10", output)


if __name__ == "__main__":
    unittest.main()
