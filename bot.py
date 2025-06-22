from web3 import Web3
from flask import Flask, request
import os
import json
from swap import set_web3_and_router, perform_swap, simulate_swap
from flask import jsonify

# === CONFIGURARE ȘI CONECTARE ===
INFURA_URL = "https://sepolia.infura.io/v3/5e9a2d027d0d4a88a528ec4b54bcbe4f"
PRIVATE_KEY = "d3b3cfb486c0114a68d5a67b3b9bdb04a99962dfde44e2bcd0fb77f26df01ea4"
ADDRESS = "0xB172DA9795C16964D4c6Ccef7d51fFecc328193c"

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not w3.is_connected():
    raise ConnectionError("❌ Conexiune eșuată la RPC Sepolia.")

print(f"✅ Conectat la Sepolia")
print(f"🔐 Wallet: {ADDRESS}")

set_web3_and_router(w3)

# === CONTRACT QUOTER (comentat, folosit anterior) ===
# QUOTER_V2_ADDRESS = "0x61fFE014bA17989E743c5F6cB21bF9697530B21e"
# QUOTER_V2_ABI = json.loads('[{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"name":"quoteExactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"view","type":"function"}]')
# quoter = w3.eth.contract(address=QUOTER_V2_ADDRESS, abi=QUOTER_V2_ABI)

WETH = "0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6"
USDC = "0xd35CcEAD182dCEE0F148EbaC9447DA2c4D449c4"
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
    amount_eth_str = request.args.get('amount', '0.01')
    try:
        amount_eth = float(amount_eth_str)
    except ValueError:
        return "⚠️ Parametru 'amount' invalid. Trebuie un număr."

    try:
        amount_out = simulate_swap(amount_eth)
        # USDC are 6 zecimale, deci convertim la format uman
        amount_out_usdc = amount_out / 10**6
        return f"🔄 Quote simulare: {amount_eth} ETH → ≈ {amount_out_usdc:.2f} USDC"
    except Exception as e:
        return f"⚠️ Eroare la simulare quote: {e}"

# Varianta veche cu quoter, comentată
# @app.route('/quote')
# def get_quote_old():
#     amount_eth_str = request.args.get('amount', '0.01')
#     try:
#         amount_eth = float(amount_eth_str)
#         amount_in_wei = w3.to_wei(amount_eth, 'ether')
#     except ValueError:
#         return "⚠️ Parametru 'amount' invalid. Trebuie un număr."
#
#     try:
#         quote = quoter.functions.quoteExactInputSingle(
#             WETH,
#             USDC,
#             FEE,
#             amount_in_wei,
#             0
#         ).call()
#         quote_usdc = quote / 10**6
#         return f"🔄 Quote: {amount_eth} ETH → ≈ {quote_usdc:.2f} USDC"
#     except Exception as e:
#         return f"⚠️ Eroare la quote: {e}"

@app.route('/swap', methods=['POST'])
def swap_route():
    data = request.get_json(force=True)
    amount_eth = float(data.get('amount', 0.01))
    try:
        tx_hash, block_number = perform_swap(PRIVATE_KEY, ADDRESS, amount_eth)
        return jsonify({
            "tx_hash": tx_hash,
            "block_number": block_number,
            "message": f"Swap {amount_eth} ETH executat."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
