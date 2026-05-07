
import jpg6
import ehen
import constants
from urllib.parse import urlparse
import requests


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

    url = input("Enter the desired URL: ")
    base_url = get_base_url(url)

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
    main()
