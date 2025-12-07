"""aed_to_inr.py

Fetch live AED -> INR exchange rate.

This script uses the free exchangerate.host API (no API key required):
https://api.exchangerate.host/convert?from=AED&to=INR

Usage:
    python aed_to_inr.py           # fetch once and print
    python aed_to_inr.py --once    # same as above
    python aed_to_inr.py --interval 60  # print rate every 60 seconds
    python aed_to_inr.py --csv rates.csv  # append timestamped rates to CSV (runs once unless --interval provided)

"""

from __future__ import annotations

import argparse
import csv
import datetime
import sys
import time
from typing import Optional

import requests

API_URL_EXCHANGE_RATE_HOST = "https://api.exchangerate.host/convert"
API_URL_ER_API = "https://open.er-api.com/v6/latest"


def fetch_rate(from_currency: str = "AED", to_currency: str = "INR") -> Optional[float]:
    """Fetch conversion rate using a free provider, with fallback.

    Tries `open.er-api.com` first (no API key), then falls back to exchangerate.host.
    Returns the conversion rate (float) or None on failure.
    """
    # 1) Try open.er-api.com endpoint: /v6/latest/{base}
    try:
        url = f"{API_URL_ER_API}/{from_currency}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Expected shape: { "result": "success", "base_code": "AED", "rates": {"INR": 22.345} }
        if data.get("result") in ("success", "ok"):
            rates = data.get("rates", {})
            if to_currency in rates:
                return float(rates[to_currency])
    except Exception:
        # Silent fallback to next provider
        pass

    # 2) Fallback to exchangerate.host convert endpoint (no key)
    try:
        resp = requests.get(API_URL_EXCHANGE_RATE_HOST, params={"from": from_currency, "to": to_currency, "amount": 1}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Response may be: {"success": true, "info": {"rate": ...}, "result": ...}
        if data.get("success"):
            info = data.get("info") or {}
            rate = info.get("rate")
            if rate is None:
                rate = data.get("result")
            return float(rate)
        else:
            # Log failure for debugging
            print("ExchangeRateHost reported failure:", data, file=sys.stderr)
            return None
    except Exception as e:
        print(f"Error fetching rate: {e}", file=sys.stderr)
        return None


def append_to_csv(path: str, timestamp: datetime.datetime, rate: float) -> None:
    header = ["timestamp", "from", "to", "rate"]
    write_header = False
    try:
        # Detect if file exists by trying to open in read mode
        with open(path, "r", newline=""):
            pass
    except FileNotFoundError:
        write_header = True

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow([timestamp.isoformat(), "AED", "INR", f"{rate:.6f}"])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Fetch live AED -> INR exchange rate")
    parser.add_argument("--interval", "-i", type=int, default=0,
                        help="If >0, poll every N seconds. Otherwise run once.")
    parser.add_argument("--csv", type=str, default=None,
                        help="Optional CSV file path to append timestamped rates")
    parser.add_argument("--once", action="store_true", help="Fetch once and exit (same as default)")
    args = parser.parse_args(argv)

    interval = args.interval
    if args.once:
        interval = 0

    def do_fetch_and_print():
        ts = datetime.datetime.now(datetime.timezone.utc)
        rate = fetch_rate("AED", "INR")
        if rate is None:
            print(f"{ts.isoformat()} - Failed to fetch rate")
            return False
        out = f"{ts.isoformat()} UTC — 1 AED = {rate:.6f} INR"
        print(out)
        if args.csv:
            try:
                append_to_csv(args.csv, ts, rate)
            except Exception as e:
                print(f"Failed to write CSV: {e}", file=sys.stderr)
        return True

    if interval > 0:
        try:
            while True:
                do_fetch_and_print()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Stopped by user")
    else:
        success = do_fetch_and_print()
        return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
