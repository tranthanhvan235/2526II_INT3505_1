from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Cấu hình MongoDB
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'book_management')

# Instance toàn cục của MongoDB client và database
client = None
db = None
connected = False

def init_db():
    """Khởi tạo kết nối MongoDB (lazy connection)"""
    global client, db, connected
    if connected:
        return db
    
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
        # Test kết nối
        client.admin.command('ping')
        db = client[DB_NAME]
        connected = True
        print(f"✓ Connected to MongoDB: {DB_NAME}")
        return db
    except Exception as e:
        print(f"⚠ MongoDB connection warning: {e}")
        print("⚠ Server running in demo mode (without database)")
        db = None
        connected = False
        return None

def get_db():
    """Lấy instance của database (khởi tạo kết nối nếu cần)"""
    global db, connected
    if db is None and not connected:
        init_db()
    return db

def is_connected():
    """Kiểm tra xem có kết nối MongoDB không"""
    global connected
    return connected

def close_db():
    """Đóng kết nối MongoDB"""
    global client, connected
    if client:
        try:
            client.close()
            print("✓ MongoDB connection closed")
        except:
            pass
        finally:
            connected = False
