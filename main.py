import sqlite3  # import database

# import logger
import logging
from fpdf import FPDF  # Dodany import
# import configs
from configparser import ConfigParser
from run_scrapper import run_scrapper
import os.path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

#tworzy konfiguracje  pliku ini
def createConfig():
    config = ConfigParser()


    if not os.path.isfile("configs/websites.ini"):
        try:
            config["Template"] = {'website_to_scrap': "template",

                            'website_name': "website_name"

                            }
            with open("configs/websites.ini", 'w') as configfile:
                config.write(configfile)

            logger.info('Template config has created.')
        except:
            logger.error('Template config not created.')




# tworzy bazę danych sqllite
def createDatabase():
    
    #tworzy folder configs jeśli nie istnieje
    if not os.path.isdir("configs"):
        os.makedirs("configs", exist_ok=True)
        config_path = os.path.abspath("configs")
        logger.info('Config folder created.')

    
    #tworzy bazę danych jeśli nie istnieje
    if not os.path.isfile("news_bot.db"):
        try:
            db = sqlite3.connect("news_bot.db")
            cursor = db.cursor()



            #wykonuje kwerendę tworzącą tabele
            cursor.execute('''
       CREATE TABLE BlogInformation(
        id integer,
        websiteName varchar,
        currentTime  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        link varchar,
        title varchar,
        text varchar,
        pubDate varchar,                   
        PRIMARY KEY(id)

         );

            ''')
        
            db.commit()
            # cursor.execute(sql,data)
            db.close()
            logger.info('Created database.')
        except:
            logger.error('Database not created.')
    if not os.path.isfile("opinions_bot.db"):
        try:
            db = sqlite3.connect("opinions_bot.db")
            cursor = db.cursor()



            #wykonuje kwerendę tworzącą tabele
            cursor.execute('''
       CREATE TABLE OpinionsInformation(
        id integer,
        operatorName varchar,
        currentTime  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        text varchar,
        pubDate varchar,                   
        PRIMARY KEY(id)

         );

            ''')
        
            db.commit()
            # cursor.execute(sql,data)
            db.close()
            logger.info('Created database.')
        except:
            logger.error('Database not created.')


# inicjuje logger, loguje błędy i to co się dzieje
logging.basicConfig(filename="latest.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

#inicjuje logger o nazwie latest
logger = logging.getLogger('latest')

logger.info('Script has started.')

# wywołuje sprawdzanie baz i konfiguracji
createDatabase()
createConfig()

# #uruchamia całą logikę programu 
try:
    # uruchamia scrapery
    run_scrapper = run_scrapper()
    run_scrapper.run()

    # eksportuje dane do plików
    run_scrapper.export_to_pdf()
    run_scrapper.export_to_csv()
    run_scrapper.export_to_json()


except:
    logger.error('Error in run_scrapper.py')
    