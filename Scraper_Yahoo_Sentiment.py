from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import pandas as pd
import os
import os.path


def main(ticker, path, pages, filter):
    # create instance of web driver
    web_driver(ticker)
    # choose filter method in drop down list
    select_reaction(filter)
    data = scrape_loop(pages)
    driver.close()
    headers = ['Index', 'Poster', 'Upvote', 'Downvote', 'Sentiment', 'Message']
    date = datetime.now().strftime("%y%m%d")
    directory = date + '_{}.xlsx'.format(ticker)
    try:
        df = pd.DataFrame(data, columns=headers)
        df.to_excel(os.path.join(path, directory))
        print('saved to {}'.format(path))
    except Exception as e:
        print('failed', e)


def select_reaction(filter):
    click_by_text('Top Reactions')
    click_by_text(filter)


def test(element):
    try:
        a = driver.find_elements(By.XPATH, element)[0].text
        return a
    except Exception as e:
        a = ""
        return a


def scrape(post):
    loop = post + 1
    WebDriverWait(driver, 10)
    xpath_posters = '//*[@id="canvass-0-CanvassApplet"]/div/ul/li/div/div[1]/button'
    xpath_upvote = '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div//div[2]/button[1]/span'.format(loop)
    xpath_downvote = '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div//div[2]/button[2]/span'.format(loop)
    xpath_sentment = '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div/div[3]/div/div'.format(loop)
    xpath_message = '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div/div[2]/div'.format(loop)

    poster = driver.find_elements(By.XPATH, xpath_posters)[post].text
    downvote = test(xpath_downvote)
    upvote = test(xpath_upvote)
    sentiment = test(xpath_sentment)
    message = test(xpath_message)
    content = (post, poster, upvote, downvote, sentiment, message)
    return content


def scrape_loop(pages):
    show_more(pages)
    xpath_posts = '//*[@id="canvass-0-CanvassApplet"]/div/ul/li'
    posts = driver.find_elements(By.XPATH, xpath_posts)
    data = []
    for post in range(len(posts)):
        content = scrape(post)
        data.append(content)
    return data


def show_more(pages):
    try:
        for i in range(pages):
            click_by_text('Show more')
            print('Pages:', pages)
    except Exception as e:
        print('page', e)
        pass


def web_driver(ticker):
    global driver
    driver_path = Service('C:/Users/suen6/.wdm/drivers/chromedriver/win32/98.0.4758.80/chromedriver.exe')
    driver = webdriver.Chrome(service=driver_path, options=build_chrome_options())
    driver.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}
    url = 'https://finance.yahoo.com/quote/{}/community?p={}'.format(ticker, ticker)
    response = driver.get(url)
    return response


def click_by_text(text):
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"' + text + '")]')))
        element.click()
    except Exception as e:
        print('click failed', e)


def build_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.accept_untrusted_certs = True
    chrome_options.assume_untrusted_cert_issuer = True
    chrome_options.add_argument("incognito")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1024,800")
    chrome_options.add_argument("disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--test-type=browser")
    chrome_options.add_argument("--disable-impl-side-painting")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-seccomp-filter-sandbox")
    chrome_options.add_argument("--disable-breakpad")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-cast")
    chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
    chrome_options.add_argument("--disable-cloud-import")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-session-crashed-bubble")
    chrome_options.add_argument("--disable-ipv6")
    chrome_options.add_argument("--allow-http-screen-capture")
    return chrome_options


if __name__ == '__main__':
    ticker = 'WISH'
    path = r'C:\Users\suen6\PycharmProjects\Scraper_Yahoo_Finance\data'
    pages = 10
    filter = 'Newest Reactions'
    main(ticker, path, pages, filter)
