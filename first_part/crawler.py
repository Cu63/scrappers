import requests
from bs4 import BeautifulSoup


class Content:
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print('New arcicle found for topic: {}'.format(self.topic))
        print('Title: {}'.format(self.title))
        print('URL: {}'.format(self.url))
        print(self.body)


class Website:
    def __init__(self, name, url, searchUrl, resultListing,
                 resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resutlUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Crawler:

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join(
                             [elem.get_text() for elem in selectedElems])
        return ''

    def search(self, topic, site):
        bs = self.getPage(site.searchUrl + topic)
        searchResult = bs.select(site.resultListing)
        for result in searchResult:
            url = result.select(site.resultUrl)[0].attrs['href']
            if site.absoluteUrl:
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print('Something was wrong with that page on URL. Skipping!')
                return
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, bodyTag)
            if title != '' and body != '':
                content = Content(topic, title, body, url)


crawler = Crawler()


siteData = [
        ['O\'Reilly Media', 'http://oreilly.com',
         'https://ssearch.oreilly.com/?q=', 'article.product-result',
         'p.title a', True, 'h1', 'section#product-description'],
]

websites = []
for row in siteData:
    websites.append(Website(row[0], row[1], row[2], row[3],
                            row[4], row[5], row[6], row[7]))

topics = ['python', 'data science']
for topic in topics:
    print('Getting info about: ' + topic)
    for targetSite in websites:
        crawler.search(topic, targetSite)
