from datetime import date
import datetime
import requests
import json
import re
import os
from bs4 import BeautifulSoup

from src.dl_scan.logic import get_amount_of_pages, parse_html

# Create a folder if needed
folder_name = "dragonslair_cards" 
os.makedirs(folder_name, exist_ok=True)

# Create and open file
start_time = datetime.datetime.now()
start_time_as_string = start_time.strftime("%Y-%m-%d_%H:%M")
file_name = f'cards_{start_time_as_string}.json'
file_path = os.path.join(folder_name, file_name)
with open(file_path, 'a') as file:
    file.write("[")


### Gets a specific page for debugging

# try:
#     request_link = "https://astraeus.dragonslair.se/product/magic/card-singles/store:kungsholmstorg/cmc-10/1"
#     rsp = requests.get(request_link)
#     card_list = parse_html(rsp.text)

#     with open(file_path, 'a') as file:
#         obj = {
#                     "link": request_link,
#                     "cards": card_list
#                 }
#         file.write(json.dumps(obj))
#         file.write(",")

# except Exception as error:
#     print(request_link)
#     print(f'unable to fetch/print because: {error}')
# raise Exception("STOP")


## get's all the cards
## Amount of cmcs, skipps 14 because it contains all dragonslairs cards..

for x in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,16]:

    pages = get_amount_of_pages(x)

    for y in range(1,pages):
        try:
            request_link = f'https://astraeus.dragonslair.se/product/magic/card-singles/store:kungsholmstorg/cmc-{x}/{y}'
            rsp = requests.get(request_link)
            card_list = parse_html(rsp.text)

            grouped_cards = {}

            for card in card_list:
                name = card["name"]
                if name not in grouped_cards:
                    grouped_cards[name] = []
                grouped_cards[name].append(card)

            with open(file_path, 'a') as file:
                obj = {
                            "link": request_link,
                            "cards": grouped_cards
                        }
                file.write(json.dumps(obj))
                if x != 16:
                    file.write(",")

        except Exception as error:
            print(request_link)
            print(f'unable to fetch/print {x} because: {error}')


with open(file_path, 'a') as file:
    file.write("]")

difference_in_minutes = ( datetime.datetime.now() - start_time).total_seconds() / 60
print(f'Dragonslair scan started {start_time_as_string} and took {difference_in_minutes}')