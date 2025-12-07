"""AED -> INR GUI

Simple Tkinter-based interface to display live AED -> INR rates.

Features:
- Display latest rate and timestamp
- Manual refresh
- Auto-refresh at user-specified interval
- Append rate to CSV file via Save button
- History view
"""

import datetime
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from aed_to_inr import fetch_rate


class AEDGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AED → INR Live Rate")
        self.resizable(False, False)

        self.rate_var = tk.StringVar(value="—")
        self.time_var = tk.StringVar(value="—")
        self.status_var = tk.StringVar(value="Ready")
        self.interval_var = tk.IntVar(value=60)
        self.auto_refresh_job = None

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self, padx=12, pady=12)
        frame.pack(fill=tk.BOTH, expand=True)

        # Rate display
        tk.Label(frame, text="1 AED =", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w")
        tk.Label(frame, textvariable=self.rate_var, font=("Segoe UI", 20, "bold"), fg="#1a73e8").grid(row=0, column=1, sticky="w")

        # Timestamp
        tk.Label(frame, text="Last updated:", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w")
        tk.Label(frame, textvariable=self.time_var, font=("Segoe UI", 9)).grid(row=1, column=1, sticky="w")

        # Controls
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(8, 0), sticky="w")

        self.refresh_btn = tk.Button(btn_frame, text="Refresh", width=10, command=self.refresh)
        self.refresh_btn.grid(row=0, column=0, padx=(0, 6))

        self.auto_btn = tk.Button(btn_frame, text="Start Auto", width=10, command=self.toggle_auto)
        self.auto_btn.grid(row=0, column=1, padx=(0, 6))

        tk.Label(btn_frame, text="Interval (s):").grid(row=0, column=2, padx=(6, 2))
        self.interval_entry = tk.Entry(btn_frame, textvariable=self.interval_var, width=6)
        self.interval_entry.grid(row=0, column=3)

        self.save_btn = tk.Button(btn_frame, text="Save CSV", width=10, command=self.save_csv)
        self.save_btn.grid(row=0, column=4, padx=(8, 0))

        # Status
        tk.Label(frame, textvariable=self.status_var, font=("Segoe UI", 9), fg="#666").grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # History
        hist_label = tk.Label(frame, text="History:", font=("Segoe UI", 10))
        hist_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))

        self.history = tk.Text(frame, width=48, height=10, state=tk.DISABLED, wrap=tk.NONE)
        self.history.grid(row=5, column=0, columnspan=2, pady=(4, 0))

    def _set_status(self, text: str):
        self.status_var.set(text)

    def _append_history(self, text: str):
        self.history.configure(state=tk.NORMAL)
        self.history.insert(tk.END, text + "\n")
        self.history.see(tk.END)
        self.history.configure(state=tk.DISABLED)

    def refresh(self):
        # Run fetch in a thread to avoid blocking UI
        self._set_status("Fetching...")
        self.refresh_btn.config(state=tk.DISABLED)
        threading.Thread(target=self._fetch_and_update, daemon=True).start()

    def _fetch_and_update(self):
        rate = fetch_rate("AED", "INR")
        ts = datetime.datetime.now(datetime.timezone.utc)

        def on_main_thread():
            if rate is None:
                self._set_status("Failed to fetch rate")
            else:
                self.rate_var.set(f"{rate:.6f} INR")
                self.time_var.set(ts.isoformat())
                self._append_history(f"{ts.isoformat()} — 1 AED = {rate:.6f} INR")
                self._set_status("Updated")
            self.refresh_btn.config(state=tk.NORMAL)

        self.after(0, on_main_thread)

    def toggle_auto(self):
        if self.auto_refresh_job is None:
            # start
            try:
                interval = int(self.interval_var.get())
                if interval <= 0:
                    raise ValueError()
            except Exception:
                messagebox.showerror("Invalid interval", "Please enter a positive integer for the interval.")
                return
            self.auto_btn.config(text="Stop Auto")
            self._schedule_auto()
            self._set_status("Auto-refresh started")
        else:
            # stop
            self.after_cancel(self.auto_refresh_job)
            self.auto_refresh_job = None
            self.auto_btn.config(text="Start Auto")
            self._set_status("Auto-refresh stopped")

    def _schedule_auto(self):
        interval = int(self.interval_var.get())
        # fetch now, then schedule next
        self.refresh()
        self.auto_refresh_job = self.after(interval * 1000, self._schedule_auto)

    def save_csv(self):
        # Ask for filepath and append last value
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*")])
        if not path:
            return

        # Get last displayed rate
        rate_text = self.rate_var.get()
        if rate_text == "—":
            messagebox.showwarning("No rate", "No rate available to save. Pull a rate first.")
            return

        try:
            # Extract numeric part
            parts = rate_text.split()
            rate = float(parts[0])
            ts_text = self.time_var.get() or datetime.datetime.now(datetime.timezone.utc).isoformat()
            # Append to CSV
            with open(path, "a", encoding="utf-8", newline="") as f:
                # write header if file is empty
                import os

                write_header = not os.path.exists(path) or os.path.getsize(path) == 0
                if write_header:
                    f.write("timestamp,from,to,rate\n")
                f.write(f"{ts_text},AED,INR,{rate:.6f}\n")
            messagebox.showinfo("Saved", f"Saved current rate to {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV: {e}")


def main():
    app = AEDGui()
    app.mainloop()


if __name__ == "__main__":
    main()
