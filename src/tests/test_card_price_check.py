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
        "id": 61953,
        "slug": "61953-alibou-ancient-witness",
        "name": "Alibou, Ancient Witness",
        "rarity": "M",
        "extendedRarity": None,
        "multiverse_id": 518313,
        "collector_number": 7,
        "foil": True,
        "flip": False,
        "flipImage": "http://i.tcgplayer.com/236059_1_200w.jpg",
        "image_flip": "http://i.tcgplayer.com/236059_1_200w.jpg",
        "legal": True,
        "image": "https://static.mtgstocks.com/cardimages/518313.png",
        "mkm_url": "/en/Magic/Products/Singles/Commander-Strixhaven/Alibou-Ancient-Witness",
        "tcg_id": 236059,
        "tcg_url": "https://tcgplayer.pxf.io/rQbqQd?u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F236059%2Fmagic-commander-2021-alibou-ancient-witness&subId2=prints",
        "cardtrader_id": 154627,
        "scryfallId": "fd2fc2d4-c4fb-4dcb-93fa-aaf8c1182f15",
        "card": {
            "id": 28132,
            "cmc": 5,
            "manaCost": "{3}{R}{W}",
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
            "lowest_print": 62440,
            "name": "Alibou, Ancient Witness",
            "oracle": "Other artifact creatures you control have haste.\nWhenever one or more artifact creatures you control attack, Alibou, Ancient Witness deals X damage to any target and you scry X, where X is the number of tapped artifacts you control.",
            "power": "4",
            "toughness": "5",
            "loyalty": None,
            "reserved": False,
            "subtype": "Golem",
            "supertype": "Legendary Artifact Creature",
            "content_warning": False,
            "edhrecUrl": "/commanders/alibou-ancient-witness",
        },
        "card_set": {
            "id": 513,
            "name": "Commander 2021",
            "abbreviation": "C21",
            "icon_class": "ss-c21",
            "set_type": "commander",
            "mkm_id": 3756,
            "slug": "513-commander-2021",
        },
        "all_time_high": {"avg": 18.99, "date": 1710806400000},
        "all_time_low": {"avg": 0.75, "date": 1654128000000},
        "buyList": {"nm": None, "lp": None, "nmFoil": 6.96, "lpFoil": 6.97},
        "change": {"yesterday": 0, "lastWeek": -1.51, "lastMonth": 7.99},
        "latest_price": {
            "low": None,
            "avg": 13.49,
            "high": None,
            "foil": 13.49,
            "market": 11.41,
            "market_foil": 11.41,
            "date": 1712361600000,
        },
        "latest_price_ck": {
            "price": None,
            "foil": 13.99,
            "url": None,
            "urlFoil": "https://www.cardkingdom.com/mtg/commander-2021/alibou-ancient-witness-foil",
        },
        "latest_price_mkm": {"avg": 3.46, "low": 1.5},
        "latest_price_cardtrader": {"avg": 11.03, "low": 4.04},
        "sets": [
            {
                "id": 62440,
                "slug": "62440-alibou-ancient-witness-extended-art",
                "image": "https://static.mtgstocks.com/cardimages/521603.png",
                "name": "Alibou, Ancient Witness",
                "icon_class": "ss-c21",
                "legal": True,
                "content_warning": False,
                "rarity": "M",
                "set_id": 513,
                "set_name": "Commander 2021",
                "latest_price": 29.99,
                "latest_price_mkm": 9.1,
            }
        ],
    }
 
    responses.add(
        responses.GET,
        f'https://api.mtgstocks.com/prints/{slug_name}',
        json=mock_response,
        status=200
    )

    result = get_list_of_prices_for_card(slug_name)

    assert result == [9.1, 3.46]

