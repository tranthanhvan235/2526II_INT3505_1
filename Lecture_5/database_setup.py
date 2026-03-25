from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    loans = db.relationship('Loan', backref='user')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.drop_all()
    db.create_all()
    u1 = User(name="Tran Thi Thanh Van")
    db.session.add(u1)
    for i in range(1, 21):
        db.session.add(Book(title=f"Data Modeling {i}"))
    db.session.add(Loan(book_id=1, user_id=1))
    db.session.add(Loan(book_id=2, user_id=1))
    db.session.commit()
    print("Database ready!")