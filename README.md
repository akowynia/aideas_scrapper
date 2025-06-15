# AI Ideas - Scrapper

Bot do automatycznego scrapowania wiadomości z różnych stron internetowych i eksportowania danych do różnych formatów.

Realizacja w ramach działań pracy grupowej oraz wyzwania branżowego [Aideas](https://aideas.generatorpomyslow.pl)

## Funkcjonalności

- **Scraping wiadomości**: Automatyczne pobieranie artykułów z skonfigurowanych stron internetowych
- **Baza danych**: Przechowywanie danych w SQLite (news_bot.db, opinions_bot.db)
- **Eksport danych**: 
  - PDF (używając ReportLab)
  - CSV
  - JSON
- **Logowanie**: Szczegółowe logi operacji w pliku latest.log
- **Konfiguracja**: Łatwa konfiguracja stron do scrapowania przez plik INI

## Wymagania

```
sqlite3
logging
fpdf
configparser
reportlab
```

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/akowynia/aideas_scrapper.git

```

2. Zainstaluj wymagane biblioteki:
```bash
pip install fpdf reportlab configparser
```

## Struktura projektu

```
projekt/
├── main.py                 # Główny plik aplikacji
├── run_scrapper.py         # Logika scrapowania
├── configs/
│   └── websites.ini        # Konfiguracja stron do scrapowania
├── news_bot.db            # Baza danych wiadomości
├── opinions_bot.db        # Baza danych opinii
├── latest.log             # Plik logów
└── scrappersClass/            # Folder z klasami scrapującymi

```

## Konfiguracja

### Dodawanie nowych stron do scrapowania

Edytuj plik `configs/websites.ini`:

```ini
[Template]
website_to_scrap = template
website_name = website_name

[Przykład]
website_to_scrap = https://example-news.com
website_name = Example News
```

## Użytkowanie

Uruchom aplikację:

```bash
python main.py
```

Aplikacja automatycznie:
1. Utworzy niezbędne foldery i pliki konfiguracyjne
2. Zainicjuje bazy danych SQLite
3. Uruchomi proces scrapowania
4. Wyeksportuje dane do formatów PDF, CSV i JSON

## Bazy danych

### BlogInformation (news_bot.db)
- `id` - Unikalny identyfikator
- `websiteName` - Nazwa strony źródłowej
- `currentTime` - Czas dodania rekordu
- `link` - Link do artykułu
- `title` - Tytuł artykułu
- `text` - Treść artykułu
- `pubDate` - Data publikacji

### OpinionsInformation (opinions_bot.db)
- `id` - Unikalny identyfikator
- `operatorName` - Nazwa operatora/źródła
- `currentTime` - Czas dodania rekordu
- `text` - Treść opinii
- `pubDate` - Data publikacji

## Logowanie

Wszystkie operacje są logowane do pliku `latest.log` z timestampami i poziomami logowania.

## Eksport danych

Po zakończeniu scrapowania dane są automatycznie eksportowane do:
- **PDF** - Sformatowany dokument z artykułami
- **CSV** - Dane tabelaryczne do analizy
- **JSON** - Strukturalne dane do dalszego przetwarzania

## Błędy i rozwiązywanie problemów

- Sprawdź plik `latest.log` w przypadku błędów
- Upewnij się, że wszystkie wymagane biblioteki są zainstalowane
- Sprawdź konfigurację w `configs/websites.ini`

## Autor

Artur Kowynia
