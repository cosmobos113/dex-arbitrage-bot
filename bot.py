from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def main():
    if w3.is_connected():
        print("Conectat la Sepolia testnet prin Infura!")

        # SushiSwap Router (Uniswap V2 fork) pe Sepolia
        uniswap_router_address = Web3.toChecksumAddress('0x1b02da8cb0d097eb8d57a175b88c7d8b47997506')

        uniswap_router_abi = [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                    {"internalType": "address[]", "name": "path", "type": "address[]"}
                ],
                "name": "getAmountsOut",
                "outputs": [
                    {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]

        router = w3.eth.contract(address=uniswap_router_address, abi=uniswap_router_abi)

        # Tokeni pe Sepolia (exemplu):
        WETH = Web3.toChecksumAddress('0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6')  # Wrapped ETH Sepolia
        DAI = Web3.toChecksumAddress('0xad6d458402f60fd3bd25163575031acdce07538d')   # DAI testnet

        amount_in = w3.toWei(1, 'ether')  # 1 ETH

        try:
            amounts_out = router.functions.getAmountsOut(amount_in, [WETH, DAI]).call()
            print(f"1 ETH poate fi schimbat pentru aproximativ {w3.fromWei(amounts_out[1], 'ether')} DAI")
        except Exception as e:
            print(f"Eroare la citirea prețului: {e}")

    else:
        print("Nu s-a putut conecta la Sepolia")

if __name__ == "__main__":
    main()
