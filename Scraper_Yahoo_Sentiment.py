from bs4 import BeautifulSoup
import pandas as pd
import re
from requests_html import HTMLSession
import nltk

def main(ticker):
    # extract json data from website
    soup = getsoup(ticker)
    print(soup)

def getsoup(ticker):
    # extract javascript
    soup = BeautifulSoup(geturl(ticker), 'html.parser')
    return soup

def geturl(ticker):
    return 'https://finance.yahoo.com/quote/{}/community?p={}'.format(ticker, ticker)

if __name__ == '__main__':
    ticker = 'WISH'
    main(ticker)