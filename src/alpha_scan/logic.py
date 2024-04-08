
import re


def get_card_information(product) -> {}:
    in_stock = product.find(class_="stock").text.strip()
    if in_stock == "Slutsåld":
        raise AssertionError("Card is Slutsåld")

    product_name = product.find(class_="product-name")

    if (
        product_name.text.lower().find("(italiensk)") != -1
        or product_name.text.lower().find("(tysk)") != -1
        or product_name.text.lower().find("(rysk)") != -1
    ):
        raise AssertionError("Card is not english")

    set_name = product_name.text.strip().split(":")

    ##Regular name and set
    if len(set_name) == 5:
        raw_name = set_name[4]
        set = (set_name[2] + ":" + set_name[3]).strip()

    elif len(set_name) == 3:
        try:
            raw_name = set_name[2]
            set = set_name[1].strip()
        except:
            raw_name = set_name[1]
            set_name[1] = "unknown"

    # Skipp token cards
    if bool(re.search(r"Token", raw_name, re.IGNORECASE)):
        raise AssertionError("Card is a token")

    price = product.find(class_="price text-success").text
    match = re.search(r"\d+", price)

    foil = (
        bool(re.search(r"\(Foil\)", raw_name, re.IGNORECASE))
        or bool(re.search(r"\(Etched Foil\)", raw_name, re.IGNORECASE))
        or bool(re.search(r"\(Foil Etched\)", raw_name, re.IGNORECASE))
    )
    raw_name = raw_name.replace("(Begagnad)", "").strip()
    name = (
        re.sub(r"\([^()]*\)", "", raw_name)
        .replace("v.2", "")
        .replace("V.2", "")
        .replace("v.1", "")
        .replace("v.3", "")
        .replace("v.4", "")
        .strip()
    )
    name = re.sub(
        r"\b(\w+)\s/\s(\w+)\b", r"\1 // \2", name
    )  # adds another / when there's only one
    # Edgecases
    name = (
        name.removeprefix("Commander 2016 ")
        .removeprefix("Conflux ")
        .removeprefix("Eventide ")
        .removeprefix("Shadowmoor ")
        .removeprefix("Planechase card bundle ")
    )

    card = {"name": name, "set": set, "price": int(match.group()), "foil": foil}
    return card
