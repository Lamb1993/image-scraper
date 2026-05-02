import os

class Scraper:
    def __init__(self, url):
        self.url = url


    def create_save_directory(self):
        try:
            project_directory = os.path.dirname(__file__)
            folder_name = input("Enter directory name: ")
            os.mkdir(os.path.join(project_directory, folder_name))
        
        except:
            print("Directory already exists")
        
        return folder_name
    

    def bs_output_save(self, bs):
        file_name = input("Webpage output file name: ")

        try:
            with open(f"{file_name}.html", "w", encoding='utf-8') as f:
                f.write(str(bs))
        except:
            print("Could not save BeautifulSoup output")

