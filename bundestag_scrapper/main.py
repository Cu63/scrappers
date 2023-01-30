from bs4 import BeautifulSoup
from collections import namedtuple
import requests
import os
import json

def get_all_memebers_link():
    f = open('memeber_links.txt', 'w')
    for i in range(0, 740, 20):
        url = (f'https://www.bundestag.de/ajax/filterlist/en/members/'
              f'863330-863330?limit=20&noFilterSet=true&offset={i}')
        req = requests.get(url)
        res = req.content
        soup = BeautifulSoup(res, 'lxml')
        members_hrefs = list()
        for div in soup.find_all('div', {'class': 'bt-slide-content'}):
            href = div.find('a').get('href')
            members_hrefs.append(href)
            f.write(f'{href}\n')
        return members_hrefs


def get_member_info(url):
    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0',
            }
    Person = namedtuple('Person', 'name company media_links')
    req = requests.get(url, headers=headers)
    res = req.content
    soup = BeautifulSoup(res, 'lxml')
    name = soup.find({'class': 'bt-biografie-name'})
    name = name.find('h3').text
    name, company = [s.strip() for s in name.split(',')]
    media_links = list()
    for li in soup.find('ul', {'class': 'bt-linkliste'}).find_all('li'):
        link = li.a.get('href')
        media_links.append(link)
    return Person(name, company, media_links)


if __name__ == "__main__":
    if 'memeber_links.txt' in os.listdir('.'):
        with open('memeber_links.txt') as f:
            members_hrefs = f.readlines()
            members_hrefs = list(map(lambda x: x[:-1], members_hrefs))
    else:
        members_hrefs = get_all_members_link('')

    members_info_list = list()
    for href in members_hrefs:
        try:
            members_info_list.append(get_member_info(href))
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f'error with {href}')
            print(e)
            continue
    with open('members_info.json', 'w') as f:
        json.dump(members_info_list, f, indent=4, ensure_ascii=False)
