from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

try:
    html = urlopen('http://www.pythonscraping.com/pages/page1.html')
except HTTPError as e:
    print(e)
except URLError:
    print("URL not found.")
else:
    print("Done.")

# bs = BeautifulSoup(html.read(), 'html.parser')
# bs = BeautifulSoup(html, 'html.parser')
bs = BeautifulSoup(html, 'lxml')
try:
    badContent = bs.nonExistingTag.anotherTag
except AttributeError as e:
    print('Tag was not found', e)
else:
    if badContent is None:
        print('Tag was not found')
    else:
        print(badContent)

print(bs.h1)
