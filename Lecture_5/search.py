# demo2_search.py
from flask import Flask, request, jsonify
from database_setup import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

@app.route('/books', methods=['GET'])
def search_books():
    keyword = request.args.get('q', '') 
    books = Book.query.filter(Book.title.contains(keyword)).all()
    return jsonify([{"id": b.id, "title": b.title} for b in books])

if __name__ == '__main__':
    app.run(port=5002)