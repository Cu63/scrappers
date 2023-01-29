from bs4 import BeautifulSoup
import json
import os
import requests
import csv


def get_src_page():
    url = ('http://health-diet.ru/table_calorie/?utm_source=lef'
          'tMenu&utm_medium=table_calorie')

    headers = {
            'Accept' : '*/*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0)'
            ' Gecko/20100101 Firefox/109.0',
        }
    req = requests.get(url, headers=headers)
    src = req.text
    # save page source to file
    with open('index.html', 'w') as f:
        f.write(src)
    return src


def get_categories_dict(domen, soup):
    all_categories = dict()
    # If file exists
    if 'all_categories.json' in os.listdir('.'):
        with open('all_categories.json', 'r') as f:
            all_categories = json.load(f)
        return all_categories

    all_products_hrefs = soup.find_all('a', {'class':
                                             'mzr-tc-group-item-href'}) 
    for item in all_products_hrefs:
        href = f"{domen}{item.get('href')}"
        product = item.text
        all_categories[product] = href

    # save json to file
    with open('all_categories.json', 'w') as f:
        json.dump(all_categories, f, indent=4, ensure_ascii=False)
    return all_categories


def get_products_form_categories(name, url, product_list):
    if f'{name}_products.html' in os.listdir('sources/'):
        with open(f'sources/{name}_products.html') as f:
            src = f.read()
    else:
        rep = ''.maketrans({' ': '_', ',': '_', "'": '_'})
        name = name.translate(rep)
        req =  requests.get(url)
        src = req.text
        with open(f'sources/{name}_products.html', 'w') as f:
            f.write(req.text)

    soup = BeautifulSoup(src, 'lxml')
    all_products = soup.find('tbody')
    for tr in all_products.find_all('tr'):
        try:
            text = tr.text.strip()
            text = text.replace('\n\n', '\n')
            print(text)
            product_name, kkal, prot, fat, carbs = text.split('\n')
            # cat units
            product_name = product_name.lower()
            kkal = kkal.split()[0]
            prot = prot.split()[0]
            fat = fat.split()[0]
            carbs = carbs.split()[0]
            product = (product_name, kkal, prot, fat, carbs)
            product_list.append(product)
        except:
            continue


def main():
    domen = 'https://health-diet.ru'
    # if file not exists - create, else - read
    if 'index.html' not in os.listdir('.'):
        src = get_src_page()
    else:
        with open('index.html', 'r') as f:
            src = f.read()

    soup = BeautifulSoup(src, 'lxml')
    all_categories = get_categories_dict(domen, soup)
    products_list = list()
    for cat_name, cat_href in all_categories.items():
        get_products_form_categories(cat_name, cat_href, products_list)
    products_list = list(sorted(products_list, key=lambda x: x[0]))
    with open('products.csv', 'w') as f:
    # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(('Name', 'Kkal', 'Protein(g)', 'Fat(g)', 'Carbs(g)'))
        write.writerows(products_list)


if __name__ == '__main__':
    main()
