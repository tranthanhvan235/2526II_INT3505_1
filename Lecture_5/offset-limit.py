from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

@app.route('/books/offset', methods=['GET'])
def get_books_offset():
    limit = request.args.get('limit', 5, type=int)
    offset = request.args.get('offset', 0, type=int)

    query = Book.query
    total_count = query.count()
    books = query.offset(offset).limit(limit).all()

    return jsonify({
        "pagination_type": "Offset-Limit",
        "metadata": {
            "total_records": total_count,
            "limit": limit,
            "offset": offset,
            "next_offset": offset + limit if (offset + limit) < total_count else None
        },
        "data": [{"id": b.id, "title": b.title} for b in books]
    })

if __name__ == '__main__':
    app.run(port=5006, debug=True)