from datetime import datetime
import requests
import json
import re
import os
import concurrent.futures

from src.dl_scan.logic import get_amount_of_pages, parse_html
from src.resources.file_io import print_to_new_file
from src.resources.other import date_time_as_string, get_time_difference_in_minutes

# Check config
short_run = os.environ.get("SHORT", False)

# Create a folder if needed
folder_name = "dragonslair_cards"
# os.makedirs(folder_name, exist_ok=True)

# Create and open file
starting_time = datetime.now()
start_time_as_string = date_time_as_string(starting_time)
file_name = f"cards_{start_time_as_string}.json"


def get_cards(x, y) -> {}:
    try:
        request_link = f"https://astraeus.dragonslair.se/product/magic/card-singles/store:kungsholmstorg/cmc-{x}/{y}"
        print(request_link)
        rsp = requests.get(request_link)
        card_list = parse_html(rsp.text)

        grouped_cards = {}

        for card in card_list:
            name = card["name"]
            if name not in grouped_cards:
                grouped_cards[name] = []
            grouped_cards[name].append(card)

        return {"link": request_link, "cards": grouped_cards}

    except Exception as error:
        print(request_link)
        print(f"unable to fetch/print {x} because: {error}")


link_cards_list = []
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = []
    for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16]:
        pages = get_amount_of_pages(x)
        for y in range(1, pages + 1):
            futures.append(executor.submit(get_cards, x, y))
            if short_run:
                break

    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            link_cards_list.append(result)
            if short_run:
                break
        except Exception as e:
            print(f"An error occurred: {e}")


print_to_new_file(folder_name, file_name, json.dumps(link_cards_list))
difference_in_minutes = get_time_difference_in_minutes(starting_time)
print(
    f"Dragonslair scan started {start_time_as_string} and took {difference_in_minutes}"
)
