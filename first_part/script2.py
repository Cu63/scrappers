from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError


def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    try:
        bs = BeautifulSoup(html, 'lxml')
        title = bs.body.h1
    except AttributeError as e:
        print(e)
        return None
    return title


# title = getTitle('http://www.pythonscraping.com/pages/page1.html')
url = input("Enter url:")
title = getTitle(url)
if (title is None):
    print("Title was not found.")
else:
    print(title)
