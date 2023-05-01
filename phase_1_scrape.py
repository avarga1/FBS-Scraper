import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
from config import START_DATE, END_DATE
from config import CURRENCIES
from multiprocessing import Pool, cpu_count

def extract_data(pair, start_date, end_date):
    url = f"https://fbs.com/analytics/calendar/currency?calendarPeriod={start_date}%2C{end_date}&CurrenciesSearch%5Bcurrencies%5D%5B%5D={pair.lower()}&CurrenciesSearch%5Bimpacts%5D%5B%5D=3&CurrenciesSearch%5Bimpacts%5D%5B%5D=2"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    date_element = None
    elements = soup.find_all(class_='e-calendar__holder')
    rows = []

    for element in elements:
        if element.has_attr('data-date'):
            date_element = element
        else:
            # Extract the required data from each element
            time_impact = element.find(class_='e-calendar__time')
            if time_impact:
                time_impact = time_impact.get_text().strip()
            else:
                time_impact = ""

            currency = element.find(class_='e-calendar__country')
            if currency:
                currency = currency.get_text().strip()
            else:
                currency = ""

            cells = element.find_all(class_='e-calendar__cell')
            if len(cells) > 2:
                event = cells[2].get_text().strip()
            else:
                event = ""

            if len(cells) > 3:
                previous = cells[3].find(class_='e-calendar__txt')
                if previous:
                    previous = previous.get_text().strip()
                else:
                    previous = ""
            else:
                previous = ""

            if len(cells) > 4:
                forecast = cells[4].find(class_='e-calendar__txt')
                if forecast:
                    forecast = forecast.get_text().strip()
                else:
                    forecast = ""
            else:
                forecast = ""

            if len(cells) > 5:
                actual = cells[5].find(class_='e-calendar__txt')
                if actual:
                    actual = actual.get_text().strip()
                else:
                    actual = ""
            else:
                actual = ""

  
            if date_element:
                date = date_element.get_text().strip()
            else:
                date = ""
            rows.append([date, time_impact, currency, event, previous, forecast, actual])
            date_element = None


    with open(f"./Phase_1_Raw/{pair}_data.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def extract_data_for_currency(curr):

    start_date = datetime.strptime(START_DATE, '%d-%m-%Y')
    end_date = datetime.strptime(END_DATE, '%d-%m-%Y')

    with open(f"./Phase_1_Raw/{curr}_data.csv", mode='w', newline='') as file:
        
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Currency", "Event", "Previous", "Forecast", "Actual"])
        while start_date <= end_date:

            extract_data(curr, start_date.strftime('%d-%m-%Y'), start_date.strftime('%d-%m-%Y'))
            start_date += timedelta(days=1)

if __name__ == '__main__':
    # Create a pool of workers equal to the number of CPUs
    pool = Pool(cpu_count())
    # Extract the data for each currency in the list
    pool.map(extract_data_for_currency, CURRENCIES)
    # Close the pool
    pool.close()
    # Join the processes
    pool.join()
