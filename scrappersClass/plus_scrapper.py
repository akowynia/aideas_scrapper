import requests
import bs4
import time
from databaseOperations import databaseOperations


class plus_scrapper:
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

            elems = content.findAll('div', class_='grid')
            elems = elems[1].findAll('a')

            for elements in elems:

                link_website = elements.get('href')

                res = requests.get(link_website)
                res.raise_for_status()
                content = bs4.BeautifulSoup(res.text, 'html.parser')

                title = content.find('h1').get_text()
                article = content.find('article')
                db_website_name = "plus"
                pubDate = content.find('p', class_='text-xs').get_text()
                pubDate = pubDate.split("  ")[-1]
                empty_text = ""
                text = article.findAll('p')
                for p in text:
                    empty_text += p.get_text() + "\n"

                try:
                    if self.data_op.check_duplicate(link_website) is not False:
                        self.data_op.add(
                            db_website_name, link_website, title, empty_text, pubDate)
                except Exception as e:
                    print("Error while adding to database:", e)
