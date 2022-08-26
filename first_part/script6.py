from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())


def getLinks(url):
    try:
        html = urlopen('http://en.wikipedia.org%s' % (url))
        bs = BeautifulSoup(html, 'lxml')
    except HTTPError as e:
        print(e)

    return bs.find(
            'div', {'id': 'bodyContent'}).find_all(
                    'a', href=re.compile('^(/wiki/)((?!:).)*$'))


url = input("Write the URL: ")
links = getLinks(url)
while (len(links) > 0):
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)
