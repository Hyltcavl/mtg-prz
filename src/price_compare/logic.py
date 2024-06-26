import json
import os
import re

from src.card_price_check.main import get_card_search_uri, get_list_of_prices_for_card
from src.scryfall.main import download_scryfall_cards


def get_scryfall_cards(today_date_as_string: str, folder_name="scryfall_cards") -> {}:
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_name = f"small_cards_{today_date_as_string}"
    scryfall_files = [
        file for file in os.listdir(folder_name) if file.startswith(file_name)
    ]

    if len(scryfall_files) == 0:
        download_scryfall_cards()
        scryfall_files = [
            file for file in os.listdir(folder_name) if file.startswith(file_name)
        ]
    else:
        print("scryfall cards already downloaded today")

    with open(f"{folder_name}/{scryfall_files[0]}", "rb") as f:
        scryfall_card_list = json.load(f)
    return scryfall_card_list


def compare_prices(cards_list: {}, scryfall_card_list: {}, store_name: str) -> []:
    prices_of_cards = []
    for card_name_original, cards in cards_list.items():
        card_name = re.sub(
            r"[^a-zA-Z]", "", card_name_original.replace("Æ", "Ae").lower()
        )

        scryfall_cards = scryfall_card_list.get(card_name)
        if scryfall_cards == None:
            for name, content in scryfall_card_list.items():
                name = name
                if name.startswith(card_name) or name.endswith(card_name):
                    scryfall_cards = content
        if scryfall_cards == None:
            print(f"Unable to find {card_name_original}")
            continue

        # find the lowest priced card of the scryfall cards
        lowest_eur, lowest_eur_foil, lowest_eur_set, lowest_eur_foil_set = get_lowest_price(scryfall_cards)

        # find the lowest priced alphaspel card
        lowest_price = float("inf")
        lowest_foil_price = float("inf")
        lowest_price_set = None
        lowest_foil_price_set = None

        for card in cards:
            price = round(card.get("price") * 0.087, 2)
            if price and float(price) < lowest_price:
                lowest_price = float(price)
                lowest_price_set = card.get("set")

            if (
                card.get("foil") == "true"
                and price
                and float(price) < lowest_foil_price
            ):
                lowest_foil_price = float(price)
                lowest_price_set = lowest_foil_price_set.get("set")

        price_compare_obj = {
            "name": card_name_original,
            "store_price": lowest_price if lowest_price != float("inf") else None,
            "store_set": lowest_price_set,
            "store_price_foil": (
                lowest_foil_price if lowest_foil_price != float("inf") else None
            ),
            "store_foil_set": lowest_foil_price_set,
            "mkm_price": lowest_eur if lowest_eur != float("inf") else None,
            "mkm_set": lowest_eur_set,
            "mkm_price_foil": (
                lowest_eur_foil if lowest_eur_foil != float("inf") else None
            ),
            "mkm_set": lowest_eur_foil_set,
            "store": store_name,
        }
        prices_of_cards.append(price_compare_obj)
    return prices_of_cards


def get_lowest_price(scryfall_cards: {}):
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

    return lowest_eur, lowest_eur_foil, lowest_eur_set, lowest_eur_foil_set


### Retruns list of cards with cards prices lower in store then MKM trend
def get_nice_prices(prices_of_cards: []):
    nice_prices = []

    for card in prices_of_cards:
        if (
            card["store_price"]
            and card["mkm_price"]
            and card["store_price"] < card["mkm_price"]
        ):
            percent_diff = (
                (card["mkm_price"] - card["store_price"]) / card["mkm_price"]
            ) * 100
            card_info = {
                "name": card["name"],
                "store_price": card["store_price"],
                "mkm_price": card["mkm_price"],
                "difference": round(percent_diff, 2),
            }
            nice_prices.append(card_info)

        if (
            card["store_price_foil"]
            and card["mkm_price_foil"]
            and card["store_price_foil"] < card["mkm_price_foil"]
        ):
            percent_diff = (
                (card["mkm_price_foil"] - card["store_price_foil"])
                / card["mkm_price_foil"]
            ) * 100
            card_info = {
                "name": card["name"],
                "foil": True,
                "store_price": card["store_price_foil"],
                "mkm_price": card["mkm_price_foil"],
                "difference": round(percent_diff, 2),
            }
            nice_prices.append(card_info)

    sorted_cards = sorted(
        nice_prices, key=lambda card: card.get("store_price", float("inf"))
    )

    return sorted_cards
