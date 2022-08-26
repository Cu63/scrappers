from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError

try:
    html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
    bs = BeautifulSoup(html.read(), 'lxml')
    nameList = bs.find_all('span', {'class': 'green'})
except HTTPError as e:
    print(e)

for name in nameList:
    print(name.get_text())
