import os
import time
from web3 import Web3
from dotenv import load_dotenv

# Încarcă variabilele din .env
load_dotenv()
RPC_URL       = os.getenv('RPC_URL')        # ex: https://rpc.ankr.com/eth_goerli
PRIVATE_KEY   = os.getenv('PRIVATE_KEY')    # fără “0x”
ACCOUNT       = os.getenv('ACCOUNT_ADDRESS')

if not (RPC_URL and PRIVATE_KEY and ACCOUNT):
    raise RuntimeError("Verifică .env: RPC_URL, PRIVATE_KEY, ACCOUNT_ADDRESS trebuie setate.")

# Conectare la Goerli
w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    raise ConnectionError("Conexiune eșuată la RPC Goerli.")
print(f"Conectat la Goerli. Account: {ACCOUNT}")

# SushiSwap V2 Router și tokeni pe Goerli
ROUTER = w3.to_checksum_address('0x1b02da8cb0d097eb8d57a175b88c7d8b47997506')
WETH   = w3.to_checksum_address('0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6')
DAI    = w3.to_checksum_address('0x11fE4B6AE13d2a6055C8D9cF65c55bac32B5d844')

# ABI minimal pentru getAmountsOut și swapExactETHForTokens
ABI = [
    {
        "inputs": [
            {"internalType": "uint256","name": "amountIn","type": "uint256"},
            {"internalType": "address[]","name": "path","type": "address[]"}
        ],
        "name": "getAmountsOut",
        "outputs": [
            {"internalType": "uint256[]","name": "amounts","type": "uint256[]"}
        ],
        "stateMutability":"view",
        "type":"function"
    },
    {
        "inputs": [
            {"internalType":"uint256","name":"amountOutMin","type":"uint256"},
            {"internalType":"address[]","name":"path","type":"address[]"},
            {"internalType":"address","name":"to","type":"address"},
            {"internalType":"uint256","name":"deadline","type":"uint256"}
        ],
        "name":"swapExactETHForTokens",
        "outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],
        "stateMutability":"payable",
        "type":"function"
    }
]

router = w3.eth.contract(address=ROUTER, abi=ABI)

# Parametri
AMOUNT_IN = w3.to_wei(0.01, 'ether')  # 0.01 WETH
SLIPPAGE  = 0.99                      # 1% slippage
DEADLINE  = int(time.time()) + 600    # 10 minute
CHAIN_ID  = 5                         # Goerli

def main():
    # Quote
    try:
        amounts = router.functions.getAmountsOut(AMOUNT_IN, [WETH, DAI]).call()
        dai_est = amounts[-1]
        print(f"Quote: {w3.from_wei(dai_est, 'ether')} DAI pentru {w3.from_wei(AMOUNT_IN, 'ether')} WETH")
    except Exception as e:
        print("Eroare la quote:", e)
        return

    # Swap
    min_out = int(dai_est * SLIPPAGE)
    nonce   = w3.eth.get_transaction_count(ACCOUNT)
    tx = router.functions.swapExactETHForTokens(
        min_out,
        [WETH, DAI],
        ACCOUNT,
        DEADLINE
    ).build_transaction({
        'from': ACCOUNT,
        'value': AMOUNT_IN,
        'gas': 200000,
        'gasPrice': w3.to_wei('20', 'gwei'),
        'nonce': nonce,
        'chainId': CHAIN_ID
    })

    signed  = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"Swap trimis: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Confirmat block {receipt.blockNumber}")

if __name__ == "__main__":
    main()
