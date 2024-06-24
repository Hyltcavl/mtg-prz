import responses
import urllib.parse

from src.card_price_check.main import get_card_search_uri, get_list_of_prices_for_card


@responses.activate
def test_get_slug():
    responses.reset()
    card_name = "dockside extortionist"
    mock_response = [
        {
            "id": 49390,
            "name": "Dockside Extortionist",
            "slug": "49390-dockside-extortionist",
        },
        {"id": 72314, "name": "Dockside Chef", "slug": "72314-dockside-chef"},
        {
            "id": 31234,
            "name": "Docent of Perfection",
            "slug": "31234-docent-of-perfection",
        },
        {"id": 55185, "name": "Doctor Theme Card", "slug": "55185-doctor-theme-card"},
        {
            "id": 109660,
            "name": "Doc Aurlock, Grizzled Genius",
            "slug": "109660-doc-aurlock-grizzled-genius",
        },
    ]
    card_name_utf8 = urllib.parse.quote(card_name)

    responses.add(
        responses.GET,
        f"https://api.mtgstocks.com/search/autocomplete/{card_name_utf8}",
        json=mock_response,
    )

    result = get_card_search_uri("dockside extortionist")

    assert result == "49390-dockside-extortionist"


@responses.activate
def test_get_list_of_prices_for_card():
    slug_name = "61953-alibou-ancient-witness"
    mock_response = {
        "id": 18211,
        "slug": "18211-ravages-of-war",
        "name": "Ravages of War",
        "rarity": "R",
        "extendedRarity": None,
        "multiverse_id": 10500,
        "collector_number": 17,
        "foil": False,
        "flip": False,
        "flipImage": "http://i.tcgplayer.com/512_1_200w.jpg",
        "image_flip": "http://i.tcgplayer.com/512_1_200w.jpg",
        "legal": True,
        "image": "https://static.mtgstocks.com/cardimages/s18211.png",
        "mkm_url": "/en/Magic/Products/Singles/Portal-Three-Kingdoms/Ravages-of-War",
        "tcg_id": 512,
        "tcg_url": "https://tcgplayer.pxf.io/rQbqQd?u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F512%2Fmagic-portal-three-kingdoms-ravages-of-war&subId2=prints",
        "cardtrader_id": 31107,
        "scryfallId": "11dca9ba-b27f-4af8-9962-3794e743886f",
        "card": {
            "id": 12547,
            "cmc": 4,
            "manaCost": "{3}{W}",
            "legal": {
                "duel": "legal",
                "brawl": "not_legal",
                "penny": "not_legal",
                "future": "not_legal",
                "legacy": "legal",
                "modern": "not_legal",
                "pauper": "not_legal",
                "alchemy": "not_legal",
                "pioneer": "not_legal",
                "vintage": "legal",
                "explorer": "not_legal",
                "historic": "not_legal",
                "standard": "not_legal",
                "commander": "legal",
                "gladiator": "not_legal",
                "oldschool": "not_legal",
                "premodern": "not_legal",
                "historicbrawl": "not_legal",
                "paupercommander": "not_legal",
            },
            "lowest_print": 107427,
            "name": "Ravages of War",
            "oracle": "Destroy all lands.",
            "power": None,
            "toughness": None,
            "loyalty": None,
            "reserved": False,
            "subtype": None,
            "supertype": "Sorcery",
            "content_warning": False,
            "edhrecUrl": "/cards/ravages-of-war",
        },
        "card_set": {
            "id": 98,
            "name": "Portal Three Kingdoms",
            "abbreviation": "PTK",
            "icon_class": "ss-ptk",
            "set_type": "special",
            "mkm_id": 30,
            "slug": "98-portal-three-kingdoms",
        },
        "all_time_high": {"avg": 5629.8, "date": 1617840000000},
        "all_time_low": {"avg": 149.95, "date": 1339891200000},
        "buyList": {"nm": 64.62, "lp": 72.69, "nmFoil": None, "lpFoil": None},
        "change": {"yesterday": -0.14, "lastWeek": -0.14, "lastMonth": 1.34},
        "latest_price": {
            "low": 229.98,
            "avg": 299.85,
            "high": 349.99,
            "foil": None,
            "market": 308.73,
            "market_foil": None,
            "date": 1712534400000,
        },
        "latest_price_ck": {
            "price": 229.99,
            "foil": None,
            "url": "https://www.cardkingdom.com/mtg/portal-3k/ravages-of-war",
            "urlFoil": None,
        },
        "latest_price_mkm": {"avg": 82.27, "low": 74.99},
        "latest_price_cardtrader": {"avg": 214.36, "low": 85.51},
        "sets": [
            {
                "id": 27961,
                "slug": "27961-ravages-of-war",
                "image": "https://static.mtgstocks.com/cardimages/s27961.png",
                "name": "Ravages of War",
                "icon_class": "ss-pmtg1",
                "legal": True,
                "content_warning": False,
                "rarity": "R",
                "set_id": 115,
                "set_name": "Judge Promos",
                "latest_price": 128.74,
                "latest_price_mkm": 300,
            },
            {
                "id": 107428,
                "slug": "107428-ravages-of-war-borderless-surge-foil",
                "image": "https://static.mtgstocks.com/cardimages/t107428.webp",
                "name": "Ravages of War",
                "icon_class": "ss-pip",
                "legal": True,
                "content_warning": False,
                "rarity": "M",
                "set_id": 1800,
                "set_name": "Universes Beyond: Fallout",
                "latest_price": 69.16,
                "latest_price_mkm": None,
            },
            {
                "id": 107427,
                "slug": "107427-ravages-of-war-borderless",
                "image": "https://static.mtgstocks.com/cardimages/t107427.webp",
                "name": "Ravages of War",
                "icon_class": "ss-pip",
                "legal": True,
                "content_warning": False,
                "rarity": "M",
                "set_id": 1800,
                "set_name": "Universes Beyond: Fallout",
                "latest_price": 23.18,
                "latest_price_mkm": None,
            },
        ],
    }

    responses.add(
        responses.GET,
        f"https://api.mtgstocks.com/prints/{slug_name}",
        json=mock_response,
        status=200,
    )

    result = get_list_of_prices_for_card(slug_name)

    assert result == [
        {"set": "Judge Promos", "price": 300},
        {"set": "Universes Beyond: Fallout", "price": None},
        {"set": "Universes Beyond: Fallout", "price": None},
        {"set": "Portal Three Kingdoms", "price": 82.27},
    ]

