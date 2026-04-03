import os
import requests
from dotenv import load_dotenv
load_dotenv() 

API_KEY = os.getenv("SCRYDEX_API_KEY")
headers = {"X-Api-Key": API_KEY}
BASE_URL = "https://api.scrydex.com/pokemon/v1/cards"

def track_scrydex_collection():
    
    with open("cardlist.txt", "r") as f:
        my_cards = [line.strip() for line in f if line.strip()]


    print(f"{'CARD NAME':<20} | {'SET':<10} | {'MARKET PRICE'}")
    print("-" * 55)

    for cid in my_cards:
        try:
            # Construct the specific endpoint
            url = f"{BASE_URL}/{cid}"
            print(url)
            response = requests.get(url, headers)
            print(response)
            
            if response.status_code == 404:
                print(f"404: {cid} not found. Try removing leading zeros (e.g., -19 instead of -019)")
                continue
                
            data = response.json()
            
            # Scrydex v1 returns the core card data in the root
            name = data.get('name', 'Unknown')
            set_code = data.get('set', {}).get('id', 'N/A')
            
            # Accessing the price data
            # Path: pricing -> tcgplayer -> market
            pricing = data.get('pricing', {}).get('tcgplayer', {})
            market_price = "N/A"
            
            # Scrydex often lists 'market' directly under the variant
            if pricing:
                for variant in ['holofoil', 'normal', 'reverse']:
                    v_data = pricing.get(variant)
                    if v_data and 'market' in v_data:
                        market_price = f"${v_data['market']}"
                        break

            print(f"{name:<20} | {set_code:<10} | {market_price}")

        except Exception as e:
            print(f"Error fetching {cid}: {e}")

if __name__ == "__main__":
    track_scrydex_collection()