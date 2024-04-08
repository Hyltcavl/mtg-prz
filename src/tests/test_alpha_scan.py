import responses
import urllib.parse
import pytest
from datetime import datetime
from bs4 import BeautifulSoup

from src.alpha_scan.logic import get_card_information
from src.resources.other import get_time_difference_in_minutes

def test_get_card_information_4_colons():
    # Read the HTML file
    with open('src/tests/alpha_4_part_name_card.html', 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    card = get_card_information(soup)

    assert card == {"name": "Commander's Sphere", "set": "Phyrexia: All Will Be One", "price": 5, "foil": False}


def test_get_card_information_2_colons():
    # Read the HTML file
    with open('src/tests/alpha_card.html', 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    card = get_card_information(soup)

    assert card == {"name": "Mantis Engine", "set": "10th Edition", "price": 5, "foil": False}


def test_fail_if_token():

    with open('src/tests/alpha_token.html', 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    with pytest.raises(AssertionError) as excinfo:
        card = get_card_information(soup)
    assert "Card is a token" in str(excinfo.value)
