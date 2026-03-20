from flask import Flask, jsonify, request, abort
from flask_swagger_ui import get_swaggerui_blueprint
import yaml, os

app = Flask(__name__)

yaml_path = os.path.join(os.path.dirname(__file__), 'api/openAPI.yaml')

with open(yaml_path) as f:
    openapi_spec = yaml.safe_load(f)

# In-memory database for demonstration
books = [
    {"id": "BK-2302", "title": "API Design Patterns", "author": "J.J. Geewax", "publishedYear": 2021},
    {"id": "BK-0002", "title": "Clean Code", "author": "Robert C. Martin", "publishedYear": 2008}
]

# 1. GET ALL BOOKS
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# 2. POST NEW BOOK
@app.route('/books', methods=['POST'])
def create_book():
    if not request.json or 'title' not in request.json:
        abort(400)
    
    new_book = {
        "id": f"BK-{len(books) + 1}",
        "title": request.json['title'],
        "author": request.json['author'],
        "publishedYear": request.json.get('publishedYear', 2026)
    }
    books.append(new_book)
    return jsonify(new_book), 201

# 3. GET BOOK BY ID
@app.route('/books/<string:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if book is None:
        abort(404)
    return jsonify(book), 200

# 4. UPDATE BOOK
@app.route('/books/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if book is None:
        abort(404)
    
    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])
    book['publishedYear'] = request.json.get('publishedYear', book['publishedYear'])
    return jsonify(book), 200

# 5. DELETE BOOK
@app.route('/books/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b['id'] != book_id]
    return '', 204


@app.route("/openapi.json")
def openapi_json():
    return jsonify(openapi_spec)

SWAGGER_URL = '/docs'
API_URL = '/openapi.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Book API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, port=8080)