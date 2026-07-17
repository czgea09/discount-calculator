from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


MONEY_PRECISION = Decimal("0.01")


class ValidationError(ValueError):
    """Raised when calculator input is invalid."""


@dataclass(frozen=True)
class DiscountResult:
    """Stores the result of a discount calculation."""

    unit_price: Decimal
    quantity: int
    discount_rate: Decimal
    subtotal: Decimal
    discount_amount: Decimal
    final_amount: Decimal


def parse_decimal(value: str, field_name: str) -> Decimal:
    """
    Convert text input into Decimal.

    Enter numbers without a thousands separator.
    Examples: 20000, 12500.50, or 12,5 for a decimal value.
    """
    normalized = value.strip().replace(",", ".")

    if not normalized:
        raise ValidationError(f"{field_name} wajib diisi.")

    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ValidationError(f"{field_name} harus berupa angka.") from exc


def parse_quantity(value: str) -> int:
    """Validate and convert the quantity input into a positive integer."""
    normalized = value.strip()

    if not normalized:
        raise ValidationError("Quantity wajib diisi.")

    try:
        quantity = int(normalized)
    except ValueError as exc:
        raise ValidationError("Quantity harus berupa bilangan bulat.") from exc

    if quantity <= 0:
        raise ValidationError("Quantity harus lebih besar dari 0.")

    return quantity


def calculate_discount(
    unit_price: Decimal | str | int | float,
    discount_rate: Decimal | str | int | float,
    quantity: int,
) -> DiscountResult:
    """
    Calculate subtotal, discount amount, and final amount.

    Formula:
        subtotal = unit_price × quantity
        discount_amount = subtotal × discount_rate / 100
        final_amount = subtotal - discount_amount
    """
    try:
        price = Decimal(str(unit_price))
        rate = Decimal(str(discount_rate))
    except InvalidOperation as exc:
        raise ValidationError("Price dan discount harus berupa angka.") from exc

    if price <= 0:
        raise ValidationError("Original Price harus lebih besar dari 0.")

    if rate < 0 or rate > 100:
        raise ValidationError("Discount harus berada di antara 0 sampai 100.")

    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        raise ValidationError("Quantity harus berupa bilangan bulat lebih besar dari 0.")

    subtotal = (price * quantity).quantize(MONEY_PRECISION, rounding=ROUND_HALF_UP)
    discount_amount = (
        subtotal * rate / Decimal("100")
    ).quantize(MONEY_PRECISION, rounding=ROUND_HALF_UP)
    final_amount = (subtotal - discount_amount).quantize(
        MONEY_PRECISION, rounding=ROUND_HALF_UP
    )

    return DiscountResult(
        unit_price=price.quantize(MONEY_PRECISION, rounding=ROUND_HALF_UP),
        quantity=quantity,
        discount_rate=rate,
        subtotal=subtotal,
        discount_amount=discount_amount,
        final_amount=final_amount,
    )


def format_rupiah(amount: Decimal) -> str:
    """Format a Decimal value using Indonesian Rupiah formatting."""
    formatted = f"{amount:,.2f}"
    formatted = formatted.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"Rp {formatted}"
