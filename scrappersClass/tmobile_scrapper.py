import requests
import bs4
import time
from databaseOperations import databaseOperations


class tmobile_scrapper:
    def __init__(self) -> None:
        self.data_op = databaseOperations()

    def scrap(self, link):
        """   
        pobiera dane
        """
        url = link
        new_link = ""
        for i in range(1, 31):
            new_link = url + str(i)
            print("current link", new_link)
            # nawiązuje połączenie
            res = requests.get(new_link)
            res.raise_for_status()
            # przekształca html obiekt bs4 do przeszukiwania strony
            content = bs4.BeautifulSoup(res.text, 'html.parser')

            elems = content.findAll('div', class_='p-6')
            elems = elems[0].findAll('a')
            for elements in elems:

                link_website = elements.get('href')
                link_website = "https://www.firma.t-mobile.pl" + link_website
                res = requests.get(link_website, verify=False)
                res.raise_for_status()
                content = bs4.BeautifulSoup(res.text, 'html.parser')

                title = content.find('h1').get_text()
                empty_text = content.findAll(
                    'div', class_="MuiGrid2-root")[14].get_text()

                db_website_name = "tmobile"
                pubDate = content.find('span', class_='text-sm').get_text()

                try:
                    if self.data_op.check_duplicate(link_website) is not False:
                        self.data_op.add(
                            db_website_name, link_website, title, empty_text, pubDate)
                except Exception as e:
                    print("Error while adding to database:", e)
