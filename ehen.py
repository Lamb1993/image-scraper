import sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import os
import time
from scraper import Scraper
from fake_useragent import UserAgent
from pathlib import Path

KB = 1024
CHUNK_SIZE = 16 * KB

USER_AGENT_ROTATOR = UserAgent()

# multiple fake user-agents may be needed to avoid download rate issues. If the site detects too many requests from the same user-agent, 
# it may block the requests or serve a captcha which would require manual intervention to solve. By using multiple fake user-agents, 
# we can rotate through them to make it appear as if the requests are coming from different browsers and devices, which can help to avoid 
# detection and reduce the chances of being blocked.
BASE = "https://e-hentai.org" # might need to add multiple base URLs if the site has multiple subdomains or sections with different URL structures
URL_PAGE_SUFFIX = "?p=" # this is the suffix for pagination, it may need to be changed if the site uses a different pagination structure

sleepTime = 0.5

class ehen(Scraper):
    def __init__(self, myURL: str):
        Scraper.__init__(self, myURL)


    def get_total_pages(self, soup: BeautifulSoup) -> int:
        tag = soup.find("table", attrs={"class": "ptt"})

        if tag:
            tag = tag.find_all("td")[-2]

            if tag:
                tag = tag.find("a")

                if tag and tag.get("href"):
                    print(f"Total pages: {tag.contents[0]}")
                    return tag.contents[0]
        return None

    # create headers with a random user-agent to avoid download rate issues. The headers are prepared for each image request to make 
    # it appear as if the requests are coming from different browsers and devices, which can help to avoid detection and reduce the 
    # chances of being blocked by the server. 
    def prepare_headers(self, myURL: str) -> dict:
        host = urlparse(myURL).netloc
        # user_agent = USER_AGENT_ROTATOR.random
        user_agent = UserAgent().random
        return {
            "Host": host,
            "User-Agent": user_agent,
            "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive",
            "Referer": BASE,
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site",
        }


    def image_scrape(self, images: list, folder_name: str):
        imageCount = 0

        print(f"{len(images)} images found")

        if len(images) != 0:
            for i, image_link in enumerate(images):

                # Even 5 seconds is not long enough
                time.sleep(sleepTime) # sleep for some time to avoid download rate issues

                headers = self.prepare_headers(image_link)
                session = requests.Session()
                session.headers.update(headers)
                response = session.get(image_link)
                response.raise_for_status
                myReq = requests.get(image_link, headers=headers).content

                try:
                    myReq = str(myReq, 'utf-8')

                except UnicodeDecodeError: # If the content is not text, it will raise a UnicodeDecodeError which we can assume is an image.
                    image_name = image_link[image_link.rfind('/'):] #remove everything before the last "/" to get the image name
                    folder_path = os.path.join(os.path.dirname(__file__), folder_name)

                    with open(f"{folder_path}/{image_name}", "wb+") as f:
                        f.write(myReq) # save the file

                        percent = (i + 1) / len(images) * 100
                        sys.stdout.write(f"\rDownloading images: {percent:5.1f}% ({i + 1}/{len(images)})")
                        sys.stdout.flush()
                    
                    imageCount += 1

            if imageCount == len(images):
                print("\nAll images downloaded")

            else:
                print(f"Downloaded {imageCount} out of {len(images)}")


    def main(self, myURL: str, run_type_select: int):
        response = requests.get(myURL)
        soup = BeautifulSoup(response.text, 'html.parser')
        folder_name = soup.find("h1", id="gn").contents[0] # name of the gallery
        download_path = super().create_save_directory(folder_name)
            
        if run_type_select == 1:
            super().bs_output_save(soup)

        elif run_type_select == 2:
            number_of_pages = self.get_total_pages(soup)
            
            if number_of_pages is None: # assume 1 page in the gallery
                image_grid = soup.find('div', id="gdt")
                images_links = image_grid.find_all('a', href=True)
                image_list = [] # list of all the image source URL's

                print("Getting image links... ", end="")

                for link in images_links: # create a list of source image URL's for a given gallery page
                    response = requests.get(link['href'])
                    soup = BeautifulSoup(response.text, 'html.parser')
                    image = soup.find('img', id="img")
                    image_list.append(image["src"])

                self.image_scrape(image_list, download_path)
                
            else: # more than 1 page in the gallery
                for page in range(int(number_of_pages)): # go through each page in the gallery
                    print(f"Scraping page {page + 1} of {number_of_pages}...")
                    
                    response = requests.get(myURL + URL_PAGE_SUFFIX + str(page))
                    soup = BeautifulSoup(response.text, 'html.parser')

                    image_grid = soup.find('div', id="gdt")
                    images_links = image_grid.find_all('a', href=True)
                    image_list = [] # list of all the image source URL's

                    print("Getting image links... ", end="")
                    for link in images_links: # create a list of source image URL's for a given gallery page
                        response = requests.get(link['href'])
                        soup = BeautifulSoup(response.text, 'html.parser')
                        image = soup.find('img', id="img")
                        image_list.append(image["src"])

                    self.image_scrape(image_list, download_path)
        else:
            print("Invalid mode selected. Please enter 'html' or 'image'.")