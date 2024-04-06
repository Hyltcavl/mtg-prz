import requests
import urllib.parse


def get_card_search_uri(card_name: str):
    card_name_utf8 = urllib.parse.quote(card_name)
    url = f"https://api.mtgstocks.com/search/autocomplete/{card_name_utf8}"

    # returns list oh objects: {"id":61953,"name":"Alibou, Ancient Witness","slug":"61953-alibou-ancient-witness"}
    # The slug is the end refernce used to get the info for a card using the
    response = requests.get(
        url,
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,sv-SE;q=0.8,sv;q=0.7,nb;q=0.6",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        },
    )

    if response.status_code == 200:
        # Extract the JSON data
        data = response.json()

        # Filter the list to include only objects with "Token" in the name
        token_objects = [obj for obj in data if "Token" not in obj["name"]]
        if len(token_objects) != 0:
            return token_objects[0].get("slug")
    raise IndexError("No nontoken card found")


def get_list_of_prices_for_card(slug: str) -> [str]:
    slug_utf8 = urllib.parse.quote(slug)
    url = f"https://api.mtgstocks.com/prints/{slug_utf8}"

    response = requests.get(
        url,
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,sv-SE;q=0.8,sv;q=0.7,nb;q=0.6",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        },
    )

    if response.status_code == 200:
        # Extract the JSON data
        data = response.json()

        current_card_set_mkm_price_trend = data.get("latest_price_mkm").get("avg")

        prices = [obj.get("latest_price_mkm") for obj in data.get("sets")]
        prices.append(current_card_set_mkm_price_trend)
        return prices

    raise IndexError(f"Bad response from api: {response.json()}")
