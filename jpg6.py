import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import os
import time
from scraper import Scraper


BASE = "https://jpg6.su" # might need to add multiple base URLs if the site has multiple subdomains or sections with different URL structures


class jpg6(Scraper):
    def __init__(self, url):
        Scraper.__init__(self, url)


    def get_next_page(self, soup):
        tag = soup.find("a", attrs={"data-pagination": "next"})
        if tag and tag.get("href"):
            return urljoin(BASE, tag["href"])
        return None


    def scrape_pages(self, myURL):
        url = myURL
        pages = []

        print("Getting the number of pages...")

        while url:
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")

            pages.append(url)
            url = self.get_next_page(soup)

        return pages


    def image_scrape(self, images, folder_name):
        imageCount = 0

        print(f"{len(images)} images found - ", end="")

    # From the image tag, Fetch image Source URL
        # 1.data-srcset
        # 2.data-src
        # 3.data-fallback-src
        # 4.src

        if len(images) != 0:
            for i, image in enumerate(images):

                percent = i / len(images) * 100
                sys.stdout.write(f"\rDownloading images: {percent:5.1f}% ({i}/{len(images)})")
                sys.stdout.flush()

                # search for "data_srcset"
                try:
                    image_link = image["data_srcset"]

                # search for "data-src"
                except:
                    try:
                        image_link = image["data-src"]

                    # search for "data-fallback-src"
                    except:
                        try:
                            image_link = image["data-fallback-src"]

                        # search for "src"
                        except:
                            try:
                                image_link = image["src"]

                            except:
                                print("No source URL found")
                                pass

                time.sleep(0.5) # Sleep for 0.5 seconds to avoid overwhelming the server with requests

                try:
                    image_link = image_link.replace("md.", "") # Remove "md." from the URL to get the source image URL
                    myReq = requests.get(image_link).content

                    try:
                        myReq = str(myReq, 'utf-8')

                    except UnicodeDecodeError: # If the content is not text, it will raise a UnicodeDecodeError which we can assume is an image.
                        image_name = image_link[image_link.rfind('/'):] #remove everything before the last "/" to get the image name

                        with open(f"{folder_name}/{image_name}", "wb+") as f:
                            f.write(myReq)
                        
                        imageCount += 1

                except requests.exceptions.RequestException:
                    print("Unable to complete get request" . e)
                    pass

            if imageCount == len(images):
                print("All images downloaded")

            else:
                print(f"Downloaded {imageCount} out of {len(images)}")


    def main(self, myURL):

        response = requests.get(myURL)
        soup = BeautifulSoup(response.text, 'html.parser')

        run_type = input("Enter 'html' or 'image' mode: " )
        
        if run_type == "html":
            super().bs_output_save(soup)    
        elif run_type == "image":
            folder_name = super().create_save_directory()
            print("Getting page links...", end="")
            page_links = self.scrape_pages(myURL)
            print(f"Found {len(page_links)} pages")
            page = 1

            for p in page_links:
                print(f"Page {page} of {len(page_links)}", end="")
                response = requests.get(p)
                soup = BeautifulSoup(response.text, 'html.parser')
                images = soup.find_all('img')
                self.image_scrape(images, folder_name)
                page += 1
            
        else:
            print("Invalid mode selected. Please enter 'html' or 'image'.")
