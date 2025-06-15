import sqlite3  # import database
import os
from configparser import RawConfigParser
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import time
import json
import pandas as pd
from fpdf import FPDF

class databaseOperations:
    def __init__(self):
        pass
    
    # Sprawdza czy rekord istnieje w bazie danych
    def check_duplicate(self, link):
        """
        funkcja sprawdza duplikaty

        """
        db = sqlite3.connect('news_bot.db')
        cursor = db.cursor()

        # sprawdzające czy istnieje już taki link w bazie danych
        sql = ''' select link, title from BlogInformation where link like ? '''

        cursor.execute(sql, (link,))
        rows = cursor.fetchall()

        db.commit()
        db.close()
        # zwraca false jeśli nie ma duplikatu (sprawdza ilość występujących wierszy z bazy danych )
        if len(rows) != 0:
            return False

    # Sprawdza czy rekord istnieje w bazie danych
    def check_duplicate_opinions(self, text):
        """
        funkcja sprawdza duplikaty

        """
        db = sqlite3.connect('opinions_bot.db')
        cursor = db.cursor()

        # sprawdzające czy istnieje już taki link w bazie danych
        sql = ''' select text, pubDate from OpinionsInformation where text like ? '''

        cursor.execute(sql, (text,))
        rows = cursor.fetchall()

        db.commit()
        db.close()
        # zwraca false jeśli nie ma duplikatu (sprawdza ilość występujących wierszy z bazy danych )
        if len(rows) != 0:
            return False


    # Funkcja dodaje rekord do bazy danych
    def add(self, website_name, link, title, text, pub_date):
        """
        funkcja dodaje do bazy danych
        """

        db = sqlite3.connect('news_bot.db')
        cursor = db.cursor()

        # kwerenda insert into dodająca wartości do bazy danych
        sql = ''' INSERT INTO BlogInformation(websiteName, link, title, text,pubDate) VALUES(?,?,?,?,?); '''

        # wartość 0 jest statyczna bo słuzy do sprawdzania czy dany wiersz został już wysłany na discorda
        data = (website_name, link, title, text, pub_date)

        cursor.execute(sql, data)
        db.commit()
        db.close()
    # Funkcja dodaje rekord do bazy danych dla opinii
    def add_opinion(self, operatorName, text, pub_date):
        """
        funkcja dodaje do bazy danych
        """

        db = sqlite3.connect('opinions_bot.db')
        cursor = db.cursor()

        # kwerenda insert into dodająca wartości do bazy danych
        sql = ''' INSERT INTO OpinionsInformation(operatorName, text, pubDate) VALUES(?,?,?); '''

        # wartość 0 jest statyczna bo słuzy do sprawdzania czy dany wiersz został już wysłany na discorda
        data = (operatorName, text, pub_date)

        cursor.execute(sql, data)
        db.commit()
        db.close()



    # Funkcja eksportujące dane do różnych formatów
    def export_to_csv(self, filename="export.csv"):
        """
        funkcja eksportuje dane do pliku csv
        """


        db = sqlite3.connect('news_bot.db')
        df = pd.read_sql_query("SELECT * FROM BlogInformation", db)
        df.to_csv(filename, index=False)
        db.close()
        print(f"Data exported to {filename}")

    def export_to_csv_opinions(self, filename="export_opinions.csv"):
        """
        funkcja eksportuje dane do pliku csv
        """


        db = sqlite3.connect('opinions_bot.db')  
        df = pd.read_sql_query("SELECT * FROM OpinionsInformation", db)
        df.to_csv(filename, index=False)
        db.close()
        print(f"Data exported to {filename}")

    def export_to_json(self, filename="export.json"):
        """
        funkcja eksportuje dane do pliku json
        """

        db = sqlite3.connect('news_bot.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM BlogInformation")

        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        db.close()
        print(f"Data exported to {filename}")

    def export_to_json_opinions(self, filename="export_opinions.json"):
        """
        funkcja eksportuje dane do pliku json
        """
        import json

        db = sqlite3.connect('opinions_bot.db')  # Poprawka: była news_bot.db
        cursor = db.cursor()
        cursor.execute("SELECT * FROM OpinionsInformation")

        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        db.close()
        print(f"Data exported to {filename}")

    def export_to_pdf(self):
        """
        Eksportuje dane do PDF z obsługą polskich znaków
        """
        try:
            def clean_text(text):
                """Czyszczenie tekstu dla PDF - zachowuje polskie znaki, usuwa HTML"""
                if not text:
                    return ""
                text = str(text)
                
                # Usuń znaczniki HTML
                import re
                text = re.sub(r'<[^>]+>', '', text)
                
                # Usuń tylko znaki specjalne i nowe linie
                special_chars = {
                    '\u2013': '-', '\u2014': '-', '\u2015': '-',
                    '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
                    '\u201e': '"', '\u2026': '...', '\u00a0': ' ',
                    '\u00bb': '>>', '\u00ab': '<<', '\u2022': '*'
                }
                
                for special, ascii_char in special_chars.items():
                    text = text.replace(special, ascii_char)
                
                # Usuń znaki nowej linii
                text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
                
                # Usuń podwójne spacje
                while '  ' in text:
                    text = text.replace('  ', ' ')
                
                return text.strip()

            filename = f"export_{date.today()}.pdf"
            db = sqlite3.connect('news_bot.db')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM BlogInformation order by pubDate desc LIMIT 950")
            rows = cursor.fetchall()
            db.close()

            if not rows:
                print("No data found in BlogInformation table")
                return

            pdf = FPDF()
            
            for row in rows:
                pdf.add_page()
                pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
                pdf.set_font('DejaVu', '', 7)
                
                pdf.cell(0, 6, clean_text(f"ID: {row[0]}"), ln=True)
                pdf.cell(0, 6, clean_text(f"Operator: {row[1] or 'N/A'}"), ln=True)
                pdf.cell(0, 6, clean_text(f"Data: {row[2] or 'N/A'}"), ln=True)
                pdf.cell(0, 6, clean_text(f"Link: {row[3] or 'N/A'}"), ln=True)
                pdf.cell(0, 6, "Tytuł:", ln=True)
                pdf.multi_cell(0, 5, clean_text(f"{row[4] or 'N/A'}"))
                pdf.ln(2)
                pdf.cell(0, 6, "Treść:", ln=True)
                pdf.multi_cell(0, 4, clean_text(f"{row[5] or 'N/A'}"))
                pdf.ln(2)
                pdf.cell(0, 6, clean_text(f"Data publikacji: {row[6] or 'N/A'}"), ln=True)

            pdf.output(filename)
            print(f"Data exported to {filename}")

        except Exception as e:
            print(f"Error exporting to PDF: {e}")

    def export_to_pdf_opinions(self):
        """
        Eksportuje opinie do PDF z obsługą polskich znaków (każdy rekord na osobnej stronie)
        """
        try:
            def clean_text(text):
                """Czyszczenie tekstu dla PDF - zachowuje polskie znaki, usuwa HTML"""
                if not text:
                    return ""
                text = str(text)
                
                # Usuń znaczniki HTML
                import re
                text = re.sub(r'<[^>]+>', '', text)
                
                # Usuń tylko znaki specjalne i nowe linie
                special_chars = {
                    '\u2013': '-', '\u2014': '-', '\u2015': '-',
                    '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
                    '\u201e': '"', '\u2026': '...', '\u00a0': ' ',
                    '\u00bb': '>>', '\u00ab': '<<', '\u2022': '*'
                }
                
                for special, ascii_char in special_chars.items():
                    text = text.replace(special, ascii_char)
                
                text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
                
                while '  ' in text:
                    text = text.replace('  ', ' ')
                
                return text.strip()

            filename = f"opinions_export_{date.today()}.pdf"
            db = sqlite3.connect('opinions_bot.db')
            cursor = db.cursor()
            cursor.execute("SELECT id, operatorName, text, pubDate FROM OpinionsInformation where pubDate like '%2025' or pubDate like '%2024'   LIMIT 950")
            rows = cursor.fetchall()
            db.close()

            if not rows:
                print("No data found in OpinionsInformation table")
                return

            pdf = FPDF()

            for row in rows:
                pdf.add_page()
                # Dodaje czcionkę DejaVuSans.ttf, która obsługuje polskie znaki, czcionka musi być w tym samym katalogu co skrypt
                pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
                pdf.set_font('DejaVu', '', 7)
                
                pdf.cell(0, 6, clean_text(f"ID: {row[0]}"), ln=True)
                pdf.cell(0, 6, clean_text(f"Operator: {row[1] or 'N/A'}"), ln=True)
                pdf.cell(0, 6, "Treść opinii:", ln=True)
                opinion_text = clean_text(str(row[2] or 'N/A'))
                pdf.multi_cell(0, 4, opinion_text)
                pdf.ln(2)
                pdf.cell(0, 6, clean_text(f"Data publikacji: {row[3] or 'N/A'}"), ln=True)

            pdf.output(filename)
            print(f"Data exported to {filename}")

        except Exception as e:
            print(f"Error exporting opinions to PDF: {e}")