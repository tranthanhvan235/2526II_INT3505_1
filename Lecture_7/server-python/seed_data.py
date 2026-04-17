#!/usr/bin/env python3
"""
Seed sample data to MongoDB for testing
"""

from pymongo import MongoClient
from hashlib import sha256
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'book_management')

def hash_password(password):
    """Hash password"""
    return sha256(password.encode()).hexdigest()

def seed_data():
    """Seed sample data"""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # Clear existing data
    db['users'].delete_many({})
    db['books'].delete_many({})
    db['authors'].delete_many({})
    
    # Insert sample users
    users = [
        {
            'email': 'user@example.com',
            'password': hash_password('password123'),
            'name': 'John Doe'
        },
        {
            'email': 'admin@example.com',
            'password': hash_password('admin123'),
            'name': 'Admin User'
        }
    ]
    db['users'].insert_many(users)
    print("✓ Users seeded")
    
    # Insert sample authors
    authors = [
        {
            'name': 'Author One',
            'bio': 'First author bio'
        },
        {
            'name': 'Author Two',
            'bio': 'Second author bio'
        }
    ]
    authors_result = db['authors'].insert_many(authors)
    print("✓ Authors seeded")
    
    # Insert sample books
    books = [
        {
            'title': 'Book One',
            'description': 'First book description',
            'author_id': str(authors_result.inserted_ids[0]),
            'isbn': '978-0-123456-78-9'
        },
        {
            'title': 'Book Two',
            'description': 'Second book description',
            'author_id': str(authors_result.inserted_ids[1]),
            'isbn': '978-0-987654-32-1'
        }
    ]
    db['books'].insert_many(books)
    print("✓ Books seeded")
    
    client.close()
    print("\nAll data seeded successfully!")

if __name__ == '__main__':
    seed_data()
