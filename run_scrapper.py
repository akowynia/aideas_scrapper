from configparser import RawConfigParser
import bs4
import logging
from databaseOperations import databaseOperations


#import scrappers
from scrappersClass.orange_scrapper import orange_scrapper
from scrappersClass.plus_scrapper import plus_scrapper
from scrappersClass.tmobile_scrapper import tmobile_scrapper
from scrappersClass.play_scrapper import play_scrapper
from scrappersClass.trustpilot_scrapper import trustpilot_scrapper
#inicjuje logowanie
logger = logging.getLogger('latest')

class run_scrapper:
    def __init__(self) -> None:
        pass

    def run(self):
        #wczytuje config, wersja raw z względu na "linki" które muszą być surowe bez zmian
        config = RawConfigParser()
        config_path = "configs/websites.ini"
        config.read(config_path)

        #odczytuje sekcje z pliku konfiguracyjnego
        sections = config.sections()

        #iteruje po sekcjach
        for list_website in sections:
            try:
                website_name = config[list_website]["website_name"]
                scrapper_class_name = f"{website_name}_scrapper"
                
                # Dynamicznie pobiera klasę scrappera na podstawie nazwy
                scrapper_class = globals().get(scrapper_class_name)
                if not scrapper_class:
                    logger.error(f"Scrapper class {scrapper_class_name} not found.")
                    continue

                
                scrapper_instance = scrapper_class()
                scrapper_instance.scrap(config[list_website]["website_to_scrap"])
            except Exception as e:
                logger.error(f"Error processing {list_website}: {e}")

    # Metody eksportujące dane do różnych formatów            
    def export_to_csv(self):
        """Export data to CSV file."""
        data_op = databaseOperations()
        data_op.export_to_csv()
        data_op.export_to_csv_opinions()
    def export_to_json(self):
        """Export data to JSON file."""
        data_op = databaseOperations()
        data_op.export_to_json()
        data_op.export_to_json_opinions()
    def export_to_pdf(self):
        """Export data to PDF file."""
        data_op = databaseOperations()
        data_op.export_to_pdf()
        data_op.export_to_pdf_opinions()
