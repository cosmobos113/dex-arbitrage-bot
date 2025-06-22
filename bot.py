from web3 import Web3
from flask import Flask, request
import os
import json

# === CONFIGURARE ȘI CONECTARE ===
INFURA_URL = "https://sepolia.infura.io/v3/5e9a2d027d0d4a88a528ec4b54bcbe4f"
PRIVATE_KEY = "d3b3cfb486c0114a68d5a67b3b9bdb04a99962dfde44e2bcd0fb77f26df01ea4"
ADDRESS = "0xB172DA9795C16964D4c6Ccef7d51fFecc328193c"

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not w3.is_connected():
    raise ConnectionError("❌ Conexiune eșuată la RPC Sepolia.")

print(f"✅ Conectat la Sepolia")
print(f"🔐 Wallet: {ADDRESS}")

# === CONTRACT QUOTER ===
QUOTER_V2_ADDRESS = "0x61fFE014bA17989E743c5F6cB21bF9697530B21e"
QUOTER_V2_ABI = json.loads('[{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"name":"quoteExactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"view","type":"function"}]')

quoter = w3.eth.contract(address=QUOTER_V2_ADDRESS, abi=QUOTER_V2_ABI)

WETH = "0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6"
USDC = "0xD35CceEAD182dcee0F148EbaC9447DA2c4D449c4"
FEE = 3000  # 0.3%

app = Flask(__name__)

@app.route('/')
def status():
    balance_wei = w3.eth.get_balance(ADDRESS)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    return f"""
    <h1>🟢 Bot activ</h1>
    <p><strong>Adresa:</strong> {ADDRESS}</p>
    <p><strong>Balanță:</strong> {balance_eth:.6f} ETH</p>
    <p>✅ Conectat la Sepolia</p>
    """

@app.route('/quote')
def get_quote():
    # Preia suma din query string ?amount=0.01, altfel 0.01 ETH default
    amount_eth_str = request.args.get('amount', '0.01')
    try:
        amount_eth = float(amount_eth_str)
        amount_in_wei = w3.to_wei(amount_eth, 'ether')
    except ValueError:
        return "⚠️ Parametru 'amount' invalid. Trebuie un număr."

    try:
        quote = quoter.functions.quoteExactInputSingle(
            WETH,
            USDC,
            FEE,
            amount_in_wei,
            0
        ).call()
        quote_usdc = quote / 10**6  # USDC are 6 zecimale
        return f"🔄 Quote: {amount_eth} ETH → ≈ {quote_usdc:.2f} USDC"
    except Exception as e:
        return f"⚠️ Eroare la quote: {e}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
