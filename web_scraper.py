import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes():
    # fetch
    response = requests.get("https://quotes.toscrape.com")
    html = response.text

    # parse
    soup = BeautifulSoup(html, "html.parser")

    # find all - grabbing every element matching a pattern
    quote_divs = soup.find_all("div", class_="quote")

    quotes = []

    # loop - going through each match one at a time
    for quote_div in quote_divs:
        # extract - pull out specific piece of data from each element
        text = quote_div.find("span", class_="text").text
        author = quote_div.find("small", class_="author").text
        tags = [tag.text for tag in quote_div.find_all("a", class_="tag")]
        quote_dict = {"text": text, "author": author, "tags": tags}
        quotes.append(quote_dict)

    return quotes

def save_quotes(quotes):
    with open("quotes.json", "w") as f:
        json.dump(quotes, f)

def load_quotes():
    try:
        with open("quotes.json", "r") as f:
            quote = json.load(f)
        return quote
    except FileNotFoundError:
        return []

def show_all_quotes(quotes):
    for quote in quotes:
        print(f'Quote : {quote["text"]}\n -{quote["author"]} \nTags - {quote["tags"]}')

def most_quoted_author(quotes):
    freq = {}
    for quote in quotes:
        freq[quote["author"]] = freq.get(quote["author"], 0) + 1
    top_author = max(freq, key=freq.get)
    print(f"Most quoted author: {top_author} ({freq[top_author]} quotes)")

def filter_by_tags(quotes):
    choice = input("Enter the tag you want to search: ").lower()
    for quote in quotes:
        if choice in quote["tags"]:
            print(quote["text"])

def longest_qoute(quotes):
    longest = max(quotes, key=lambda x: len(x["text"]))
    print(f"Longest quote is:\n{longest['text']} - {longest['author']}")

def main():
    quotes = load_quotes()
    if not quotes:
        print("Scraping quotes.toscrape.com...")
        quotes = scrape_quotes()
        save_quotes(quotes)

    while True:
        print("1. Show all quotes\n2. Most quoted author\n3. Filter by tag\n4. Longest quote\n5. Quit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            show_all_quotes(quotes)
        elif choice == 2:
            most_quoted_author(quotes)
        elif choice == 3:
            filter_by_tags(quotes)
        elif choice == 4:
            longest_qoute(quotes)
        elif choice == 5:
            print("THANK YOU")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()