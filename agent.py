from ddgs import DDGS
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()

def search_web(query):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=3):
            results.append({
                "title" : r["title"],
                "url" : r["href"],
                "snippet" : r["body"]
            })
    return results

def read_page(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return text[:2000]

if __name__ == "__main__":
    results = search_web("AI tools for HR teams in UAE")
    for r in results:
        print(r)

    first_url = results[0]["url"]
    print("\nReading first resulti...")
    page_text = read_page(first_url)
    print(page_text)