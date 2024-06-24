import requests
import re
from bs4 import BeautifulSoup


def get_amount_of_pages(cmc: int):
    # find how many pages exist with cards of the choosen cmc
    rsp = requests.get(
        f"https://astraeus.dragonslair.se/product/magic/card-singles/store:kungsholmstorg/cmc-{cmc}/1"
    )
    soup = BeautifulSoup(rsp.text, "html.parser")
    pages_count = 1  # default value if no pages are found
    try:
        a_element = (
            soup.find(class_="container align-center pagination")
            .find("ul")
            .find_all("li")
            .pop()
            .a
        )

        pattern = r'href="/.*?/(\d+)"'
        match = re.search(pattern, str(a_element))
        pages_count = int(match.group(1))
    except:
        print(f"no pages found on cmc-{cmc}, using default value {pages_count}")
    return pages_count


def parse_html(html_doc):
    # Parse the HTML document
    soup = BeautifulSoup(html_doc, "html.parser")

    # Find the table with class "products"
    products_table = soup.find("table", class_="products")
    card_list = []
    if products_table:
        # Find all <tr> elements within the table
        tr_elements = products_table.find_all("tr")
        tr_elements.pop(0)  # remove a unused row of elements

        for tr in tr_elements:
            card = getCard(tr)
            if card != {}:
                card_list.append(getCard(tr))
    else:
        print("Table with class 'products' not found in the HTML document.")
    return card_list


def getCard(tr):
    tds = tr.find_all("td")

    name_element = tds[0].find("a", class_="fancybox")
    name = ""
    if name_element == None:
        name = tds[0].text.strip()
    else:
        name = name_element.text.strip()

    if (
        bool(re.search(r"\(Skadad\)", name, re.IGNORECASE))
        or bool(re.search(r"\(Spelad\)", name, re.IGNORECASE))
        or bool(re.search(r"\( Skadad \)", name, re.IGNORECASE))
        or bool(re.search(r"\[Token\]", name, re.IGNORECASE))
    ):
        return {}

    foil = (
        bool(re.search(r"\(Foil\)", name, re.IGNORECASE))
        or bool(re.search(r"\(Etched Foil\)", name, re.IGNORECASE))
        or bool(re.search(r"\(Foil Etched\)", name, re.IGNORECASE))
    )

    prerelease = bool(re.search(r"\(Prerelease\)", name, re.IGNORECASE))

    showcase = bool(re.search(r"\(Showcase\)", name, re.IGNORECASE))

    extended_art = bool(re.search(r"\(Extended Art\)", name, re.IGNORECASE))

    set = tds[1].a.text.strip()
    if set == "":

        set = tds[1].a.img.get("title").strip()

    try:
        price = int(tds[6].text.strip().split()[0])
    except:
        price = 0

    try:
        trade_in_price_element = tr.find_all("span", class_="format-subtle")
        trade_in_price = int(trade_in_price_element[-1].text.strip().split()[0])
    except:
        trade_in_price = 0

    amount_element = tr.find("span", class_="stock")
    amount = int(amount_element.text.strip())

    return {
        "name": re.sub(r"\([^()]*\)", "", name).strip(),
        "foil": foil,
        "extendedArt": extended_art,
        "prerelease": prerelease,
        "showcase": showcase,
        "set": set,
        "price": price,
        "tradeInPrice": trade_in_price,
        "amount": amount,
    }
