"""Calculator GUI using Tkinter.

Run with:
    python gui.py

This GUI uses the arithmetic functions from `calculator.py`.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import math

from calculator import add, subtract, multiply, divide


class CalculatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg='#202020')

        # Variables
        self.expr = tk.StringVar(value="0")
        self.memory = 0
        self.has_result = False

        self._build_ui()

    def _build_ui(self):
        # Main frame
        main_frame = tk.Frame(self, bg='#202020')
        main_frame.pack(padx=10, pady=10)

        # Display
        display_frame = tk.Frame(main_frame, bg='#202020')
        display_frame.pack(fill='x', pady=(0, 10))

        display = tk.Label(display_frame, textvariable=self.expr, font=("Segoe UI", 36, 'bold'),
                          bg='#202020', fg='#ffffff', anchor='e', height=1)
        display.pack(fill='x')

        # Button frame
        button_frame = tk.Frame(main_frame, bg='#202020')
        button_frame.pack()

        # Button layout (similar to Windows Calculator)
        buttons = [
            ('%', 0, 0), ('CE', 0, 1), ('C', 0, 2), ('⌫', 0, 3),
            ('¹∕x', 1, 0), ('x²', 1, 1), ('√x', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('−', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('±', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3),
        ]

        # Memory buttons (top right)
        mem_buttons = [
            ('MC', 0, 4), ('MR', 1, 4), ('MS', 2, 4), ('M+', 3, 4), ('M−', 4, 4),
        ]

        # Create buttons
        self.buttons = {}
        for text, row, col in buttons + mem_buttons:
            self._create_button(button_frame, text, row, col)

        # Configure grid
        for i in range(6):
            button_frame.rowconfigure(i, weight=1)
        for i in range(5):
            button_frame.columnconfigure(i, weight=1)

    def _create_button(self, parent, text, row, col):
        # Button colors
        if text in ['%', 'CE', 'C', '⌫', '¹∕x', 'x²', '√x', '±']:
            bg = '#d4d4d2'  # Light gray
            fg = '#000000'
        elif text in ['÷', '×', '−', '+', '=']:
            bg = '#ff8c00'  # Orange
            fg = '#ffffff'
        elif text in ['MC', 'MR', 'MS', 'M+', 'M−']:
            bg = '#a6a6a6'  # Gray
            fg = '#000000'
        else:
            bg = '#505050'  # Dark gray
            fg = '#ffffff'

        # Special sizing
        rowspan = 1
        colspan = 1
        if text == '=':
            rowspan = 2
        if text == '0':
            colspan = 2

        btn = tk.Button(parent, text=text, font=('Segoe UI', 14, 'bold'),
                       bg=bg, fg=fg, bd=0, relief='flat', activebackground=bg,
                       activeforeground=fg, command=lambda: self._on_button(text))
        btn.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan,
                sticky='nsew', padx=1, pady=1)

        # Hover effect
        def on_enter(e):
            if bg == '#505050':
                btn.config(bg='#666666')
            elif bg == '#d4d4d2':
                btn.config(bg='#e8e8e8')
            elif bg == '#ff8c00':
                btn.config(bg='#ffa500')
            elif bg == '#a6a6a6':
                btn.config(bg='#b8b8b8')

        def on_leave(e):
            btn.config(bg=bg)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

        self.buttons[text] = btn

    def _on_button(self, ch: str):
        current = self.expr.get()

        if ch == 'C':
            self.expr.set("0")
            self.has_result = False
        elif ch == 'CE':
            self.expr.set("0")
        elif ch == '⌫':
            if len(current) > 1:
                self.expr.set(current[:-1])
            else:
                self.expr.set("0")
        elif ch == '±':
            try:
                val = float(current)
                self.expr.set(str(-val))
            except:
                pass
        elif ch == '=':
            self._calculate()
        elif ch in ['%', '¹∕x', 'x²', '√x']:
            self._special_operation(ch)
        elif ch in ['MC', 'MR', 'MS', 'M+', 'M−']:
            self._memory_operation(ch)
        else:
            # Number or operator
            if self.has_result and ch not in ['+', '-', '×', '÷']:
                self.expr.set(ch)
                self.has_result = False
            elif current == "0" and ch not in ['+', '-', '×', '÷', '.']:
                self.expr.set(ch)
            else:
                self.expr.set(current + ch)

    def _calculate(self):
        expr = self.expr.get().replace('×', '*').replace('÷', '/').replace('−', '-')
        try:
            result = eval(expr)
            self.expr.set(str(result))
            self.has_result = True
        except:
            messagebox.showerror("Error", "Invalid expression")

    def _special_operation(self, op: str):
        try:
            val = float(self.expr.get())
            if op == '%':
                self.expr.set(str(val / 100))
            elif op == '¹∕x':
                if val != 0:
                    self.expr.set(str(1 / val))
                else:
                    messagebox.showerror("Error", "Cannot divide by zero")
            elif op == 'x²':
                self.expr.set(str(val ** 2))
            elif op == '√x':
                if val >= 0:
                    self.expr.set(str(math.sqrt(val)))
                else:
                    messagebox.showerror("Error", "Invalid input for square root")
            self.has_result = True
        except:
            messagebox.showerror("Error", "Invalid input")

    def _memory_operation(self, op: str):
        if op == 'MC':
            self.memory = 0
        elif op == 'MR':
            self.expr.set(str(self.memory))
        elif op == 'MS':
            try:
                self.memory = float(self.expr.get())
            except:
                pass
        elif op == 'M+':
            try:
                self.memory += float(self.expr.get())
            except:
                pass
        elif op == 'M−':
            try:
                self.memory -= float(self.expr.get())
            except:
                pass


def main():
    app = CalculatorGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
