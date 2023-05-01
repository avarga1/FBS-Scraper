import pandas as pd
import re
import sys
from config import CURRENCIES


def clean_data(pair):
    # read the CSV file
    df = pd.read_csv(f'./Phase_1_Raw/{pair}_data.csv', encoding='latin1')

    # fill missing values in the "Date" column with the previous non-null value
    df['Date'].fillna(method='ffill', inplace=True)

    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%b %d, %Y %H:%M')

    df.drop(['Date', 'Time'], axis=1, inplace=True)

    df['Datetime'] = pd.to_datetime(df['Datetime']).dt.round('30min')

    df['Datetime'] = df['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    df['Datetime'] = pd.to_datetime(df['Datetime']) - pd.Timedelta(hours=5)

    df.dropna(subset=['Previous', 'Forecast', 'Actual'], how='all', inplace=True)

    df = df[['Datetime', 'Currency', 'Event', 'Previous', 'Forecast', 'Actual']]

    # extract numnber and decimal or hyphen from "Previous", "Forecast", and "Actual" columns
    pattern = r'([-+])?[\d.,]+([%¥€£])?(?<!%)'
    for col in ['Previous', 'Forecast', 'Actual']:
        try:
            df[f'{col}_Value'] = df[col].apply(lambda x: re.search(pattern, str(x)).group(0) if pd.notnull(x) else None)
            df[f'{col}_Value'] = df[f'{col}_Value'].str.replace(',', '').astype(float)
            # make any na values in the "Previous", "Forecast", and "Actual" columns equal to 0
            df[col].fillna(0, inplace=True)
        except:
            print(f"Error in {col}_Value")
            continue
        # if an error occurs, print the row that caused the error
    # drop the "Previous", "Forecast", and "Actual" columns
    df.drop(['Previous', 'Forecast', 'Actual'], axis=1, inplace=True)
    # remove rows where previous, forecast, and actual values are all 0
    df = df[~(df['Previous_Value'] == 0) & ~(df['Forecast_Value'] == 0) & ~(df['Actual_Value'] == 0)]
    # nan to 0
    df.fillna(0, inplace=True)
    # change the Previous, Forecast, and Actual columns to float
    df['Previous_Value'] = df['Previous_Value'].astype(float)
    df['Forecast_Value'] = df['Forecast_Value'].astype(float)
    df['Actual_Value'] = df['Actual_Value'].astype(float)
    # print the first 10 rows of the dataframe
    print(df.head(10))

    # save the cleaned data to a new CSV file
    df.to_csv(f'./Phase_2_Pre-Processed/{pair}_data_x.csv', index=False, float_format='%.4f')
    unique_events = df['Event'].unique()

    print(F'There are {len(unique_events)} unique events in the dataset.')




def main():
    for curr in CURRENCIES:
        clean_data(curr)


if __name__ == '__main__':
    main()