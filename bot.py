import os

print("=== Environment Variables ===")
for key, value in os.environ.items():
    print(f"{key} = {value}")

infura_url = os.getenv('INFURA_URL')
private_key = os.getenv('PRIVATE_KEY')

print(f"\nINFURA_URL is set: {bool(infura_url)}")
print(f"PRIVATE_KEY is set: {bool(private_key)}")
