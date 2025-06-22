import os
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("https://sepolia.infura.io/v3/5e9a2d027d0d4a88a528ec4b54bcbe4f")
PRIVATE_KEY = os.getenv("d3b3cfb486c0114a68d5a67b3b9bdb04a99962dfde44e2bcd0fb77f26df01ea4")

print(f"INFURA_URL is set: {INFURA_URL is not None}")
print(f"PRIVATE_KEY is set: {PRIVATE_KEY is not None}")
