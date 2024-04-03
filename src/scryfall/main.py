from datetime import datetime
import re
import ijson
import requests
import json

from src.resources.file_io import print_to_new_file, print_to_new_file_bytes
from src.resources.other import date_time_as_string


def download_large_scryfall_file(file_path: str, file_name: str):
    possible_downloads = requests.get("https://api.scryfall.com/bulk-data")
    download_uri = json.loads(possible_downloads.text)["data"][2]["download_uri"]
    all_cards = requests.get(download_uri)

    print_to_new_file_bytes(file_path, file_name, all_cards.content)


def download_scryfall_cards():

    # Download all cards
    file_path = "scryfall_cards"
    date_as_string = date_time_as_string(datetime.now())
    file_name = f"cards_{date_as_string}.json"
    download_large_scryfall_file(file_path, file_name)

    # make the dowload smaller
    scryfall_card_list = []
    with open(f"{file_path}/{file_name}", "rb") as f:
        parser = ijson.items(f, "item")
        for obj in parser:
            if obj.get("layout") != "token":  # Filtering out token cards
                scryfall_card = {
                    "name": re.sub(r"[^a-zA-Z]", "", obj.get("name").lower()),
                    "set": obj.get("set_name"),
                    "prices": obj.get("prices"),
                }
                scryfall_card_list.append(scryfall_card)

    grouped_cards = {}
    for card in scryfall_card_list:
        name = card["name"]
        if name not in grouped_cards:
            grouped_cards[name] = []
        grouped_cards[name].append(card)

    print_to_new_file(file_path, f"small_cards_{date_as_string}.json", json.dumps(grouped_cards))
