# demo5_page_based.py
from flask import Flask, request, jsonify
from database_setup import db, Book
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

@app.route('/books/page-based', methods=['GET'])
def get_books_page_based():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('size', 5, type=int)

    # offset = (page - 1) * page_size
    offset = (page - 1) * page_size

    query = Book.query
    total_items = query.count() 
    books = query.offset(offset).limit(page_size).all()

    total_pages = math.ceil(total_items / page_size)
    has_next = page < total_pages
    has_prev = page > 1

    return jsonify({
        "pagination": {
            "current_page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev
        },
        "data": [{"id": b.id, "title": b.title} for b in books]
    })

if __name__ == '__main__':
    app.run(port=5005)