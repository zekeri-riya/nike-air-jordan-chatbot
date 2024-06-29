import requests
from bs4 import BeautifulSoup

def get_product_info(catalog_url):
    response = requests.get(catalog_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch product catalog")
    
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    for product in soup.find_all('div', class_='product-card'):
        name = product.find('div', class_='product-card__title').text.strip()
        description = product.find('div', class_='product-card__subtitle').text.strip()
        price = product.find('div', class_='product-price').text.strip()
        image_tag = product.find('img', class_='product-card__img')
        image_url = image_tag['src'] if image_tag else None
        
        products.append({
            "name": name,
            "description": description,
            "price": price,
            "image_url": image_url
        })
    return products
