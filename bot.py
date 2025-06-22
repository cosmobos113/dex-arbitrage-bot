from web3 import Web3
from flask import Flask
import os

# === CONFIGURARE ===
INFURA_URL = "https://sepolia.infura.io/v3/5e9a2d027d0d4a88a528ec4b54bcbe4f"
PRIVATE_KEY = "d3b3cfb486c0114a68d5a67b3b9bdb04a99962dfde44e2bcd0fb77f26df01ea4"
ADDRESS = "0xB172DA9795C16964D4c6Ccef7d51fFecc328193c"

# === CONECTARE LA SEPOLIA ===
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not w3.is_connected():
    raise ConnectionError("❌ Conexiune eșuată la RPC Sepolia.")

print(f"✅ Conectat la Sepolia")
print(f"🔐 Wallet: {ADDRESS}")

# === BALANȚĂ ===
balance_wei = w3.eth.get_balance(ADDRESS)
balance_eth = w3.from_wei(balance_wei, 'ether')
print(f"💰 Balanță: {balance_eth:.6f} ETH")

# === SERVER FLASK PENTRU RENDER ===
app = Flask(__name__)

@app.route('/')
def status():
    return f"""
    <h1>🟢 Bot activ</h1>
    <p><strong>Adresa:</strong> {ADDRESS}</p>
    <p><strong>Balanță:</strong> {balance_eth:.6f} ETH</p>
    <p>✅ Conectat la Sepolia</p>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render așteaptă o variabilă PORT
    app.run(host='0.0.0.0', port=port)
