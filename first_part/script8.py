from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re


pages = set()


def getLinks(url):
    global pages
    try:
        html = urlopen('http://en.wikipedia.org%s' % (url))
        bs = BeautifulSoup(html, 'lxml')
    except HTTPError as e:
        print(e)
    except AttributeError as e:
        print(e)

    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').find_all('p')[0])
        print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('This page is missing something! Continuing.')

    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if ('href' in link.attrs):
            if (link.attrs['href'] not in pages):
                newLink = link.attrs['href']
                print('-'*20)
                print(newLink)
                pages.add(newLink)
                getLinks(newLink)


getLinks('')
