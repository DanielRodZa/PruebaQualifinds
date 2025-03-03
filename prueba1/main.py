import json
import logging
import requests
import pandas as pd

URL = "https://storage.googleapis.com/resources-prod-shelftia/scrapers-prueba/product.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def obtener_datos_json(url: str) -> dict:
    """
    Obtiene los datos JSON desde una ULR
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error obtienendo los datos de la API: {e}")
        raise
    except json.decoder.JSONDecodeError as e:
        logging.error(f"Error al decodificar la respuesta de la API: {e}")
        raise

def encontrar_custom_attributes(datos_json: dict) -> dict:
    """Encuentra los atributos en los datos del JSON"""
    try:
        return datos_json["allVariants"][0]["attributesRaw"][31]
    except KeyError as e:
        logging.error(f"Error al buscar en el JSON: {e}")
        raise

def formatar_datos(datos_json: dict) -> dict:
    """Dar formato a los datos extraídos del JSON"""
    try:
        values = json.loads(datos_json["value"]["en-CR"])
        allergens = [item["name"] for item in values["allergens"]["value"]]
        return {
            "allergens": allergens,
            "sku": values["sku"]["value"],
            "vegan": values["vegan"]["value"],
            "kosher": values["kosher"]["value"],
            "organic": values["organic"]["value"],
            "vegetarian": values["vegetarian"]["value"],
            "gluten_free": values["gluten_free"]["value"],
            "lactose_free": values["lactose_free"]["value"],
            "package_quantity": values["package_quantity"]["value"],
            "unit_size (g)": values["unit_size"]["value"],
            "net_weight (g)": values["net_weight"]["value"]
        }
    except KeyError as e:
        logging.error(f"Error al buscar en los atributos: {e}")
        raise

def convertir_csv(datos: dict) -> None:
    """Convierte un diccionario en un archivo CSV"""
    if datos:
        df = pd.DataFrame.from_dict(datos)
        df.to_csv("datos_formateados.csv", index=False, encoding="utf-8")
        logging.info("CSV Correctamente guardado")
    else:
        logging.error("No se recibieron datos para guardar en el archivo CSV")

def main():
    try:
        datos_json = obtener_datos_json(URL)
        datos = encontrar_custom_attributes(datos_json)
        datos_formateados = formatar_datos(datos)
        
        if datos_formateados:
            convertir_csv(datos_formateados)
        else:
            logging.error("No se recibiendo datos formateados")

    except Exception as e:
        logging.error(f"Error en la función principal: {e}")

if __name__ == "__main__":
    main()