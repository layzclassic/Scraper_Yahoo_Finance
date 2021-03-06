import re
import json
from bs4 import BeautifulSoup
import pandas as pd
#fetch the Javascript content
from requests_html import HTMLSession
from datetime import datetime
import os
import numpy

def main(ticker, tab):
    # extract json data from website
    json_data = getsoup(ticker, tab)
    # select account to extract
    selected_acc = extract_raw_data(json_data)
    # filter raw data
    filtered_data = extract_acc_list(selected_acc)
    # create datdframe and add date as index
    df = create_dataframe(filtered_data)
    # save csv
    try:
        # check if there is an existing file
        if not os.path.isfile('{}.csv'.format(ticker)):
            df.to_csv('{}.csv'.format(ticker), index=False)
            os.system('{}.csv'.format(ticker))
        # check if existing file already has the data for the particular year f.index ==
        elif os.path.isfile('{}.csv'.format(ticker)):
            reader = pd.read_csv('{}.csv'.format(ticker))
            if datetime.now().year in reader.date.values:
                print('The existing csv already has the data for {}'.format(datetime.now().year))
            else:
                # append to existing file
                reader.dropna(how="all", inplace=True)
                reader.drop_duplicates().to_csv('{}.csv'.format(ticker), mode='a', index=False, header=False, line_terminator='\n\r')
                os.system('{}.csv'.format(ticker))
        else:
            print('error')
    except:
        print('unable to do shit')


def geturl(ticker, tab):
    return 'https://finance.yahoo.com/quote/{}/{}?p={}'.format(ticker, tab, ticker)

# add date column and remove index
def create_dataframe(data):
    df = pd.DataFrame(data)
    date = datetime.now().year
    df.insert(0, 'date', date)
    return df
    """
    # set date as index
    df = pd.DataFrame(data)
    date = datetime.now().year
    df['date'] = date
    df.set_index('date' , inplace=True)
    return df
    """

def delete_empty_rows(file_path, new_file_path):
    data = pd.read_csv(file_path, skip_blank_lines=True)
    data.dropna(how="all", inplace=True)
    data.to_csv(new_file_path, header=True)


def clean_data(df):
    df = df.set_index(0)

def getsoup(ticker, tab):
    session = HTMLSession()
    response = session.get(geturl(ticker, tab))
    soup = BeautifulSoup(response.text, 'html.parser')
    # extract json formatted strings
    pattern = re.compile(r'\s--\sData\s--\s')
    script_data = soup.find('script', text=pattern).contents[0]
    # find the starting position of the json string through 'context'
    start = script_data.find("context") - 2
    # slice the json string / removing the javascript syntax
    json_data = json.loads(script_data[start:-12])
    return json_data


def extract_raw_data(json_data):
    # income statement
    annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
    quarterly_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']['incomeStatementHistory']

    # cash flow statement
    annual_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
    quarterly_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']

    # balance sheet
    annual_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
    quarterly_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']

    selected_acc = annual_cf
    # select which account user wants to extract
    return selected_acc

def extract_acc_list(selected_acc):
    # consolidate data
    filtered_data = []
    for s in selected_acc:
        statement = {}
    for key, val in s.items():
        try:
        # 3 formats - 'raw', 'fmt', 'longFmt'
            statement[key] = val['fmt']
        # some accounts do not contain data nor dictionary
        except TypeError:
            continue
        except KeyError:
            continue
    filtered_data.append(statement)
    return filtered_data

if __name__ == '__main__':
    ticker = 'WISH'
    tab = 'financials'

    main(ticker, tab)
