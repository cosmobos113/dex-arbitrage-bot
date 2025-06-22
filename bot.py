import os

def main():
    infura_url = os.getenv('INFURA_URL')
    private_key = os.getenv('PRIVATE_KEY')

    print(f"INFURA_URL is set: {bool(infura_url)}")
    print(f"PRIVATE_KEY is set: {bool(private_key)}")

    # Restul codului tău aici
    # De exemplu:
    if not infura_url or not private_key:
        print("Variabilele de mediu nu sunt setate corect!")
        return

    # Folosește infura_url și private_key pentru conexiuni, etc.

if __name__ == "__main__":
    main()
