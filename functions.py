import requests
from bs4 import BeautifulSoup
import csv

def scrapBaseUrl(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'lxml')