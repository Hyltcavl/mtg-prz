import requests

def print_to_file(file_path: str, file_name: str, content: any) :
    with open(f'{file_path}/{file_name}', 'wb') as f:
            f.write(content)

# Get the page with all the sets



sets_page = requests.get("https://alphaspel.se/1978-mtg-loskort/")

print_to_file(".", sets_page.text)

# list all the sets