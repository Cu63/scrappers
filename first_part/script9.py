from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random


pages = set()
random.seed(datetime.datetime.now())
allExtLinks = set()
allIntLinks = set()


# get list of local links on site
def getInternalLinks(bs, includeUrl):
    includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme,
                                  urlparse(includeUrl).netloc)
    interalLinks = []
    for link in bs.find_all(
            'a', href=re.compile('^(/|.*'+includeUrl+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in interalLinks:
                if (link.attrs['href'].startswith('/')):
                    interalLinks.append(includeUrl+link.attrs['href'])
                else:
                    interalLinks.append(link.attrs['href'])
    return interalLinks


def getExternalLinks(bs, excludeUrl):
    externalLinks = []
# find all links, which begins with 'http' or 'www' and not include excludeUrl
    for link in bs.find_all(
            'a', href=re.compile('^(http|www)((?!' + excludeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bs = BeautifulSoup(html, 'html.parser')
    externalLinks = getExternalLinks(bs, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print('No external links, looking arount the site for one')
        domain = '{}://{}'.format(urlparse(startingPage).scheme,
                                  urlparse(startingPage).netloc)
        interalLinks = getInternalLinks(bs, domain)
        return getRandomExternalLink(interalLinks[random.randint(0,
                                     len(interalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print('Random external link is: {}'.format(externalLink))
    followExternalOnly(externalLink)


def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    domain = '{}://{}'.format(urlparse(siteUrl).scheme,
                              urlparse(siteUrl).netloc)
    bs = BeautifulSoup(html, 'html.parser')
    internalLinks = getInternalLinks(bs, domain)
    externalLinks = getExternalLinks(bs, domain)

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)

    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            getAllExternalLinks(link)


def main():
    # followExternalOnly('http://oreilly.com')
    allIntLinks.add('http://oreilly.com')
    getAllExternalLinks('http://oreilly.com')


if __name__ == '__main__':
    main()
