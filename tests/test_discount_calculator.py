import unittest
from decimal import Decimal

from discount_calculator import (
    ValidationError,
    calculate_discount,
    format_rupiah,
    parse_decimal,
    parse_quantity,
)


class DiscountCalculatorTests(unittest.TestCase):
    def test_typical_calculation(self):
        result = calculate_discount(
            unit_price=Decimal("20000"),
            discount_rate=Decimal("25"),
            quantity=2,
        )

        self.assertEqual(result.subtotal, Decimal("40000.00"))
        self.assertEqual(result.discount_amount, Decimal("10000.00"))
        self.assertEqual(result.final_amount, Decimal("30000.00"))

    def test_zero_discount(self):
        result = calculate_discount("15000", "0", 3)

        self.assertEqual(result.subtotal, Decimal("45000.00"))
        self.assertEqual(result.discount_amount, Decimal("0.00"))
        self.assertEqual(result.final_amount, Decimal("45000.00"))

    def test_full_discount(self):
        result = calculate_discount("50000", "100", 1)

        self.assertEqual(result.final_amount, Decimal("0.00"))

    def test_decimal_rounding(self):
        result = calculate_discount("9999.99", "12.5", 1)

        self.assertEqual(result.discount_amount, Decimal("1250.00"))
        self.assertEqual(result.final_amount, Decimal("8749.99"))

    def test_invalid_price(self):
        with self.assertRaises(ValidationError):
            calculate_discount("0", "10", 1)

    def test_invalid_discount_rate(self):
        with self.assertRaises(ValidationError):
            calculate_discount("10000", "101", 1)

    def test_invalid_quantity(self):
        with self.assertRaises(ValidationError):
            calculate_discount("10000", "10", 0)

    def test_parse_input(self):
        self.assertEqual(parse_decimal("12,5", "Discount"), Decimal("12.5"))
        self.assertEqual(parse_quantity("4"), 4)

    def test_rupiah_format(self):
        self.assertEqual(format_rupiah(Decimal("30000")), "Rp 30.000,00")


if __name__ == "__main__":
    unittest.main()
