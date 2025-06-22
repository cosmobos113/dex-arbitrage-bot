import os
import time
from web3 import Web3
from dotenv import load_dotenv

# Încarcă .env
load_dotenv()
INFURA_URL = os.getenv('INFURA_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
ACCOUNT = os.getenv('ACCOUNT_ADDRESS')

if not (INFURA_URL and PRIVATE_KEY and ACCOUNT):
    raise RuntimeError("Verifică variabilele de mediu în .env")

# Conectare la Sepolia
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not w3.is_connected():
    raise ConnectionError("Nu s-a putut conecta la Infura Sepolia")
print(f"Conectat la Sepolia. Account: {ACCOUNT}")

# Adrese contracte Uniswap V3 pe Sepolia
ROUTER = w3.to_checksum_address('0xE592427A0AEce92De3Edee1F18E0157C05861564')  # SwapRouter V3
QUOTER = w3.to_checksum_address('0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6')  # Quoter V2
WETH = w3.to_checksum_address('0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6')
DAI  = w3.to_checksum_address('0xaD6D458402F60fD3Bd25163575031ACDce07538D')

# ABI minimal pentru Quoter și Swap
QUOTER_ABI = [{
    "inputs":[{"internalType":"address","name":"tokenIn","type":"address"},
              {"internalType":"address","name":"tokenOut","type":"address"},
              {"internalType":"uint24","name":"fee","type":"uint24"},
              {"internalType":"uint256","name":"amountIn","type":"uint256"},
              {"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],
    "name":"quoteExactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],
    "stateMutability":"view","type":"function"
}]

SWAP_ABI = [{
    "inputs":[
        {"internalType":"address","name":"tokenIn","type":"address"},
        {"internalType":"address","name":"tokenOut","type":"address"},
        {"internalType":"uint24","name":"fee","type":"uint24"},
        {"internalType":"address","name":"recipient","type":"address"},
        {"internalType":"uint256","name":"deadline","type":"uint256"},
        {"internalType":"uint256","name":"amountIn","type":"uint256"},
        {"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},
        {"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}
    ],
    "name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],
    "stateMutability":"payable","type":"function"
}]

# Contracte
quoter = w3.eth.contract(address=QUOTER, abi=QUOTER_ABI)
router = w3.eth.contract(address=ROUTER, abi=SWAP_ABI)

# Parametri de tranzacționare
FEE = 3000  # 0.3%
AMOUNT_IN = w3.to_wei(0.01, 'ether')  # 0.01 WETH

# 1) Quote
amount_out = quoter.functions.quoteExactInputSingle(WETH, DAI, FEE, AMOUNT_IN, 0).call()
print(f"Quote: {w3.from_wei(amount_out, 'ether')} DAI pentru {w3.from_wei(AMOUNT_IN, 'ether')} WETH")

# 2) Swap (semnează și trimite)
deadline = int(time.time()) + 600
non = w3.eth.get_transaction_count(ACCOUNT)

tx = router.functions.exactInputSingle(
    WETH, DAI, FEE, ACCOUNT, deadline, AMOUNT_IN, int(amount_out * 0.99), 0
).build_transaction({
    'from': ACCOUNT,
    'value': AMOUNT_IN,
    'gas': 300000,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': non,
    'chainId': 11155111
})
signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
print(f"Swap trimis: {tx_hash.hex()}")

# Așteaptă confirmare
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Confirmat block {receipt.blockNumber}")
