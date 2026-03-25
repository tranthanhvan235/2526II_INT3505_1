from flask import Flask, request, jsonify
from database_setup import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

@app.route('/books', methods=['GET'])
def get_books_offset():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page
    
    books = Book.query.offset(offset).limit(per_page).all()
    return jsonify({
        "current_page": page,
        "data": [{"id": b.id, "title": b.title} for b in books]
    })

if __name__ == '__main__':
    app.run(port=5003)