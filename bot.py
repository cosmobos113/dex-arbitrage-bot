from web3 import Web3
import json
import os

# === CONFIG ===
RPC_URL = "https://rpc.ankr.com/eth_sepolia"  # RPC HTTP valid
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # Pune cheia ta privată în mediul de execuție
ADDRESS = Web3.to_checksum_address("0xB172DA9795C16964D4c6Ccef7d51fFecc328193c")

# === INIT ===
w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    raise ConnectionError("Conexiune eșuată la RPC Sepolia.")
print(f"✅ Conectat la Sepolia. Account: {ADDRESS}")

# === EXEMPLE SIMPLE DE INTERACȚIUNE ===

# Afișează balansul ETH
balance = w3.eth.get_balance(ADDRESS)
print(f"💰 Balansul tău: {w3.from_wei(balance, 'ether')} ETH")

# Ex: Citire block curent
block = w3.eth.block_number
print(f"🔢 Block curent: {block}")

# === TEMPLATE: Trimitere tranzacție (NEACTIVATĂ implicit) ===
"""
def trimite_eth(destinatar, valoare_eth):
    nonce = w3.eth.get_transaction_count(ADDRESS)
    tx = {
        'nonce': nonce,
        'to': Web3.to_checksum_address(destinatar),
        'value': w3.to_wei(valoare_eth, 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'chainId': 11155111  # Sepolia Chain ID
    }
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"📤 Tranzacție trimisă: {w3.to_hex(tx_hash)}")
"""

# === TEMPLATE: Contract quote / interacțiune ===
"""
# Încarcă ABI-ul și interacționează cu un contract
with open("uniswap_abi.json") as f:
    abi = json.load(f)

contract_address = Web3.to_checksum_address("0x...")  # adresa contractului
contract = w3.eth.contract(address=contract_address, abi=abi)

try:
    quote = contract.functions.getQuote(...).call()
    print(f"💬 Quote: {quote}")
except Exception as e:
    print(f"Eroare la quote: {e}")
"""
