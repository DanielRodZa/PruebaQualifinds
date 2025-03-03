import requests
import json

def obtener_productos_api(url_api, url_pagina):
    """
    Realiza una solicitud POST a la API para extraer los productos de la página
    """

    try:
        data = {"url": url_pagina}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url_api, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None

def main():
    url_api = "http://localhost:5000/extract_products"
    url_pagina = [
        "https://www.jumbocolombia.com/supermercado/despensa/enlatados-y-conservas",
        "https://www.tiendasjumbo.co/supermercado/despensa/harinas-y-mezclas-para-preparar",
        "https://www.tiendasjumbo.co/supermercado/despensa/bebida-achocolatada-en-polvo"
    ]
    for url in url_pagina:
        productos = obtener_productos_api(url_api, url)

        if productos:
            print(json.dumps(productos, indent=4))
        else:
            print("No se pudieron obtener los productos.")

if __name__ == "__main__":
    main()