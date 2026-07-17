from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from discount_calculator import (
    ValidationError,
    calculate_discount,
    format_rupiah,
    parse_decimal,
    parse_quantity,
)


class DiscountCalculatorApp:
    """Tkinter GUI for the Discount Calculator project."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Discount Calculator")
        self.root.geometry("460x500")
        self.root.resizable(False, False)

        self.price_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1")

        self.subtotal_var = tk.StringVar(value="Rp 0,00")
        self.discount_amount_var = tk.StringVar(value="Rp 0,00")
        self.final_amount_var = tk.StringVar(value="Rp 0,00")

        self._configure_style()
        self._build_interface()

        self.root.bind("<Return>", lambda _event: self.calculate())
        self.root.bind("<Escape>", lambda _event: self.reset())

    def _configure_style(self) -> None:
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 9))
        style.configure("Field.TLabel", font=("Segoe UI", 10, "bold"))
        style.configure("ResultTitle.TLabel", font=("Segoe UI", 10))
        style.configure("Final.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))

    def _build_interface(self) -> None:
        container = ttk.Frame(self.root, padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Discount Calculator",
            style="Title.TLabel",
        ).pack(pady=(0, 4))

        ttk.Label(
            container,
            text="Hitung total harga setelah diskon",
            style="Subtitle.TLabel",
        ).pack(pady=(0, 18))

        form = ttk.Frame(container)
        form.pack(fill="x")

        self._create_input(
            parent=form,
            row=0,
            label="Original Price",
            variable=self.price_var,
            placeholder="Contoh: 20000",
        )
        self._create_input(
            parent=form,
            row=1,
            label="Discount (%)",
            variable=self.discount_var,
            placeholder="Contoh: 25",
        )
        self._create_input(
            parent=form,
            row=2,
            label="Quantity",
            variable=self.quantity_var,
            placeholder="Contoh: 2",
        )

        button_frame = ttk.Frame(container)
        button_frame.pack(fill="x", pady=18)

        ttk.Button(
            button_frame,
            text="Calculate",
            command=self.calculate,
            style="Primary.TButton",
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset,
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))

        ttk.Separator(container).pack(fill="x", pady=(0, 14))

        result_frame = ttk.Frame(container)
        result_frame.pack(fill="x")

        self._create_result_row(
            result_frame, 0, "Subtotal", self.subtotal_var
        )
        self._create_result_row(
            result_frame, 1, "Discount Amount", self.discount_amount_var
        )

        ttk.Separator(result_frame).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=10
        )

        ttk.Label(
            result_frame,
            text="Final Amount",
            style="ResultTitle.TLabel",
        ).grid(row=3, column=0, sticky="w")

        ttk.Label(
            result_frame,
            textvariable=self.final_amount_var,
            style="Final.TLabel",
        ).grid(row=3, column=1, sticky="e")

        result_frame.columnconfigure(1, weight=1)

    @staticmethod
    def _create_input(
        parent: ttk.Frame,
        row: int,
        label: str,
        variable: tk.StringVar,
        placeholder: str,
    ) -> None:
        ttk.Label(parent, text=label, style="Field.TLabel").grid(
            row=row * 2,
            column=0,
            sticky="w",
            pady=(0 if row == 0 else 10, 4),
        )

        entry = ttk.Entry(parent, textvariable=variable, font=("Segoe UI", 11))
        entry.grid(row=row * 2 + 1, column=0, sticky="ew")

        ttk.Label(parent, text=placeholder, style="Subtitle.TLabel").grid(
            row=row * 2 + 1,
            column=1,
            sticky="w",
            padx=(10, 0),
        )

        parent.columnconfigure(0, weight=1)

    @staticmethod
    def _create_result_row(
        parent: ttk.Frame,
        row: int,
        label: str,
        variable: tk.StringVar,
    ) -> None:
        ttk.Label(parent, text=label).grid(
            row=row, column=0, sticky="w", pady=3
        )
        ttk.Label(parent, textvariable=variable).grid(
            row=row, column=1, sticky="e", pady=3
        )

    def calculate(self) -> None:
        """Read form input, calculate the result, and update the GUI."""
        try:
            price = parse_decimal(self.price_var.get(), "Original Price")
            discount = parse_decimal(self.discount_var.get(), "Discount")
            quantity = parse_quantity(self.quantity_var.get())

            result = calculate_discount(price, discount, quantity)

            self.subtotal_var.set(format_rupiah(result.subtotal))
            self.discount_amount_var.set(format_rupiah(result.discount_amount))
            self.final_amount_var.set(format_rupiah(result.final_amount))

        except ValidationError as exc:
            messagebox.showerror("Input tidak valid", str(exc))

    def reset(self) -> None:
        """Clear all input fields and reset the displayed result."""
        self.price_var.set("")
        self.discount_var.set("")
        self.quantity_var.set("1")
        self.subtotal_var.set("Rp 0,00")
        self.discount_amount_var.set("Rp 0,00")
        self.final_amount_var.set("Rp 0,00")


def main() -> None:
    root = tk.Tk()
    DiscountCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
