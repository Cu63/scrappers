from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
headers = {
        '_ga': 'GA1.2.1575439766.1662835167', 
        '_gat':	'1',
        '_gid':	'GA1.2.854699608.1663004884',
        '_ym_d':	'1662835167',
        '_ym_isad':	'2',
        '_ym_uid':	'1662835167606822212',
        '_ym_visorc':	'w',
        'wordpress_logged_in_95a2ce14874d444647baa643165aaf19':	'otdel89%7C16'
                '64044809%7Cxnn8jVRXFM2v1aQ18IvpGtgi0HgDqfGDsyLAbaJMcBY'
                '%7C3a84b30d69bbdd5ae262d3fd4768f0c'
                '7876c15c77032bc7ca4933fb05ddd1d2f',
        'wordpress_sec_95a2ce14874d444647baa643165aaf19':	'otdel89%7C1664044809%7Cxnn8jVRXFM2v1aQ18IvpGtgi0HgDqfGDsyLAbaJMcBY%7C74edde5ee1f4b4b7ab4c45ca1670f2110878a096499c862fc5b555846950d6ef'}


html = urlopen('https://xakep.ru/issues/xa/278/', headers=headers)
bs = BeautifulSoup(html, 'html.parser')
link =  bs.find('a', {'class': 'download-button'})
print(link)
"""
urlretrieve(imageLocation, 'logo.jpg')
print(imageLocation)
"""
