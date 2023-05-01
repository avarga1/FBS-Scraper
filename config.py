# This file contains all the configuration variables for the program

"""
Legend

    START_DATE: The start date for the data to be scraped- Earliest available start: April 1, 2019

    END_DATE: The end date for the data to be scraped
    
    PAIRS: The currency pairs to be scraped (Must be in the following list and inside quotation marks)
        Options: 
          SGD, TRY, CAD, CHF, CNY, MXN, AUD,
          EUR, JPY, BRL, NZD, USD, ZAR, GBP

"""


START_DATE = "01-01-2023" # Fromat as: DD-MM-YYYY
END_DATE = "20-01-2023" # Format as: DD-MM-YYYY

CURRENCIES = ["CHF", "CAD", "USD", "EUR", "GBP", "JPY", "AUD", "NZD"]
