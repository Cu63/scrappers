from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import datetime
import random
import re


random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen(f'http://en.wikipedia.org{articleUrl}')
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find('div', {'id': 'bodyContent'}).find_all('a',
                   href=re.compile('^(/wiki/)((?!:).)*$'))


def getHistoryIPs(pageUrl):
    pageUrl = pageUrl.replace('/wiki/', '')
    historyUrl = ('http://en.wikipedia.org/w/index.php'
                 '?title={}&action=history'.format(pageUrl))
    print('history url is: {}'.format(historyUrl))
    html = urlopen(historyUrl)
    bs = BeautifulSoup(html, 'html.parser')
    ipAddresses = bs.find_all('a', {'class': 'mw-anonuserlink'})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
    return addressList


def getContry(ipAddress):
    try:
        response = urlopen(
                f'http://ip-api.com/json/{ipAddress}').read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get('countryCode')

links = getLinks('/wiki/Python_(programming_language)')

while len(links) > 0:
    for link in links:
        print('-'*20)
        historyIPs = getHistoryIPs(link.attrs['href'])
        for historyIP in historyIPs:
            country = getContry(historyIP)
            if country is not None:
                print('%s is from %s' % (historyIP, country))

    newLink = links[random.randint(0, len(links)-1)].attrs['href']
    links = getLinks(newLink)
