import datetime
import ijson
import requests
import json

def download_scryfall_cards():

    #Download all cards
    possible_downloads = requests.get("https://api.scryfall.com/bulk-data")

    download_uri = json.loads(possible_downloads.text)["data"][2]["download_uri"]
    allcards = requests.get(download_uri)

    date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
    file_path = f'scryfall_cards/cards_{date}.json'

    with open(file_path, 'wb') as f:
            f.write(allcards.content)

    #make the dowload more managable
    scryfall_card_list = []
    with open(file_path, 'rb') as f:
        parser = ijson.items(f, 'item')
        for obj in parser:
            if obj.get("layout") != "token": #Filtering out token cards
                scryfall_card = {
                    "name": obj.get("name"),
                    "set": obj.get("set_name"),
                    "prices": obj.get("prices")
                }
                scryfall_card_list.append(scryfall_card)

    grouped_cards = {}
    for card in scryfall_card_list:
        name = card["name"]
        if name not in grouped_cards:
            grouped_cards[name] = []
        grouped_cards[name].append(card)

    file_path_smaller = f'scryfall_cards/small_cards_{date}.json'
    with open(file_path_smaller, 'a') as file:
        file.write(json.dumps(grouped_cards))