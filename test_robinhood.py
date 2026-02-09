try:
    import robin_stocks.robinhood as rh
    print("[SUCCESS] Robin-stocks SDK imported successfully.")
    # Checking access to a public function that doesn't require login
    price = rh.stocks.get_latest_price("AAPL")
    if price:
        print(f"[SUCCESS] Robinhood API connectivity verified. AAPL: ${price[0]}")
except ImportError:
    print("[FAIL] Robin-stocks SDK not found. Re-run: pip install robin-stocks")
except Exception as e:
    print(f"[FAIL] Connectivity error: {e}")