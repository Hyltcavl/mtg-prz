import json
import os
import requests

from bs4 import BeautifulSoup
from datetime import datetime

from src.alpha_scan.logic import get_card_information
from src.resources.file_io import print_to_new_file
from src.resources.other import date_time_as_string, get_time_difference_in_minutes

# Check config
short_run = os.environ.get("SHORT", False)

start_time = datetime.now()
start_time_as_string = date_time_as_string(start_time)

# Get the page with all the sets
sets_page = requests.get("https://alphaspel.se/1978-mtg-loskort/")

# list all the sets
soup = BeautifulSoup(sets_page.text, "html.parser")
sets_list = soup.find(class_="nav nav-list").find_all("a")

sets_links = []
for set in sets_list:
    try:
        # print(set.attrs.get("href"))
        sets_links.append(set.attrs.get("href"))

    except:
        print(set)

grouped_cards = {}
for set_href in sets_links:
    link = f"https://alphaspel.se{set_href}?order_by=stock_a&ordering=desc&page=1"
    print(link)
    set_initial_page = requests.get(link)
    soup = BeautifulSoup(set_initial_page.text, "html.parser")
    try:
        pages_html = soup.find(class_="pagination pagination-sm pull-right").find_all(
            "li"
        )
        pages_html.pop()  # Removes the pagination arrows element
        pages = int(pages_html.pop().text.strip())
    except:
        pages = 1

    for x in range(1, pages + 1):
        link = f"https://alphaspel.se{set_href}?order_by=stock_a&ordering=desc&page={x}"
        set_page = requests.get(link)
        soup = BeautifulSoup(set_page.text, "html.parser")
        try:
            products = soup.find(class_="products row").find_all(class_="product")
        except:
            products = []

        for product in products:

            try:
                card = get_card_information(product)
            except:
                continue

            name = card["name"]
            if name not in grouped_cards:
                grouped_cards[name] = []
            grouped_cards[name].append(card)

    if short_run:
        break


print_to_new_file(
    "alphaspel_cards", f"cards_{start_time_as_string}.json", json.dumps(grouped_cards)
)

difference_in_minutes = get_time_difference_in_minutes(start_time)
print(f"Alphaspel scan started {start_time_as_string} and took {difference_in_minutes}")
