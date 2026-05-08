import os

url_file_name = "URLs.txt"
image_hosts_urls = {
    "https://jpg6.su": "jpg6",
    "https://e-hentai.org": "e-hentai",
    "https://www.everiaclub.com": "EveriaClub",
    "https://bunkr.is": "bunkr"
}
run_type = ["html", "images"]
download_directory = os.path.join(os.path.dirname(__file__), "Downloads")
config_directory = os.path.join(os.path.dirname(__file__), "Config")