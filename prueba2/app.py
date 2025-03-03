from flask import Flask, request, jsonify
import utils

app = Flask(__name__)

@app.route('/extract_products', methods=['POST'])
def extract_products():
    """
    Extrae los primeros 15 productos de una URL (POST)
    :return:
        JSON con la lista de productos
    """
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No se encontrado'}), 400

    url = data['url']
    html_text = utils.obtener_html(url)
    if not html_text:
        return jsonify({'error': 'No se pudo obtener el HTML'}), 400

    products = utils.extract_products(html_text)

    response = {
        "url": url,
        "products": products[0:15]
    }
    print(response)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')