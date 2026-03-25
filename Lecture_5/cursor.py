# demo4_cursor.py
from flask import Flask, request, jsonify
from database_setup import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

@app.route('/books/cursor', methods=['GET'])
def get_books_cursor():
    after_id = request.args.get('after_id', 0, type=int)
    limit = 5
    
    books = Book.query.filter(Book.id > after_id).limit(limit).all()
    next_cursor = books[-1].id if books else None
    
    return jsonify({
        "data": [{"id": b.id, "title": b.title} for b in books],
        "next_cursor": next_cursor
    })

if __name__ == '__main__':
    app.run(port=5004)