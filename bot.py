from web3 import Web3
import os

def main():
    INFURA_URL = os.getenv("INFURA_URL")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    if not INFURA_URL or not PRIVATE_KEY:
        print("Setează variabilele de mediu INFURA_URL și PRIVATE_KEY!")
        return

    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    if not w3.is_connected():
        print("Nu s-a putut conecta la node-ul Ethereum!")
        return

    print("Conectat la Sepolia testnet prin Infura!")

    account = w3.eth.account.from_key(PRIVATE_KEY)
    print(f"Folosind contul: {account.address}")

    # Adrese corecte pentru Sepolia:

    # SushiSwap Router V2 (funcționează pe Sepolia)
    router_address = w3.to_checksum_address('0x1b02da8cb0d097eb8d57a175b88c7d8b47997506')

    # Tokeni pe Sepolia (verificați)
    WETH_address = w3.to_checksum_address('0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6')
    DAI_address = w3.to_checksum_address('0xaD6D458402F60fD3Bd25163575031ACDce07538D')

    print(f"Uniswap Router Address: {router_address}")
    print(f"WETH Token Address: {WETH_address}")
    print(f"DAI Token Address: {DAI_address}")

    # Verificăm dacă contractul router există
    code = w3.eth.get_code(router_address)
    if code == b'':
        print("Nu există contract la adresa routerului pe Sepolia!")
        return
    else:
        print("Contract găsit la adresa routerului.")

    router_abi = [
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

    contract = w3.eth.contract(address=router_address, abi=router_abi)

    eth_amount = w3.to_wei(0.01, 'ether')
    path = [WETH_address, DAI_address]

    try:
        amounts_out = contract.functions.getAmountsOut(eth_amount, path).call()
        print(f"Pentru {w3.from_wei(eth_amount, 'ether')} WETH primești aproximativ {w3.from_wei(amounts_out[-1], 'ether')} DAI.")
    except Exception as e:
        print("Eroare la apelul getAmountsOut:", e)

if __name__ == "__main__":
    main()
