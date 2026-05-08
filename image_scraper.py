import os
import jpg6
import ehen
import constants
from urllib.parse import urlparse

# check if the necessary directories exist and create them if not.
def base_directories_check():
    if not os.path.exists(constants.download_directory):
        os.mkdir(constants.download_directory)

    if not os.path.exists(constants.config_directory):
        os.mkdir(constants.config_directory)


def open_urls_file():
    urls_file_path = os.path.join(constants.config_directory, constants.url_file_name)

    if not os.path.exists(urls_file_path): # if URLs.txt doesn't exist, create it
        with open(urls_file_path, "w") as f:
            f.write("# Enter URLs here, one per line. Supported hosts: jpg6.su, e-hentai.org")

    with open(urls_file_path, "r") as f:
        urls = []
        for line in f.read().splitlines():
            line = line.strip()

            if not line or line.startswith("#"): # skip empty lines and comments
                continue

            urls.append(line)

    return urls


def get_base_url(url: str) -> str:
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def main():
    run_type_select = 0
    while run_type_select < 1 or run_type_select > len(constants.run_type):
        print("Select a run type:")
        
        for i, rtype in enumerate(constants.run_type):
            print(f"{i + 1}. {rtype}")

        run_type_select = int(input("\nChoose a run type: "))

    for url in open_urls_file():
        base_url = get_base_url(url)
        print(f"\nProcessing URL: {url}")

        match constants.image_hosts_urls[base_url]:
            case "jpg6":
                jpg6.jpg6(url).main(url, run_type_select)
            case "e-hentai":
                ehen.ehen(url).main(url, run_type_select)
            case "EveriaClub":
                print("EveriaClub support coming soon!")
            case "bunkr":
                print("bunkr support coming soon!")
            case _:
                print("Host not supported. Please enter a valid URL from the supported hosts.")


if __name__ == "__main__":
    base_directories_check() # should always be run first before anything else to ensure the necessary directories exist
    main()
