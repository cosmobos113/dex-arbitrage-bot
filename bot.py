from web3 import Web3
import os

def main():
    INFURA_URL = os.getenv('INFURA_URL')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')

    if not INFURA_URL or not PRIVATE_KEY:
        print("INFURA_URL or PRIVATE_KEY environment variables are not set.")
        return

    print(f"INFURA_URL is set: {bool(INFURA_URL)}")
    print(f"PRIVATE_KEY is set: {bool(PRIVATE_KEY)}")

    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

    if w3.is_connected():
        print("Conectat la Sepolia testnet prin Infura!")
    else:
        print("Nu s-a putut conecta la Sepolia testnet prin Infura.")
        return

    # Adrese Uniswap V2 Router pe Sepolia testnet (exemplu, poate trebuie actualizată)
    uniswap_router_address = Web3.to_checksum_address('0x1b02da8cb0d097eb8d57a175b88c7d8b47997506')

    # Exemple de adrese token (WETH și DAI) pe Sepolia
    WETH = Web3.to_checksum_address('0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6')
    DAI = Web3.to_checksum_address('0xad6d458402f60fd3bd25163575031acdce07538d')

    print(f"Uniswap Router Address: {uniswap_router_address}")
    print(f"WETH Token Address: {WETH}")
    print(f"DAI Token Address: {DAI}")

    # Aici poți continua să implementezi funcționalitatea botului, ex:
    # - conectarea la contractul router
    # - construirea și trimiterea tranzacțiilor
    # - monitorizarea oportunităților de arbitraj etc.

if __name__ == "__main__":
    main()
