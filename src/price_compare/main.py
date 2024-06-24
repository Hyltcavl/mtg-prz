from datetime import datetime
import json
import os

from src.price_compare.logic import compare_prices, get_nice_prices, get_scryfall_cards
from src.resources.file_io import print_to_new_file
from src.resources.other import date_time_as_string, get_time_difference_in_minutes
from src.scryfall.main import download_scryfall_cards

# Get scryfall cards
start_time = datetime.now()
today_date_as_string = datetime.now().strftime("%Y-%m-%d")
start_time_as_string = date_time_as_string(start_time)

scryfall_card_list = get_scryfall_cards(today_date_as_string)

# Get alphaspel cards
alphaspel_folder = "alphaspel_cards"
cards_file_prefix = f"cards_{today_date_as_string}"
files = [
    file for file in os.listdir(alphaspel_folder) if file.startswith(cards_file_prefix)
]
alphaspel_file = files[0]
with open(f"{alphaspel_folder}/{alphaspel_file}", "rb") as f:
    card_lists = json.load(f)
alphaspel_cards_list = card_lists

# Get dragonslair cards
dragonslair_folder = "dragonslair_cards"
cards_file_prefix = f"cards_{today_date_as_string}"
files = [
    file
    for file in os.listdir(dragonslair_folder)
    if file.startswith(cards_file_prefix)
]
dragonslair_file = files[0]
with open(f"{dragonslair_folder}/{dragonslair_file}", "rb") as f:
    cards_list = json.load(f)

dl_card_list_refined = {}
for block in cards_list:
    if block != None:
        dl_card_list_refined.update(block.get("cards"))
dragonslair_cards_list = dl_card_list_refined

prices_of_cards_alpha = compare_prices(
    alphaspel_cards_list, scryfall_card_list, "alphaspel"
)
prices_of_cards_dl = compare_prices(
    dragonslair_cards_list, scryfall_card_list, "alphaspel"
)

print_to_new_file(
    "results",
    f"alpha_prices_{start_time_as_string}.json",
    json.dumps(prices_of_cards_alpha),
)
print_to_new_file(
    "results", f"dl_prices_{start_time_as_string}.json", json.dumps(prices_of_cards_dl)
)

nice_prices_alpha = get_nice_prices(prices_of_cards_alpha)
nice_prices_dl = get_nice_prices(prices_of_cards_dl)

# Write the sorted lists to a JSON file
print_to_new_file(
    "nice_prices",
    f"alpha_cards_{today_date_as_string}.json",
    json.dumps(nice_prices_alpha),
)
print_to_new_file(
    "nice_prices", f"dl_cards_{today_date_as_string}.json", json.dumps(nice_prices_dl)
)

difference_in_minutes = get_time_difference_in_minutes(start_time)
print(
    f"Comparing prices started {start_time_as_string} and took {difference_in_minutes}"
)
