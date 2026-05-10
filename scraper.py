import os
import constants
from bs4 import BeautifulSoup

# Scraper class that contains shared methods for all scrapers to use. This is to avoid code 
# duplication and make it easier to maintain the codebase. Each scraper can inherit from this 
# class and use its methods without having to rewrite them.

class Scraper:
    def __init__(self, url: str):
        self.url = url

    # remove any invalid characters from the file name
    def sanitize_file_name(self, file_name: str) -> str:
        invalid_chars = '<>:"|?*\\//'
        for char in invalid_chars:
            file_name = file_name.replace(char, '_') # replace with _, is it better to just remove?
        
        return file_name


    def get_next_page(self, soup: BeautifulSoup):
        return None
    
    
    def scrape_pages(self, myURL: str):
        return None


    def image_scrape(self, images: list, folder_name: str):
        return None


    def create_save_directory(self, folder_name: str) -> str:       
        folder_name = self.sanitize_file_name(folder_name)
        download_path = os.path.join(constants.download_directory, folder_name)
        
        try:
            os.mkdir(download_path)
        
        except:
            print("Directory already exists")
        
        return download_path
    

    def bs_output_save(self, bs: BeautifulSoup):
        file_name = input("Webpage output file name: ")

        try:
            with open(f"{file_name}.html", "w", encoding='utf-8') as f:
                f.write(str(bs))
        except:
            print("Could not save BeautifulSoup output")

