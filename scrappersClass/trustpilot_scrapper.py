import requests
import bs4
import time
from databaseOperations import databaseOperations


class trustpilot_scrapper:
    def __init__(self) -> None:
        self.data_op = databaseOperations()

    def scrap(self, link):
        """   
        pobiera dane
        """
        url = link
        new_link = ""
        name_operator = ""

        for i in range(1, 31):
            new_link = url + str(i)
            print("current link", new_link)
            # nawiązuje połączenie
            res = requests.get(new_link)
            res.raise_for_status()
            # przekształca html obiekt bs4 do przeszukiwania strony
            content = bs4.BeautifulSoup(res.text, 'html.parser')
            name_operator = content.find(
                'span', class_='title_displayName__9lGaz').get_text()

            elems = content.findAll(
                'section', class_='styles_reviewListContainer__2bg_p')
            elems = elems[0].findAll('div', class_='styles_cardWrapper__g8amG')

            for elements in elems:
                remove_text = elements.find(
                    'h2', class_='typography_heading-xs__osRhC').get_text()
                opinion = elements.find('div', class_='styles_reviewContent__tuXiN').get_text(
                ).split('Data doświadczenia:')
                pubDate = opinion[1]
                opinion_text = opinion[0].replace(
                    remove_text, f"Nazwa opinii:{remove_text} Opinia:", 1)

                try:
                    if self.data_op.check_duplicate_opinions(opinion_text) is not False:
                        self.data_op.add_opinion(
                            name_operator, opinion_text, pubDate)
                except Exception as e:
                    print("Error while adding to database:", e)
