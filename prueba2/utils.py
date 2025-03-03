import random
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def obtener_html(url: str):

    filename = f"html_cache_{url.replace('/','_').replace(':','_')}.html"

    if os.path.exists(filename):
        print(f"File {filename} exists, using cache...")
        with open(filename,'r', encoding="utf-8") as f:
            return f.read()

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "vtex-flex-layout-0-x-flexRow"))
        )
        time.sleep(random.randint(3 ,5))
        # Iniciar scroll abajo
        ultimo_alto = driver.execute_script("return document.body.scrollHeight")
        posicion_actual = 0
        incremento = 200

        while posicion_actual < ultimo_alto:
            posicion_siguiente = min(posicion_actual + incremento, ultimo_alto)
            driver.execute_script(f"window.scrollTo(0, {posicion_siguiente});")
            posicion_actual = posicion_siguiente
            time.sleep(0.5)

        html = driver.page_source

        # Guardar en HTML para evitar consultas repetidas y posibles bloqueos
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML Obtenido: {filename}")

        return html
    except Exception as e:
        print(e)
        return None
    finally:
        driver.close()

def extract_products(html: str):
    """
    Extrae los primeros 15 productos de una URL
    :return:
        JSON con la lista de productos
    """
    soup = BeautifulSoup(html, 'html.parser')
    main_productos = soup.find('div', attrs={'id': 'gallery-layout-container'})
    productos = main_productos.find_all('article')
    productos_lista = []
    for producto in productos:
        name = producto.find('span', attrs={'class': 'vtex-product-summary-2-x-productBrand'}).text

        prices_raw = producto.find('div', attrs={'class':'vtex-product-price-1-x-priceSuspenseContentWrapper'})
        prices = prices_raw.find_all('div', attrs={'class': 'tiendasjumboqaio-jumbo-minicart-2-x-pp_container'})
        prices_list = []
        for price in prices:
            prices_list.append(price.text.replace('\u00a0', ' '))

        if len(prices_list) >= 2:
            product_dict = {
                'name': name,
                'price': prices_list[0],
                'promo_price': prices_list[1]
            }
        else:
            product_dict = {
                'name': name,
                'price': prices_list[0],
                'promo_price': prices_list[0]
            }
        productos_lista.append(product_dict)

    return productos_lista


urls = [
    "https://www.jumbocolombia.com/supermercado/despensa/enlatados-y-conservas",
    "https://www.tiendasjumbo.co/supermercado/despensa/harinas-y-mezclas-para-preparar",
    "https://www.tiendasjumbo.co/supermercado/despensa/bebida-achocolatada-en-polvo"
]

def main():
    for url in urls:
        html_url = obtener_html(url)
        products_list = extract_products(html_url)
        for product in products_list:
            print(product)

if __name__ == '__main__':
    main()