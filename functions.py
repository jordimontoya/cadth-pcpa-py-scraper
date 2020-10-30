import requests
from bs4 import BeautifulSoup

def scrapBaseUrl(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'lxml')