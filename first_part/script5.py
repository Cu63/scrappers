from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

try:
    html = urlopen('http://www.pythonscraping.com/pages/page3.html')
    bs = BeautifulSoup(html, 'lxml')
    images = bs.find_all(
            'img', {'src': re.compile('..//img//gifts//img.*.jpg')})
except HTTPError as e:
    print(e)

for image in images:
    print(image['src'])
