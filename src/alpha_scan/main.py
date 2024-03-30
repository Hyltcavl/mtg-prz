import datetime
import json
from bs4 import BeautifulSoup
import requests
import re

from src.resources.file_io import print_to_new_file
from src.resources.other import date_time_as_string, get_time_difference_in_minutes

start_time = datetime.datetime.now()
start_time_as_string = date_time_as_string(start_time)

# Get the page with all the sets
sets_page = requests.get("https://alphaspel.se/1978-mtg-loskort/")

# list all the sets
soup = BeautifulSoup(sets_page.text, 'html.parser')
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
    link = f'https://alphaspel.se{set_href}?order_by=stock_a&ordering=desc&page=1'
    print(link)
    set_initial_page = requests.get(link)
    soup = BeautifulSoup(set_initial_page.text, 'html.parser')
    try:
        pages_html = soup.find(class_="pagination pagination-sm pull-right").find_all('li')
        pages_html.pop() #Removes the pagination arrows element
        pages = int(pages_html.pop().text.strip())
    except:
        pages = 1
    
    for x in range(1,pages+1):
        link = f'https://alphaspel.se{set_href}?order_by=stock_a&ordering=desc&page={x}'
        set_page = requests.get(link)
        soup = BeautifulSoup(set_page.text, 'html.parser')
        try:
            products = soup.find(class_="products row").find_all(class_="product")
        except:
            products = []
        
        for product in products:

            in_stock = product.find(class_="stock").text.strip()
            if in_stock == "Slutsåld":
                continue

            product_name = product.find(class_="product-name")
            set_name = product_name.text.strip().split(":")

            ##Regular name and set

            if len(set_name) == 3:
                try:
                    raw_name = set_name[2].replace("(Begagnad)", "").strip()
                    set = set_name[1].strip()
                except:
                    raw_name = set_name[1].replace("(Begagnad)", "").strip()
                    set_name[1] = "unknown"
            
            ##universes beyond: somthing kind of set names with extra :
            else:
                try:
                    raw_name = set_name[3].replace("(Begagnad)", "").strip()
                    set = f'{set_name[1]} {set_name[2]}'.strip()

                except:
                    raw_name = set_name[1].replace("(Begagnad)", "").strip()
                    set_name[1] = "unknown"

            #Skipp token cards
            if bool(re.search(r'Token', raw_name, re.IGNORECASE)):
                continue

            price = product.find(class_="price text-success").text
            match = re.search(r'\d+', price)

            foil = bool(re.search(r'\(Foil\)', raw_name, re.IGNORECASE)) or bool(re.search(r'\(Etched Foil\)', raw_name, re.IGNORECASE)) or bool(re.search(r'\(Foil Etched\)', raw_name, re.IGNORECASE))

            name = re.sub(r'\([^()]*\)', '', raw_name).replace("v.2", "").replace("V.2", "").replace("v.1", "").replace("v.3", "").replace("v.4", "").strip()
            name = re.sub(r'\b(\w+)\s/\s(\w+)\b', r'\1 // \2', name) # adds another / when there's only one
            #Edgecases
            name = name.removeprefix("Commander 2016 ").removeprefix("Conflux ").removeprefix("Eventide ").removeprefix("Shadowmoor ").removeprefix("Planechase card bundle ")

            card = {
                 "name": name,
                 "set": set,
                 "price": int(match.group()),
                 "foil": foil
            }

            name = card["name"]
            if name not in grouped_cards:
                grouped_cards[name] = []
            grouped_cards[name].append(card)


print_to_new_file("alphaspel_cards", f'cards_{start_time_as_string}.json', json.dumps(grouped_cards))

difference_in_minutes =get_time_difference_in_minutes(start_time)
print(f'Alphaspel scan started {start_time_as_string} and took {difference_in_minutes}')
