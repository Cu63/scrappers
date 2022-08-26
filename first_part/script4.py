from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen('http://www.pythonscraping.com/pages/page3.html')
    bs = BeautifulSoup(html, 'lxml')
except HTTPError as e:
    print(e)

for sibling in bs.find('table', {'id': "giftList"}).tr.next_siblings:
    print(sibling)
