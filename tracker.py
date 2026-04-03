import asyncio
from tcgdexsdk import TCGdex
import requests

async def track_my_collection():
    # 1. Initialize the API
    tcgdex = TCGdex("en")

    # 2. Your list of Card IDs
    # Find these IDs by searching on tcgdex.dev
    with open("cardlist.txt", "r") as f:
        my_cards = [line.strip() for line in f if line.strip()]

    print(f"{'CARD NAME':<25} | {'SET':<20} | {'MARKET PRICE'}")
    print("-" * 65)

    for card_id in my_cards:
        try:
            url = f"https://api.tcgdex.net/v2/en/cards/{card_id}"
            response = requests.get(url)
            data = response.json()
            #print(data) # Print entire JSON
            
            name = data.get('name', 'Unknown')
            set_info = data.get('set', {})
            set_name = set_info.get('name', 'Unknown')
            
            # --- THE SAFETY CHECK ---
            market_price = "N/A"
            
            # 1. Safely check for pricing -> tcgplayer
            pricing = data.get('pricing', {})
            if pricing: # Check if pricing exists
                tcg_pricing = pricing.get('tcgplayer') # Use .get()
                
                # 2. Check if tcg_pricing actually has data (is not None)
                if tcg_pricing and isinstance(tcg_pricing, dict):
                    # 3. Look through the variants (normal, holofoil, etc.)
                    for variant_name, details in tcg_pricing.items():
                        if isinstance(details, dict):
                            # TCGdex often uses 'market' or 'marketPrice'
                            price = details.get('marketPrice') or details.get('market')
                            if price:
                                market_price = f"${price}"
                                break

            print(f"{name:<20} | {set_name:<18} | {market_price}")
            
        except Exception as e:
            print(f"Error with {card_id}: {e}")

if __name__ == "__main__":
    asyncio.run(track_my_collection())