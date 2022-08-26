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

    for link in bs.find('div', {'id': 'bodyContent'}).find_all(
            'a', href=re.compile('^(/wiki/)')):
        if ('href' in link.attrs):
            if link.attrs['href'] not in pages:
                # мы нашли новую страницу
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)


getLinks('')
