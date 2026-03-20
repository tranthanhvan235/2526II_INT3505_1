from flask import Flask, jsonify, request, abort
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# In-memory database for demonstration
books = [
    {"id": "BK-2302", "title": "API Design Patterns", "author": "J.J. Geewax", "publishedYear": 2021},
    {"id": "BK-0002", "title": "Clean Code", "author": "Robert C. Martin", "publishedYear": 2008}
]

def handler(request, context):
    return app(request.environ, lambda *args: None)
    
# 1. GET ALL BOOKS
@app.route('/books', methods=['GET'])
def get_books():
    """
    List all books
    ---
    responses:
      200:
        description: A list of books
    """
    return jsonify(books), 200

# 2. POST NEW BOOK
@app.route('/books', methods=['POST'])
def create_book():
    """
    Create a new book
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Book
          required:
            - title
            - author
          properties:
            title:
              type: string
            author:
              type: string
            publishedYear:
              type: integer
    responses:
      201:
        description: Book created successfully
    """
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
    """
    Get book details by ID
    ---
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Book found
      404:
        description: Book not found
    """
    book = next((b for b in books if b['id'] == book_id), None)
    if book is None:
        abort(404)
    return jsonify(book), 200

# 4. UPDATE BOOK
@app.route('/books/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Update an existing book
    ---
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Book'
    responses:
      200:
        description: Book updated
    """
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
    """
    Remove a book from the library
    ---
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
    responses:
      204:
        description: Book deleted
    """
    global books
    books = [b for b in books if b['id'] != book_id]
    return '', 204


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Book API"})

if __name__ == '__main__':
    app.run(debug=True, port=8080)