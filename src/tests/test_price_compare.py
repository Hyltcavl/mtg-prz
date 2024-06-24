from src.price_compare.logic import get_lowest_price


def test_get_lowest_price():
    example_scryfall_card = [
        {
            "name": "ravagesofwar",
            "set": "Portal Three Kingdoms",
            "prices": {
                "usd": "250.98",
                "usd_foil": None,
                "usd_etched": None,
                "eur": "88.27",
                "eur_foil": None,
                "tix": None,
            },
        },
        {
            "name": "ravagesofwar",
            "set": "Fallout",
            "prices": {
                "usd": "21.29",
                "usd_foil": "23.02",
                "usd_etched": None,
                "eur": None,
                "eur_foil": None,
                "tix": None,
            },
        },
        {
            "name": "ravagesofwar",
            "set": "Masters Edition II",
            "prices": {
                "usd": None,
                "usd_foil": None,
                "usd_etched": None,
                "eur": None,
                "eur_foil": None,
                "tix": "0.12",
            },
        },
        {
            "name": "ravagesofwar",
            "set": "Magic Online Promos",
            "prices": {
                "usd": None,
                "usd_foil": None,
                "usd_etched": None,
                "eur": None,
                "eur_foil": None,
                "tix": None,
            },
        },
        {
            "name": "ravagesofwar",
            "set": "Judge Gift Cards 2015",
            "prices": {
                "usd": None,
                "usd_foil": "115.03",
                "usd_etched": None,
                "eur": None,
                "eur_foil": "130.23",
                "tix": None,
            },
        },
        {
            "name": "ravagesofwar",
            "set": "Fallout",
            "prices": {
                "usd": None,
                "usd_foil": "64.53",
                "usd_etched": None,
                "eur": None,
                "eur_foil": None,
                "tix": None,
            },
        },
    ]

    lowest_eur, lowest_eur_foil, lowest_eur_set, lowest_eur_foil_set = get_lowest_price(
        example_scryfall_card
    )

    assert lowest_eur == 88.27
    assert lowest_eur_foil == 130.23
    assert lowest_eur_set == "Portal Three Kingdoms"
    assert lowest_eur_foil_set == "Judge Gift Cards 2015"
