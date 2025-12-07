"""Calculator GUI using Tkinter.

Run with:
    python gui.py

This GUI uses the arithmetic functions from `calculator.py`.
"""

import tkinter as tk
from tkinter import messagebox

from calculator import add, subtract, multiply, divide


class CalculatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Calculator")
        self.resizable(False, False)

        self.expr = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        entry = tk.Entry(self, textvariable=self.expr, font=("Segoe UI", 18), bd=4, relief=tk.RIDGE, justify=tk.RIGHT)
        entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
            ('=', 5, 0, 4),
        ]

        for btn in buttons:
            if len(btn) == 4:
                text, r, c, colspan = btn
            else:
                text, r, c = btn
                colspan = 1

            action = (lambda ch=text: self._on_button(ch))
            b = tk.Button(self, text=text, width=5 if colspan==1 else 24, height=2, font=("Segoe UI", 14), command=action)
            b.grid(row=r, column=c, columnspan=colspan, padx=3, pady=3)

    def _on_button(self, ch: str):
        if ch == 'C':
            self.expr.set("")
            return

        if ch == '=':
            self._calculate()
            return

        # Append character
        self.expr.set(self.expr.get() + ch)

    def _calculate(self):
        expr = self.expr.get().strip()
        if not expr:
            return

        # Simple parsing: find operator
        for op in ['+', '-', '*', '/']:
            if op in expr:
                parts = expr.split(op)
                if len(parts) != 2:
                    messagebox.showerror("Error", "Invalid expression")
                    return
                a_str, b_str = parts
                try:
                    a = float(a_str)
                    b = float(b_str)
                except ValueError:
                    messagebox.showerror("Error", "Invalid numbers")
                    return

                try:
                    if op == '+':
                        res = add(a, b)
                    elif op == '-':
                        res = subtract(a, b)
                    elif op == '*':
                        res = multiply(a, b)
                    else:
                        res = divide(a, b)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    return

                # Display result
                # Remove trailing .0 for integers
                if isinstance(res, float) and res.is_integer():
                    res = int(res)
                self.expr.set(str(res))
                return

        messagebox.showerror("Error", "Operator not found. Use +, -, *, /")


def main():
    app = CalculatorGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
