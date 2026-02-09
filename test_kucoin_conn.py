import os
import yaml
from kucoin_universal_sdk.model.client_option import ClientOptionBuilder
from kucoin_universal_sdk.control.default_client import DefaultClient
from kucoin_universal_sdk.generate.account.account.model_get_account_list_req import GetAccountListReq

def test_connection():
    print("--- KuCoin Connectivity Test ---")
    
    # 1. Load Keys from config.yaml
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
            # Adjust these keys based on your specific YAML structure
            api_key = config['exchange']['api_key']
            api_secret = config['exchange']['api_secret']
            api_passphrase = config['exchange']['api_passphrase']
            is_sandbox = config['exchange'].get('is_sandbox', False)
    except Exception as e:
        print(f"[FAIL] Could not read config.yaml: {e}")
        return

    # 2. Initialize Client
    try:
        options = ClientOptionBuilder() \
            .with_key(api_key) \
            .with_secret(api_secret) \
            .with_passphrase(api_passphrase) \
            .with_is_sandbox(is_sandbox) \
            .build()
        
        client = DefaultClient(options)
        account_api = client.rest_service().get_account_service().get_account_api()
        
        print("[OK] Client initialized.")
        
        # 3. Attempt to fetch account list (Simple Read Request)
        print("[...] Attempting to fetch account info...")
        req = GetAccountListReq()
        resp = account_api.get_account_list(req)
        
        if resp and resp.data:
            print(f"[SUCCESS] Connected! Found {len(resp.data)} account sub-wallets.")
            for acc in resp.data[:2]: # Show first two for privacy
                print(f" - Wallet: {acc.type}, Asset: {acc.currency}, Balance: {acc.balance}")
        else:
            print("[FAIL] Connected to API, but returned no account data.")
            
    except Exception as e:
        print(f"[CRITICAL FAIL] API Error: {e}")
        print("\nPossible causes:")
        print("- Invalid API Key/Secret/Passphrase")
        print("- IP Address not whitelisted in KuCoin API settings")
        print("- Incorrect Sandbox/Live toggle")

if __name__ == "__main__":
    test_connection()