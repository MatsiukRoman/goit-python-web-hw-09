import requests
from bs4 import BeautifulSoup
import json

def main():
    base_url = "http://quotes.toscrape.com"
    page_url = "/page/1/"
    quotes = []
    authors = []
    seen_authors = set()

    while page_url:
        response = requests.get(base_url + page_url)
        soup = BeautifulSoup(response.text, "html.parser")
        quote_divs = soup.find_all("div", class_="quote")

        for quote_div in quote_divs:
            text = quote_div.find("span", class_="text").get_text(strip=True)
            author_name = quote_div.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote_div.find_all("a", class_="tag")]
            
            quotes.append({
                "tags": tags,
                "author": author_name,
                "quote": text
            })
                    
            if author_name not in seen_authors:
                author_url = quote_div.find("a")["href"]
                author_response = requests.get(base_url + author_url)
                author_soup = BeautifulSoup(author_response.text, "html.parser")
                
                born_date = author_soup.find("span", class_="author-born-date").get_text(strip=True)
                born_location = author_soup.find("span", class_="author-born-location").get_text(strip=True)
                description = author_soup.find("div", class_="author-description").get_text(strip=True)
                
                authors.append({
                    "fullname": author_name,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                })
                seen_authors.add(author_name)
                
        next_button = soup.find("li", class_="next")
        page_url = next_button.find("a")["href"] if next_button else None

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)
    print("Quotes have been successfully scraped and saved to quotes.json")

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)
    print("Authors' information has been successfully scraped and saved to authors.json")

if __name__ == '__main__':
    main()    


