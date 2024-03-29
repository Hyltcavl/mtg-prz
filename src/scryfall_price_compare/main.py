import json
import datetime
import os
import re

from src.scryfall_price_compare.logic import download_scryfall_cards



    
today_date = datetime.datetime.now().strftime("%Y-%m-%d")
folder_name = "scryfall_cards"
file_name = f'small_cards_{today_date}'
scryfall_files = [file for file in os.listdir(folder_name) if file.startswith(file_name)]

if len(scryfall_files) == 0:
    download_scryfall_cards()
    scryfall_files = [file for file in os.listdir(folder_name) if file.startswith(file_name)]
else:
    print("scryfall cards already downloaded today")

with open(f'{folder_name}/{scryfall_files[0]}', 'rb') as f:
    scryfall_card_list = json.load(f)

dl_files = [file for file in os.listdir("dragonslair_cards") if file.startswith(f'cards_{today_date}')]

print({dl_files[0]})
with open(f'dragonslair_cards/{dl_files[0]}', 'rb') as f:
    dl_card_list = json.load(f)

dl_card_list_refined = {}
for block in dl_card_list:
    dl_card_list_refined.update(block.get("cards"))


sd = {}
prices_of_cards = []
for card_name, cards in dl_card_list_refined.items():
    card_name = card_name.replace("Æ", "Ae")
    scryfall_cards = scryfall_card_list.get(card_name)
    if scryfall_cards == None:
        for name, content in scryfall_card_list.items():
            name:str = name
            if name.startswith(card_name) or name.endswith(card_name):
                scryfall_cards = content
    if scryfall_cards == None:
        print(f'Unable to find {card_name}')
        continue
        
    
    #find the lowest priced card of the scryfall cards 
    lowest_eur = float("inf")
    lowest_eur_foil = float("inf")
    lowest_eur_set = None
    lowest_eur_foil_set = None

    for scryfallCard in scryfall_cards:
        eur = scryfallCard.get("prices").get("eur")

        if eur and float(eur) < lowest_eur:
            lowest_eur = float(eur)
            lowest_eur_set = scryfallCard.get("set")
        
        eur_foil = scryfallCard.get("prices").get("eur_foil")
        if eur_foil and float(eur_foil) < lowest_eur_foil:
            lowest_eur_foil = float(eur_foil)
            lowest_eur_foil_set = scryfallCard.get("set")
    
    #find the lowest priced dragonslair card 
    lowest_price = float("inf")
    lowest_foil_price = float("inf")
    lowest_price_set = None
    lowest_foil_price_set = None

    for card in cards:
        price = round(card.get("price") * 0.087, 2)
        if price and float(price) < lowest_price:
            lowest_price = float(price)
            lowest_price_set = card.get("set") 

        if card.get("foil") == "true" and price and float(price) < lowest_foil_price:
            lowest_foil_price = float(price)
            lowest_price_set = lowest_foil_price_set.get("set")
        
    price_compare_obj = {
        "name": card_name,
        "dl_price": lowest_price if lowest_price != float("inf") else None,
        "dl_set": lowest_price_set,
        "dl_price_foil": lowest_foil_price if lowest_foil_price != float("inf") else None,
        "dl_foil_set": lowest_foil_price_set,
        "mkm_price": lowest_eur if lowest_eur != float("inf") else None,
        "mkm_set": lowest_eur_set,
        "mkm_price_foil": lowest_eur_foil if lowest_eur_foil != float("inf") else None,
        "mkm_set": lowest_eur_foil_set
    }
    prices_of_cards.append(price_compare_obj)

with open(f'results/prices_{today_date}.json', 'a') as file:
    file.write(json.dumps(prices_of_cards))

cards_with_lower_dl_price = []
foil_cards_with_lower_dl_price = []

for card in prices_of_cards:
    if card['dl_price'] and card['mkm_price'] and card['dl_price'] < card['mkm_price']:
        percent_diff = ((card['mkm_price'] - card['dl_price']) / card['mkm_price']) * 100
        card_info = {
            'name': card['name'],
            'DL_price': card['dl_price'],
            'mkm_price': card['mkm_price'],
            'difference': round(percent_diff, 2)
        }
        cards_with_lower_dl_price.append(card_info)

    if card['dl_price_foil'] and card['mkm_price_foil'] and card['dl_price_foil'] < card['mkm_price_foil']:
        percent_diff = ((card['mkm_price_foil'] - card['dl_price_foil']) / card['mkm_price_foil']) * 100
        card_info = {
            'name': card['name'],
            'DL_price': card['dl_price_foil'],
            'mkm_price': card['mkm_price_foil'],
            'difference': round(percent_diff, 2)
        }
        foil_cards_with_lower_dl_price.append(card_info)

# Sort cards with lower prices by dl_price
sorted_cards = sorted(cards_with_lower_dl_price, key=lambda card: card.get('DL_price', float('inf')))

# Sort foil cards with lower prices by dl_price_foil
sorted_foil_cards = sorted(foil_cards_with_lower_dl_price, key=lambda card: card.get('DL_price', float('inf')))

# Write the sorted lists to a JSON file
with open('sorted_cards.json', 'w') as f:
    json.dump(sorted_cards, f, indent=4)

with open('sorted_foil_cards.json', 'w') as f:
    json.dump(sorted_foil_cards, f, indent=4)

# cards_with_lower_dl_price = []
# foil_cards_with_lower_dl_price = []

# for card in prices_of_cards:
#     if card['dl_price'] and card['mkm_price'] and card['dl_price'] < card['mkm_price']:
#         percent_diff = ((card['mkm_price'] - card['dl_price']) / card['mkm_price']) * 100
#         card_info = {
#             'name': card['name'],
#             'DL_price': card['dl_price'],
#             'mkm_price': card['mkm_price'],
#             'difference': round(percent_diff, 2)
#         }
#         cards_with_lower_dl_price.append(card_info)

#     if card['dl_price_foil'] and card['mkm_price_foil'] and card['dl_price_foil'] < card['mkm_price_foil']:
#         percent_diff = ((card['mkm_price_foil'] - card['dl_price_foil']) / card['mkm_price_foil']) * 100
#         card_info = {
#             'name': card['name'],
#             'DL_price': card['dl_price_foil'],
#             'mkm_price': card['mkm_price_foil'],
#             'difference': round(percent_diff, 2)
#         }
#         foil_cards_with_lower_dl_price.append(card_info)

# # Sort cards with lower prices by dl_price
# sorted_cards = sorted(cards_with_lower_dl_price, key=lambda card: card.get('DL_price', float('inf')))

# # Sort foil cards with lower prices by dl_price_foil
# sorted_foil_cards = sorted(foil_cards_with_lower_dl_price, key=lambda card: card.get('DL_price', float('inf')))

# print("\nCards sorted by dl_price:")
# for card in sorted_cards:
#     print(f"Card: {card['name']}, DL: {card['DL_price']}, MKM: {card['mkm_price']}, Diff: {card['difference']}%")

# print("\nFoil cards sorted by dl_price:")
# for card in sorted_foil_cards:
#     print(f"Card: {card['name']}, Foil, DL: {card['DL_price']}, MKM: {card['mkm_price']}, Diff: {card['difference']}%")

# Get the name of a card

# get all the cards with the same name from the scryfall list

# Convert the eu price to sec prices

# check if the card has the same or a lower price

# put them in to tiers

# 10% less

# 20% less

# 30% less

# more 

# with open(file_path, 'a') as file:
#     file.write(json.dumps(allcards.text))
