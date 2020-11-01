import requests
import os
from bs4 import BeautifulSoup
import codecs

def getAbsolutePath(relative_path):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_path = os.path.join(script_dir, relative_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    return abs_path

def scrapBaseUrl(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'lxml')