import requests
from bs4 import BeautifulSoup
import json
import random
import time
import os

def get_url(url):
    headers = {
        'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    }
    request = requests.get(url, headers)

    with open('project.html', 'w+') as file:
        file.write(request.text)
    
    with open('project.html', 'r') as file:
        src = file.read()
    
    os.mkdir('data')
    
    soup = BeautifulSoup(src, 'lxml')

    products = soup.find_all('div', class_='product__title-block')

    product_urls = []
    data_out = []

    for product in products:
        productUrl = 'https://tvoe.ru' + product.find('component', class_='product__title').get('link')
        product_urls.append(productUrl)

    step_to_out = len(product_urls)
    
    for product_url in product_urls:
        product_name = f'{product_url.split('/')[-2]}.html'
        req = requests.get(product_url, headers)

        with open(f'data\\{product_name}', 'w+') as file:
            file.write(req.text)

        with open(f'data\\{product_name}', 'r') as file:
            src = file.read()
        
        soup_urls = BeautifulSoup(src, 'lxml')

        try:
            logo = soup_urls.find('img', class_='product-detail__image').get('src')
        except Exception:
            logo = 'no things'
        try:
            name = soup_urls.find('h1', class_='product-detail__title').text
        except Exception:
            logo = 'no things'
        try:
            price = soup_urls.find('span', class_='product-detail__price product-detail__price--discount').text
        except Exception:
            logo = 'no things'

        data = {
            'название товара': name,
            'фотография': logo,
            'цена товара': price,
            'ссылка на товар': product_url
        }
        data_out.append(data)

        step_to_out -= 1
        if step_to_out == 0:
            print('Программа завершена!')
        else:
            print(f'Теперь осталось загрузить файлов: #{step_to_out}')

        time.sleep(random.randrange(2,4))

    with open('data_out.json', 'a', encoding='utf-8') as file:
        json.dump(data_out, file, indent=4, ensure_ascii=False)
    

get_url('https://tvoe.ru/catalog/new/?ysclid=lpsvm5a4s8554434040')
