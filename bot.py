import os
from web3 import Web3
from dotenv import load_dotenv
from uniswap import UniswapV3

# Încarcă variabilele de mediu
load_dotenv()

# Verifică dacă variabilele de mediu sunt setate corect
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

if not INFURA_URL or not PRIVATE_KEY:
    print("Eroare: INFURA_URL sau PRIVATE_KEY nu sunt setate corect.")
    exit()

# Conectează-te la Sepolia Testnet prin Infura
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = w3.eth.account.privateKeyToAccount(PRIVATE_KEY)
print(f"Conectat la Sepolia testnet prin Infura!\nFolosind contul: {account.address}")

# Adresele contractelor Uniswap V3 pe Sepolia
UNISWAP_V3_FACTORY_ADDRESS = "0x0227628f3F023bb0B980b67D528571c95c6DaC1c"
SWAP_ROUTER_ADDRESS = "0x3bFA4769FB09eefC5a80d6E87c3B9C650f7Ae48E"
QUOTER_ADDRESS = "0xEd1f6473345F45b75F8179591dd5bA1888cf2FB3"
WETH_ADDRESS = "0xfFf9976782d46CC05630D1f6eBAb18b2324d6B14"
DAI_ADDRESS = "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

# Instanțiază obiectul UniswapV3
uni = UniswapV3(
    w3=w3,
    private_key=PRIVATE_KEY,
    router_address=SWAP_ROUTER_ADDRESS,
    factory_address=UNISWAP_V3_FACTORY_ADDRESS,
    quoter_address=QUOTER_ADDRESS,
    weth_address=WETH_ADDRESS,
    dai_address=DAI_ADDRESS
)

# Exemplu de swap: 0.1 WETH -> DAI
amount_in = 0.1  # în WETH
amount_out_min = 100  # în DAI (valoare estimată minimă)
recipient = account.address
deadline = w3.eth.get_block('latest')['timestamp'] + 1200  # 20 minute de la blocul curent

# Realizează swap-ul
try:
    tx = uni.swap_exact_tokens_for_tokens(
        amount_in,
        amount_out_min,
        recipient,
        deadline
    )
    print(f"Swap realizat cu succes! Hash tranzacție: {tx.transactionHash.hex()}")
except Exception as e:
    print(f"Eroare la realizarea swap-ului: {e}")
