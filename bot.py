import os
from web3 import Web3

def main():
    infura_url = os.getenv('INFURA_URL')
    private_key = os.getenv('PRIVATE_KEY')

    if not infura_url or not private_key:
        print("Variabilele de mediu nu sunt setate corect!")
        return

    # Conectare la Infura Sepolia
    w3 = Web3(Web3.HTTPProvider(infura_url))

    if w3.isConnected():
        print("Conectat la Sepolia testnet prin Infura!")
    else:
        print("Nu s-a putut conecta la Infura.")
        return

    # Creare cont din cheia privată
    account = w3.eth.account.from_key(private_key)
    print(f"Adresa portofelului tău este: {account.address}")

    # Exemplu: afișează balanța ETH a contului
    balance = w3.eth.get_balance(account.address)
    print(f"Balanța în Wei este: {balance}")
    print(f"Balanța în ETH este: {w3.fromWei(balance, 'ether')}")

if __name__ == "__main__":
    main()
