from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    INFURA_URL = os.getenv("INFURA_URL")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")

    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

    print(f"INFURA_URL is set: {bool(INFURA_URL)}")
    print(f"PRIVATE_KEY is set: {bool(PRIVATE_KEY)}")

    if w3.is_connected():
        print("Conectat la Sepolia testnet prin Infura!")
    else:
        print("Nu s-a putut conecta la Infura.")
        return

if __name__ == "__main__":
    main()
