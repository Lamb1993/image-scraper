from bs4 import BeautifulSoup
import requests
import os

def save_location_create(images):
    try:
        project_directory = os.path.dirname(__file__)
        folder_name = input("Enter directory name: ")
        os.mkdir(os.path.join(project_directory, folder_name))
    
    except:
        print("Directory already exists")
        
    image_scrape(images, folder_name)


def image_scrape(images, folder_name):
    imageCount = 0

    print(f"{len(images)} images found")

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

            try:
                myReq = requests.get(image_link).content
                try:

                    myReq = str(myReq, 'utf-8')

                except UnicodeDecodeError:
                    with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                        f.write(myReq)
                    
                    count += 1

            except:
                print("Unable to complete get request")
                pass

        if imageCount == len(images):
            print("All images downloaded")

        else:
            print(f"Downloaded {imageCount} out of {len(images)}")


def bs_output_save(bs):
    file_name = input("Enter webpage output file name: ")

    try:
        with open(f"{file_name}.html", "w", encoding='utf-8') as f:
            f.write(str(bs))
    except:
        print("Could not save BeautifulSoup output")


def main(myURL):

    response = requests.get(myURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    run_type = input("Enter 'output' or 'image' mode:" )
    if run_type == "output":
        bs_output_save(soup)    
    else:
        images = soup.findAll('img')
        save_location_create(images)

url = input("Enter the desired URL: ")
main(url)