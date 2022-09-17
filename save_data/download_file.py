from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup


html = urlopen('https://pythonscraping.com')
bs = BeautifulSoup(html, 'html.parser')
#imageLocation = bs.find('a', {'id': 'logo'}).find('img')['src']
imageLocation = bs.find('img')['src']
urlretrieve(imageLocation, 'logo.jpg')
print(imageLocation)
