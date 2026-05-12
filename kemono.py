import os
import requests
from bs4 import BeautifulSoup
from scraper import Scraper

class kemono(Scraper):
    def __init__(self, url: str):
        super().__init__(url)

    # page scraping isn't needed as the image URLs are all on the same page.

    def main(self, myURL: str, run_type_select: int):
        response = requests.get(myURL)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")

        if run_type_select == 1:
            super().bs_output_save(soup)

        elif run_type_select == 2:
            print("Kemono image scraping coming soon!")

            tag = soup.find('a', class_=["fileThumb", "image-link"])
            if tag and tag.get("href"):
                image_link = tag["href"]
                print(f"Image link: {image_link}")
            else:
                print("No image link found")