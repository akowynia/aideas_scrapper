import requests
import bs4
import time
from databaseOperations import databaseOperations


class play_scrapper:
    def __init__(self) -> None:
        self.data_op = databaseOperations()

    def scrap(self, link):
        """   
        pobiera dane
        """
        url = link
        new_link = ""
        for i in range(0, 30):
            new_link = url + str(i*12)
            print("current link", new_link)
            #nawiązuje połączenie
            res = requests.get(new_link)
            res.raise_for_status()
            #przekształca html obiekt bs4 do przeszukiwania strony
            content = bs4.BeautifulSoup(res.text, 'html.parser')
         
            #szuka elentu
        
            elems = content.findAll('div', class_='publication-list')
            elems = elems[0].findAll('h2')
            for elements in elems:
                
                link_website = elements.find('a').get('href')

                #time.sleep(2)
                res = requests.get(link_website)
                res.raise_for_status()
                content = bs4.BeautifulSoup(res.text, 'html.parser')

            
                title = content.find('h1',class_='publication__title').get_text()
                empty_text = content.find('div',class_="publication__content").get_text()
               

                db_website_name = "play"
                pubDate = content.find('div', class_='publication__date').get_text()
                #print(title, link_website, empty_text, pubDate)
                try:
                    if self.data_op.check_duplicate(link_website) is not False:
                            self.data_op.add(db_website_name,link_website, title, empty_text,pubDate)
                except Exception as e:
                    print("Error while adding to database:", e)

