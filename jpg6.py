import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import os
import time
from scraper import Scraper
from pathlib import Path


BASE = "https://jpg6.su" # might need to add multiple base URLs if the site has multiple subdomains or sections with different URL structures


class jpg6(Scraper):
    def __init__(self, url: str):
        Scraper.__init__(self, url)


    def get_next_page(self, soup: BeautifulSoup) -> str:
        tag = soup.find("a", attrs={"data-pagination": "next"})
        if tag and tag.get("href"):
            return urljoin(BASE, tag["href"])
        return None


    def scrape_pages(self, myURL: str):
        url = myURL
        pages = []

        print("Getting the number of pages...")

        while url:
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")

            pages.append(url)
            url = self.get_next_page(soup)

        return pages


    def image_scrape(self, images: list, folder_name: str):
        imageCount = 0

        print(f"-{len(images)} images found - ", end="")

    # From the image tag, Fetch image Source URL
        # 1.data-srcset
        # 2.data-src
        # 3.data-fallback-src
        # 4.src

        if len(images) != 0:
            for i, image in enumerate(images):

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
                    imageData = requests.get(image_link).content

                    try:
                        imageData = str(imageData, 'utf-8')

                    except UnicodeDecodeError: # If the content is not text, it will raise a UnicodeDecodeError which we can assume is an image.
                        image_name = image_link[image_link.rfind('/') + 1:] # remove everything before the last "/" to get the image name
                        base, ext = os.path.splitext(image_name) # base = image name, ext = image extension
                        folder_path = os.path.join(os.path.dirname(__file__), folder_name)
                        file_path = os.path.join(folder_path, image_name)


                        if Path(file_path).exists():
                            print(f" Image {image_name} already exists, adding a counter to the file name")
                            image_name = f"{base}({i}){ext}" # TODO: only increment i when there's already an image with the same name
                            file_path = os.path.join(folder_path, image_name) # build new file_path with the image name with counter

                        with open(file_path, "wb+") as f:
                            f.write(imageData) # save the file (with or without counter)

                            # only increment image count if an image was successfully saved.
                            percent = (i + 1) / len(images) * 100
                            sys.stdout.write(f"\rDownloading images: {percent:5.1f}% ({i + 1}/{len(images)})")
                            sys.stdout.flush()
                        
                            imageCount += 1

                except requests.exceptions.RequestException:
                    print("Unable to complete get request" . e)
                    pass

            if imageCount == len(images):
                print(" - All images downloaded")

            else:
                print(f"Downloaded {imageCount} out of {len(images)}")


    def main(self, myURL: str, run_type_select: int):

        response = requests.get(myURL)
        soup = BeautifulSoup(response.text, 'html.parser')

        if run_type_select == 1:
            super().bs_output_save(soup)    
        elif run_type_select == 2:
            tag = soup.find('a', {'data-text': True})
            folder_name = tag.contents[0] if tag.get('data-text') == 'album-name' else "jpg6_gallery" # name of the gallery. if it cannot be found, use "jpg6_gallery" as the default folder name
            download_path = super().create_save_directory(folder_name)

            print("Getting page links... ", end="")
            page_links = self.scrape_pages(myURL)
            print(f"Found {len(page_links)} pages")
            page = 1

            for p in page_links:
                print(f"Page {page} of {len(page_links)}", end="")
                response = requests.get(p)
                soup = BeautifulSoup(response.text, 'html.parser')
                images = soup.find_all('img')
                self.image_scrape(images, download_path)
                page += 1
            
        else:
            print("Invalid mode selected. Please enter 'html' or 'image'.")
