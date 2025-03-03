# Prueba Técnica - Extracción y API de Productos
## Por Daniel Rodriguez Zavaleta

Este repositorio contiene la solución a la prueba técnica de selección de personal, que consta de dos partes principales:

1.  **Extracción de Propiedades de JSON a CSV**: Un script en Python que procesa un archivo JSON para extraer y formatear propiedades específicas en un archivo CSV.
2.  **API de Extracción de Productos**: Una API en Python que recibe una URL y extrae los primeros 15 productos, junto con un `Dockerfile` para su contenedorización.

## Parte 1: Extracción de Propiedades de JSON a CSV

### Descripción

Este script en Python toma un archivo JSON como entrada y extrae las siguientes propiedades del nodo "custom\_attributes":

* allergens
* sku
* vegan
* kosher
* organic
* vegetarian
* gluten\_free
* lactose\_free
* package\_quantity
* unit\_size
* net\_weight

La salida se genera en un archivo CSV formateado, facilitando la lectura y el análisis de los datos.

**Nota:** Se ha ajustado el formato de salida a CSV para mejorar la visualización y el manejo de los datos, ya que el formato de ejemplo proporcionado no fué posible visualizarlo con la URL proporcionada.


### Requisitos

* Python 3.x
* Librerías `requests` y `pandas`

### Instalación

1.  Clona el repositorio:

    ```bash
    git clone [https://github.com/DanielRodZa/PruebaQualifinds.git](https://github.com/DanielRodZa/PruebaQualifinds.git)
    ```

2. Instala las dependencias:

    ```bash
    pip install requests pandas
    ```

### Uso

1.  Ejecuta el script:

    ```bash
    python extraer_json_a_csv.py
    ```

    El script obtendrá los datos de la URL predefinida y generará el archivo `datos_formateados.csv` en el mismo directorio.


### Estructura del Script

* `obtener_datos_json(url: str) -> dict`: Obtiene los datos JSON desde una URL.
* `encontrar_custom_attributes(datos_json: dict) -> dict`: Encuentra los atributos en los datos del JSON.
* `formatar_datos(datos_json: dict) -> dict`: Da formato a los datos extraídos del JSON.
* `convertir_csv(datos: dict) -> None`: Convierte un diccionario en un archivo CSV.
* `main()`: Función principal que ejecuta el proceso completo.

### Consideraciones Adicionales

* El script incluye manejo de errores con `logging` para facilitar la depuración.
* Se utiliza `requests` para obtener los datos JSON desde la URL y `pandas` para convertir los datos en un archivo CSV.
* El archivo `datos_formateados.csv` se genera automáticamente al ejecutar el script.

## Parte 2: API de Extracción de Productos

### Descripción

Esta API en Python (`app.py`) proporciona un servicio para extraer los primeros 15 productos de una URL dada. Utiliza el método POST para recibir la URL como parámetro de entrada. La extracción de los productos se realiza mediante web scraping utilizando Selenium y BeautifulSoup.

### Requisitos

* Python 3.x
* Librerías `Flask`, `requests`, `BeautifulSoup4`, `Selenium` y `webdriver-manager`
* WebDriver para Selenium (por ejemplo, ChromeDriver)
* Docker (opcional, para la contenedorización)

### Instalación

1. Instala las dependencias:

    ```bash
    pip install Flask requests beautifulsoup4 selenium webdriver-manager
    ```

### Uso

1.  Ejecuta la API:

    ```bash
    python app.py
    ```

2.  Utiliza el script `get_api_response.py` para probar la API

    ```bash
    python get_api_response.py
    ```

### Estructura del Código

* **`app.py`**:
    * Define la API Flask con una ruta `/extract_products` que recibe una URL por POST.
    * Utiliza funciones de `utils.py` para obtener el HTML y extraer los productos.
    * Devuelve un JSON con los resultados.
* **`utils.py`**:
    * `obtener_html(url: str)`: Utiliza Selenium para obtener el HTML de la página, realizando scroll para cargar todos los productos.
    * `extract_products(html: str)`: Utiliza BeautifulSoup para parsear el HTML y extraer los nombres, precios y precios de promoción de los productos.
* **`get_api_response.py`**:
    * Script para probar la API enviando peticiones POST con URLs de prueba.

### Consideraciones Adicionales

* El script `utils.py` guarda el HTML obtenido en un archivo local para evitar consultas repetidas y posibles bloqueos.
* Se utiliza Selenium para simular el scroll y asegurar que todos los productos se carguen antes de extraer la información.
* Asegúrate de que el WebDriver sea compatible con tu navegador y esté correctamente configurado.