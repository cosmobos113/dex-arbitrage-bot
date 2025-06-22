from web3 import Web3
import json

# Adresa și ABI Router Uniswap V3 (ExactInputSingle)
UNISWAP_ROUTER_ADDRESS = Web3.to_checksum_address("0xE592427A0AEce92De3Edee1F18E0157C05861564")
UNISWAP_ROUTER_ABI = json.loads("""
[
  {
    "inputs": [
      {
        "components": [
          {"internalType": "address", "name": "tokenIn", "type": "address"},
          {"internalType": "address", "name": "tokenOut", "type": "address"},
          {"internalType": "uint24", "name": "fee", "type": "uint24"},
          {"internalType": "address", "name": "recipient", "type": "address"},
          {"internalType": "uint256", "name": "deadline", "type": "uint256"},
          {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
          {"internalType": "uint256", "name": "amountOutMinimum", "type": "uint256"},
          {"internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160"}
        ],
        "internalType": "struct ISwapRouter.ExactInputSingleParams",
        "name": "params",
        "type": "tuple"
      }
    ],
    "name": "exactInputSingle",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "amountOut",
        "type": "uint256"
      }
    ],
    "stateMutability": "payable",
    "type": "function"
  }
]
""")

w3 = None
router = None

def set_web3_and_router(web3_instance):
    global w3, router
    w3 = web3_instance
    router = w3.eth.contract(address=UNISWAP_ROUTER_ADDRESS, abi=UNISWAP_ROUTER_ABI)

def perform_swap(private_key, address, amount_eth):
    if w3 is None or router is None:
        raise Exception("Web3 or Router not initialized. Call set_web3_and_router first.")

    amount_in_wei = w3.to_wei(amount_eth, 'ether')
    deadline = w3.eth.get_block('latest')['timestamp'] + 600  # +10 minute termen limită

    params = {
        "tokenIn": Web3.to_checksum_address("0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6"),   # WETH Sepolia
        "tokenOut": Web3.to_checksum_address("0xd35CcEAD182dCEE0F148EbaC9447DA2c4D449c4c"),  # USDC Sepolia
        "fee": 3000,  # 0.3%
        "recipient": Web3.to_checksum_address(address),
        "deadline": deadline,
        "amountIn": amount_in_wei,
        "amountOutMinimum": 0,  # Accept orice (atenție: risc de slippage mare)
        "sqrtPriceLimitX96": 0
    }

    nonce = w3.eth.get_transaction_count(address)
    tx = router.functions.exactInputSingle(params).build_transaction({
        "from": address,
        "value": amount_in_wei,
        "gas": 300000,
        "gasPrice": w3.to_wei('10', 'gwei'),
        "nonce": nonce
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash.hex(), receipt.blockNumber

def simulate_swap(amount_eth):
    if w3 is None or router is None:
        raise Exception("Web3 or Router not initialized. Call set_web3_and_router first.")

    amount_in_wei = w3.to_wei(amount_eth, 'ether')
    deadline = w3.eth.get_block('latest')['timestamp'] + 600  # +10 minute termen limită

    params = {
        "tokenIn": Web3.to_checksum_address("0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6"),   # WETH Sepolia
        "tokenOut": Web3.to_checksum_address("0xd35CcEAD182dCEE0F148EbaC9447DA2c4D449c4c"),  # USDC Sepolia
        "fee": 3000,  # 0.3%
        "recipient": Web3.to_checksum_address("0x0000000000000000000000000000000000000000"),  # Dummy recipient
        "deadline": deadline,
        "amountIn": amount_in_wei,
        "amountOutMinimum": 0,
        "sqrtPriceLimitX96": 0
    }

    # Call metoda exactInputSingle ca simulare (quote)
    amount_out = router.functions.exactInputSingle(params).call({
        "from": "0x0000000000000000000000000000000000000000",
        "value": amount_in_wei,
    })

    return amount_out
