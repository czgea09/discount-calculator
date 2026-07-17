# Python Project — Discount Calculator

Aplikasi desktop sederhana untuk menghitung total harga setelah diskon berdasarkan:

- Original Price
- Discount Rate
- Quantity

GUI dibuat dengan `tkinter`, sedangkan perhitungan uang memakai `Decimal` agar hasil lebih presisi.

## Formula

```text
subtotal = original_price × quantity
discount_amount = subtotal × discount_rate / 100
final_amount = subtotal - discount_amount
```

## Contoh

```text
Original Price : 20000
Discount       : 25
Quantity       : 2

Subtotal       : Rp 40.000,00
Discount       : Rp 10.000,00
Final Amount   : Rp 30.000,00
```

## Struktur Project

```text
discount-calculator/
├── main.py
├── discount_calculator.py
├── requirements.txt
├── .gitignore
├── README.md
└── tests/
    ├── __init__.py
    └── test_discount_calculator.py
```

## Menjalankan Aplikasi

Windows:

```powershell
py main.py
```

Alternatif:

```powershell
python main.py
```

macOS/Linux:

```bash
python3 main.py
```

## Menjalankan Automated Test

Windows:

```powershell
py -m unittest discover -s tests -v
```

macOS/Linux:

```bash
python3 -m unittest discover -s tests -v
```

## Mengecek Tkinter

```powershell
py -m tkinter
```

Apabila muncul jendela demo Tk, berarti Tkinter tersedia.

## Push ke GitHub

Buat repository kosong di GitHub, lalu jalankan:

```bash
git init
git add .
git commit -m "Initial commit: discount calculator"
git branch -M main
git remote add origin https://github.com/USERNAME/discount-calculator.git
git push -u origin main
```

Ganti `USERNAME` dengan username GitHub milikmu.
