import requests
import bs4

from databaseOperations import databaseOperations


class orange_scrapper:
    def __init__(self) -> None:
        self.data_op = databaseOperations()

    def scrap(self, link):
        """   
        pobiera dane
        """
        url = link
        # nawiązuje połączenie
        res = requests.get(url)
        res.raise_for_status()
        # przekształca html obiekt bs4 do przeszukiwania strony
        content = bs4.BeautifulSoup(res.text, 'lxml-xml')

        elems = content.findAll('item')

        for elements in elems:

            # sprawdza czy pola które chcemy pobrać istnieją
            try:

                title = elements.find('title').get_text()
                link_article = elements.find('guid').get_text()
                text = elements.find('content:encoded').get_text()
                pubDate = elements.find('pubDate').get_text()

                db_website_name = "orange"
                # jeśli nie to sprawdza czy dany link istnieje w bazie danych
                if self.data_op.check_duplicate(link_article) is not False:
                    self.data_op.add(
                        db_website_name, link_article, title, text, pubDate)
            except Exception as e:
                print("not exist", e)
