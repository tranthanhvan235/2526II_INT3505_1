from app import app, db, Book, Author, User, Loan

with app.app_context():
    db.drop_all()
    db.create_all()
    
    a1 = Author(name="J.K. Rowling")
    u1 = User(name="Van Van")
    db.session.add_all([a1, u1])
    db.session.commit()

    for i in range(1, 21):
        b = Book(title=f"Harry Potter Vol {i}", category="Magic", author_id=a1.id)
        db.session.add(b)
    
    l1 = Loan(book_id=1, user_id=u1.id)
    db.session.add(l1)
    
    db.session.commit()
    print("Seed data created!")