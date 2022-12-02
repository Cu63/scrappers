from bs4 import BeautifulSoup
from urllib.request import urlopen
import base64
import json
import codecs


def get_page(url: str) -> BeautifulSoup:
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    return bs


def get_trends(url: str) -> dict:
    trends = dict()
    bs = get_page(url)
    for li in bs.find('ul',
                     {'class': 'nav__row nav__row_popular-trends'}).find_all('li',
                     {'class': 'nav__row-item nav__row-item_popular-trends'}):
        trend = li.a.text
        trend = trend.strip()
        trend_tag = li.a.attrs['href']
        trends[trend] = trend_tag
    return trends


def get_n_articles_suffix(url: str, n=10) -> list[str]:
    i = 0
    hrefs = list()
    bs = get_page(url)
    for li in bs.find('ul',
                      {'class': 'listing__trend-right__column'}).find_all('li',
                      {'class': 'listing__trend-right__wrapper'}):
        hrefs.append(li.a.attrs['href'])
        i += 1
        if (n == i):
            break
    return hrefs


def get_article_info(url: str) -> dict:
    bs = get_page(url)
    article = dict()

    title = bs.find('h1').text

    description = bs.find('div',
                          {'class': 'article__summary article__summary_article'
                           '-page js-mediator-article'}).text

    content = bs.find('div',
                      {'class': 'article__text'
                       ' article__text_article-page js-mediator-article'})
    content = [str(p) for p in content.find_all('p')]
    content = ''.join(content)
    content = base64.b64encode(bytes(content, 'utf-8')).decode()
# 'adivrticle__cover article__cover_article-page'})
    image = bs.find('img',
                    {'class': 'article__cover-image'})
    if image is not None:
        image = image.attrs['src']
        article['image'] = image

    article['title'] = title
    article['description'] = description
    article['content'] = content
    return article


def main():
    categories = ['world', 'russia', 'ussr', 'business', 'sport', 'science',
                 'nopolitics']

    url = 'https://russian.rt.com'
    json_file = open('news.json', 'w', encoding='utf-8')
    json_file.write('const news = [')

    for cat in categories:
        print(cat)
        cat_url = '%s/%s' % (url, cat)
        trends = get_trends(cat_url)
        for trend in trends:

            print('\t%s' % trend)
            try:
                trend_url = '%s%s' % (url, trends[trend])
                articles_suffix = get_n_articles_suffix(trend_url)
                for suffix in articles_suffix:
                    article_url = '%s%s' % (url, suffix)
                    print('\t\t%s' % article_url)
                    article = get_article_info(article_url)
#                print(article)
                    # article['trends'] = trend
                    json_file.write('\n\t{\n')
                    for key in article:
                        json_file.write('\t\t%s: "%s",\n' % (key, article[key]))
                    json_file.write('\t\ttrends: "%s"\n\t},' % (trend))
            except:
                print(' - unusual page format')
    json_file.write('\r\n]')
    json_file.close()


if __name__ == '__main__':
    main()
