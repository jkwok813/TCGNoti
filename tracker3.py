import os
import requests
from dotenv import load_dotenv
load_dotenv() 

# CURRENTLY DEAD - PokeWallet's API currently does not have Price Support

API_KEY = os.getenv("POKEWALLET_API_KEY")
BASE_URL = "https://api.pokewallet.io/cards"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

with open("cardlist.txt", "r") as f:
        my_cards = [line.strip() for line in f if line.strip()]

def track_with_pokewallet():

    print(f"{'CARD NAME':<20} | {'MARKET (USA)':<14} | {'MARKET (EU)'}")
    print("-" * 60)

    for cid in my_cards:
        url = f"{BASE_URL}/{cid}"
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} for {cid}")
                continue

            data = response.json()
            
            name = data.get('name', 'Unknown')
            
            # PokeWallet provides dual-market data
            prices = data.get('prices', {})
            usa_price = prices.get('tcgplayer', {}).get('market', 'N/A')
            eu_price = prices.get('cardmarket', {}).get('market', 'N/A')

            # Formatting
            usa_str = f"${usa_price}" if usa_price != 'N/A' else 'N/A'
            eu_str = f"€{eu_price}" if eu_price != 'N/A' else 'N/A'

            print(f"{name:<20} | {usa_str:<14} | {eu_str}")

        except Exception as e:
            print(f"Request failed for {cid}: {e}")

if __name__ == "__main__":
    track_with_pokewallet()
    