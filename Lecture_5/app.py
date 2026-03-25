from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    books = db.relationship('Book', backref='author', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    loans = db.relationship('Loan', backref='user', lazy=True)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='borrowed') # borrowed, returned

@app.route('/users/<int:user_id>/loans', methods=['GET'])
def get_user_loans(user_id):
    user = User.query.get_or_404(user_id)
    loans = Loan.query.filter_by(user_id=user_id).all()
    return jsonify({
        "user_name": user.name,
        "loans": [{"loan_id": l.id, "book_id": l.book_id, "status": l.status} for l in loans]
    })

@app.route('/books', methods=['GET'])
def get_books_offset():
    # Search
    search = request.args.get('q', '')
    # Pagination params
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    query = Book.query.filter(Book.title.contains(search))
    total = query.count()
    
    # Offset/Limit
    books = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return jsonify({
        "type": "Offset/Limit Pagination",
        "total_records": total,
        "current_page": page,
        "data": [{"id": b.id, "title": b.title, "category": b.category} for b in books]
    })

@app.route('/books/cursor', methods=['GET'])
def get_books_cursor():
    limit = request.args.get('limit', 5, type=int)
    after_id = request.args.get('after_id', 0, type=int) 

    books = Book.query.filter(Book.id > after_id).limit(limit).all()
    
    next_cursor = books[-1].id if books else None
    
    return jsonify({
        "type": "Cursor-based Pagination",
        "next_cursor": next_cursor,
        "has_more": len(books) == limit,
        "data": [{"id": b.id, "title": b.title} for b in books]
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)