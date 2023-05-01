# FBS-Scraper
A python micro-project, for collecting and cleaning forex news data from FBS. 
The program is able to retrieve historical exchange rates for a given range of dates and for a selection of currency pairs.
This is performed independantly by the phase_1_scrape.py file,
phase_2_clean.py will then clean the data, formatting it in a csv which can be further manipulated as per user requirements.

Running main.py weill run these 2 files sequentially.

## Prerequisites 
The following packages are required to run the program:
```
beautifulsoup4==4.11.2
requests==2.26.0
```

## Installing 

1. Clone the repository to your local machine using the command:
```
git clone https://github.com/avarga1/FBS-Scraper.git
```
2. Navigate to the project directory:
```
cd FBS-Scraper
```
3. Install the requirements:
```
pip install beautifulsoup4==4.11.2
pip install requests==2.26.0
```

## Usage
Inside of config.py, you can specify the start and end date for scraping, as well as the currencies you wish to select. the defaults are as follows:
```
START_DATE = "20-08-2022" # Fromat as: DD-MM-YYYY
END_DATE = "20-01-2023" # Format as: DD-MM-YYYY

CURRENCIES = ["CHF", "CAD", "USD", "EUR", "GBP", "JPY", "AUD", "NZD"]
```
You can find more info inside of config.py..


The program can be run from the command line. To start the program, navigate to the project directory and run the command:
```      
python main.py
```
