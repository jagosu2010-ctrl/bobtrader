try:
    from alpaca_trade_api.rest import REST
    print("[SUCCESS] Alpaca SDK imported successfully.")
    # Attempting a blank init to check dependencies (will fail on auth, which is fine)
    api = REST('fake_key', 'fake_secret', 'https://paper-api.alpaca.markets')
    print("[SUCCESS] Alpaca REST client initialized.")
except ImportError:
    print("[FAIL] Alpaca SDK not found. Re-run: pip install alpaca-trade-api")
except Exception as e:
    print(f"[NOTE] SDK is installed, but check dependencies: {e}")