import datetime
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
import os
import requests


def fetch_rate(from_curr, to_curr):
    """Fetch live exchange rate using a free public API"""
    try:
        url = f"https://open.er-api.com/v6/latest/{from_curr}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("result") == "success":
            return data.get("rates", {}).get(to_curr)
        return None
    except Exception as e:
        print("Fetch error:", e)
        return None


class CurrencyConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Xchange")
        self.geometry("400x550")
        self.minsize(400, 500)
        self.resizable(True, True)
        self.configure(bg="#f0f2f5")

        self.currencies = ["USD", "EUR", "GBP", "JPY", "AED", "INR", "CAD", "AUD", "CHF", "CNY"]
        self.config_file = "currency_config.txt"

        default_from, default_to = self._load_defaults()
        self.from_var = tk.StringVar(value=default_from)
        self.to_var = tk.StringVar(value=default_to)
        self.rate_var = tk.StringVar(value="—")
        self.rate_label_var = tk.StringVar(value=f"1 {default_from} =")
        self.time_var = tk.StringVar(value="—")
        self.status_var = tk.StringVar(value="Ready")

        self.auto_refresh_var = tk.BooleanVar(value=False)
        self.frequency_var = tk.StringVar(value="30 seconds")
        self.countdown_var = tk.StringVar(value="")
        self._auto_refresh_job = None
        self._target_time = 0

        self._create_menu()
        self._build_ui()

    def _load_defaults(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        return lines[0].strip(), lines[1].strip()
            except:
                pass
        return "AED", "INR"


    def _create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save History to CSV", command=self.save_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

    def _build_ui(self):
        # Configure grid for resizing
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        main_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1) # History row expands

        # Header
        tk.Label(main_frame, text="Currency Exchange", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#202124").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        # Currency Selection
        sel_frame = tk.Frame(main_frame, bg="#ffffff")
        sel_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        tk.Label(sel_frame, text="From", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#5f6368").grid(row=0, column=0, sticky="w")
        ttk.Combobox(sel_frame, textvariable=self.from_var, values=self.currencies, width=10, state="readonly", font=("Segoe UI", 10)).grid(row=1, column=0, padx=(0, 20), pady=(5, 0), sticky="ew")

        tk.Label(sel_frame, text="To", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#5f6368").grid(row=0, column=1, sticky="w")
        ttk.Combobox(sel_frame, textvariable=self.to_var, values=self.currencies, width=10, state="readonly", font=("Segoe UI", 10)).grid(row=1, column=1, pady=(5, 0), sticky="ew")

        # Rate Display
        info_frame = tk.Frame(main_frame, bg="#f8f9fa", padx=15, pady=15)
        info_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        tk.Label(info_frame, textvariable=self.rate_label_var, font=("Segoe UI", 12), bg="#f8f9fa", fg="#5f6368").pack(anchor="w")
        tk.Label(info_frame, textvariable=self.rate_var, font=("Segoe UI", 24, "bold"), bg="#f8f9fa", fg="#1a73e8").pack(anchor="w")
        tk.Label(info_frame, textvariable=self.time_var, font=("Segoe UI", 9), bg="#f8f9fa", fg="#5f6368").pack(anchor="w", pady=(5, 0))

        # Controls & Auto Refresh
        ctrl_frame = tk.Frame(main_frame, bg="#ffffff")
        ctrl_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.refresh_btn = tk.Button(ctrl_frame, text="Refresh Now", command=self.refresh, bg="#1a73e8", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=5, cursor="hand2")
        self.refresh_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Auto Refresh Options
        ar_frame = tk.LabelFrame(main_frame, text="Auto Refresh", bg="#ffffff", fg="#5f6368", font=("Segoe UI", 9), padx=10, pady=10)
        ar_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        tk.Checkbutton(ar_frame, text="Enable", variable=self.auto_refresh_var, command=self._toggle_auto_refresh, bg="#ffffff", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        tk.Label(ar_frame, textvariable=self.countdown_var, bg="#ffffff", fg="#d93025", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=15)
        
        freq_box = ttk.Combobox(ar_frame, textvariable=self.frequency_var, values=["30 seconds", "60 seconds", "1 hour", "1 day"], width=15)
        freq_box.pack(side=tk.RIGHT)
        freq_box.bind("<<ComboboxSelected>>", self._on_frequency_change)
        freq_box.bind("<Return>", self._on_frequency_change)

        tk.Label(ar_frame, text="Every:", bg="#ffffff", font=("Segoe UI", 9)).pack(side=tk.RIGHT, padx=5)

        # History with Scrollbar
        tk.Label(main_frame, text="History Log", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#202124").grid(row=5, column=0, sticky="nw")
        
        hist_frame = tk.Frame(main_frame, bg="#ffffff")
        hist_frame.grid(row=6, column=0, columnspan=2, sticky="nsew")
        hist_frame.rowconfigure(0, weight=1)
        hist_frame.columnconfigure(0, weight=1)

        self.history = tk.Text(hist_frame, height=5, width=40, font=("Consolas", 9), state=tk.DISABLED, relief="flat", bg="#f1f3f4", padx=5, pady=5)
        self.history.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(hist_frame, orient="vertical", command=self.history.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.history.configure(yscrollcommand=scrollbar.set)

        # Status Bar
        tk.Label(main_frame, textvariable=self.status_var, font=("Segoe UI", 9), bg="#ffffff", fg="#1a73e8").grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def show_about(self):
        messagebox.showinfo("About Xchange", "Xchange v1.0\nYear: 2025\n\nBuilt by @MinusDegree Ltd.")


    def _set_status(self, text):
        self.status_var.set(text)

    def _append_history(self, text):
        self.history.config(state=tk.NORMAL)
        self.history.insert(tk.END, text + "\n")
        self.history.see(tk.END)
        self.history.config(state=tk.DISABLED)

    def refresh(self):
        self._set_status("Fetching...")
        self.refresh_btn.config(state=tk.DISABLED)
        threading.Thread(target=self._fetch_and_update, daemon=True).start()

    def _fetch_and_update(self):
        from_curr = self.from_var.get()
        to_curr = self.to_var.get()
        rate = fetch_rate(from_curr, to_curr)
        ts = datetime.datetime.now(datetime.timezone.utc)

        def update_ui():
            if rate is None:
                self._set_status("Failed to fetch rate")
            else:
                self.rate_label_var.set(f"1 {from_curr} =")
                self.rate_var.set(f"{rate:.6f} {to_curr}")
                ts_str = ts.strftime("%d-%b-%y %H:%M:%S").upper()
                self.time_var.set(ts_str)
                self._append_history(f"{ts_str} — 1 {from_curr} = {rate:.6f} {to_curr}")
                self._set_status("Updated")
            self.refresh_btn.config(state=tk.NORMAL)
            if self.auto_refresh_var.get():
                self._schedule_next_refresh()

        self.after(0, update_ui)

    def _parse_interval(self):
        try:
            val_str = self.frequency_var.get().lower()
            if "second" in val_str:
                return int(val_str.split()[0]) * 1000
            elif "minute" in val_str:
                return int(val_str.split()[0]) * 60000
            elif "hour" in val_str:
                return int(val_str.split()[0]) * 3600000
            elif "day" in val_str:
                return int(val_str.split()[0]) * 86400000
            else:
                return int(val_str) * 1000
        except:
            return 30000  # Default 30s

    def _on_frequency_change(self, event=None):
        if self.auto_refresh_var.get():
            self._schedule_next_refresh()

    def _toggle_auto_refresh(self):
        if self.auto_refresh_var.get():
            self._schedule_next_refresh()
        else:
            if self._auto_refresh_job:
                self.after_cancel(self._auto_refresh_job)
                self._auto_refresh_job = None
                self._set_status("Auto-refresh stopped")
            self.countdown_var.set("")

    def _schedule_next_refresh(self):
        if self._auto_refresh_job:
            self.after_cancel(self._auto_refresh_job)
        ms = self._parse_interval()
        self._target_time = time.time() + (ms / 1000)
        self._countdown_tick()

    def _countdown_tick(self):
        if not self.auto_refresh_var.get():
            return

        remaining = int(self._target_time - time.time())
        if remaining <= 0:
            self.refresh()
        else:
            self.countdown_var.set(f"Refreshing in {remaining}s")
            self._auto_refresh_job = self.after(1000, self._countdown_tick)

    def save_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return

        if self.rate_var.get() == "—":
            messagebox.showwarning("No rate", "Fetch a rate first.")
            return

        try:
            rate = float(self.rate_var.get().split()[0])
            write_header = not os.path.exists(path) or os.path.getsize(path) == 0
            with open(path, "a", encoding="utf-8", newline="") as f:
                if write_header:
                    f.write("timestamp,from,to,rate\n")
                f.write(
                    f"{self.time_var.get()},{self.from_var.get()},"
                    f"{self.to_var.get()},{rate:.6f}\n"
                )
            messagebox.showinfo("Saved", "Rate saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    CurrencyConverter().mainloop()


if __name__ == "__main__":
    main()
