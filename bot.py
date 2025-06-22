from web3 import Web3
import os
import time

def main():
    INFURA_URL = os.getenv("INFURA_URL")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    if not INFURA_URL or not PRIVATE_KEY:
        print("Lipsesc variabilele de mediu INFURA_URL sau PRIVATE_KEY")
        return

    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    if not w3.is_connected():
        print("Nu s-a putut conecta la Infura")
        return
    print("Conectat la Sepolia testnet prin Infura!")

    # Adrese
    uniswap_router_address = w3.to_checksum_address("0x1b02da8cb0d097eb8d57a175b88c7d8b47997506")  # SushiSwap Router V2 pe Sepolia
    WETH_address = w3.to_checksum_address("0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6")
    DAI_address = w3.to_checksum_address("0xaD6D458402F60fD3Bd25163575031ACDce07538D")

    # ABI minim pentru swapExactETHForTokens și getAmountsOut
    router_abi = [
        {
            "inputs": [
                {"internalType": "uint256","name": "amountOutMin","type": "uint256"},
                {"internalType": "address[]","name": "path","type": "address[]"},
                {"internalType": "address","name": "to","type": "address"},
                {"internalType": "uint256","name": "deadline","type": "uint256"}
            ],
            "name": "swapExactETHForTokens",
            "outputs": [
                {"internalType": "uint256[]","name": "amounts","type": "uint256[]"}
            ],
            "stateMutability": "payable",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "uint256","name": "amountIn","type": "uint256"},
                {"internalType": "address[]","name": "path","type": "address[]"}
            ],
            "name": "getAmountsOut",
            "outputs": [
                {"internalType": "uint256[]","name": "amounts","type": "uint256[]"}
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

    contract = w3.eth.contract(address=uniswap_router_address, abi=router_abi)

    account = w3.eth.account.from_key(PRIVATE_KEY)
    print(f"Folosind contul: {account.address}")

    # Cât ETH vrem să schimbăm
    eth_amount = w3.to_wei(0.01, 'ether')

    # Path pentru swap WETH -> DAI
    path = [WETH_address, DAI_address]

    # Calculăm amountOutMin cu 1% slippage (în minus)
    amounts_out = contract.functions.getAmountsOut(eth_amount, path).call()
    estimated_dai = amounts_out[-1]
    slippage = 0.99  # Acceptăm minim 99% din estimare
    amount_out_min = int(estimated_dai * slippage)

    print(f"Estimare DAI primiti: {w3.from_wei(estimated_dai, 'ether')}")
    print(f"amountOutMin cu 1% slippage: {w3.from_wei(amount_out_min, 'ether')}")

    to = account.address
    deadline = int(time.time()) + 300  # 5 minute de la momentul apelului

    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions.swapExactETHForTokens(
        amount_out_min,
        path,
        to,
        deadline
    ).build_transaction({
        'from': account.address,
        'value': eth_amount,
        'gas': 250000,
        'gasPrice': w3.to_wei('30', 'gwei'),
        'nonce': nonce,
        'chainId': 11155111
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Tranzacția a fost trimisă! Hash: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Tranzacția confirmată în block {receipt.blockNumber}")

if __name__ == "__main__":
    main()
