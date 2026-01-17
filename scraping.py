import requests
from bs4 import BeautifulSoup
import json

def parse_quotes():
    BASE_URL = "http://quotes.toscrape.com"
    quotes_list = []
    authors_dict = {}
    page = 1

    while True:
        response = requests.get(f"{BASE_URL}/page/{page}/")
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.select(".quote")
        if not quotes:
            break

        for quote in quotes:
            text = quote.select_one(".text").get_text(strip=True)
            author_name = quote.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in quote.select(".tags .tag")]

            quotes_list.append({
                "text": text,
                "author": author_name,
                "tags": tags
            })

            if author_name not in authors_dict:
                author_url = BASE_URL + quote.select_one("span a")["href"]
                author_resp = requests.get(author_url)
                author_soup = BeautifulSoup(author_resp.text, "html.parser")
                authors_dict[author_name] = {
                    "fullname": author_name,
                    "born_date": author_soup.select_one(".author-born-date").get_text(strip=True),
                    "born_location": author_soup.select_one(".author-born-location").get_text(strip=True),
                    "description": author_soup.select_one(".author-description").get_text(strip=True)
                }

        page += 1

    return quotes_list, list(authors_dict.values())


if __name__ == "__main__":
    quotes_data, authors_data = parse_quotes()

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=4)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors_data, f, ensure_ascii=False, indent=4)

    print("Готово! Файли quotes.json та authors.json створені.")

