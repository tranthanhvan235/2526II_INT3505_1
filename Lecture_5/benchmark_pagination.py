import time
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///big_data_library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BigBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

# Create 1 million records for benchmarking pagination
def seed_one_million():
    db.drop_all()
    db.create_all()
    print("Creating 1 million records... Please wait about 30s...")
    
    # Insert bulk to speed up the process
    batch_size = 100000
    for i in range(10):
        books = [BigBook(title=f"Book {j + i*batch_size}") for j in range(batch_size)]
        db.session.bulk_save_objects(books)
        db.session.commit()
        print(f"Done { (i+1) * 10 }%...")
    print("Finished creating 1 million records!")

# Endpoint comparing Offset/Limit vs Cursor-based pagination when fetching the "last page" (records 999,991 - 1,000,000)
@app.route('/benchmark', methods=['GET'])
def benchmark():
    # Accessing record at offset 999,990 with limit 10 (records 999,991 - 1,000,000)
    target_offset = 999990
    limit = 10
    
    # Offset/Limit (Page-based)
    start_time = time.perf_counter()
    res_offset = BigBook.query.offset(target_offset).limit(limit).all()
    offset_time = (time.perf_counter() - start_time) * 1000 # (ms)

    # Cursor-based (Keyset)
    # last page end at ID 999,990, so we start from there
    last_id = 999990 
    start_time = time.perf_counter()
    res_cursor = BigBook.query.filter(BigBook.id > last_id).limit(limit).all()
    cursor_time = (time.perf_counter() - start_time) * 1000

    return jsonify({
        "test_at_record": target_offset,
        "offset_limit": {
            "time_ms": round(offset_time, 4),
            "result_count": len(res_offset),
            "status": "need to scan through 999,990 records first"
        },
        "cursor_based": {
            "time_ms": round(cursor_time, 4),
            "result_count": len(res_cursor),
            "status": "Jump straight to ID > 999,990 thanks to Index"
        },
        "conclusion": f"Cursor is faster than Offset by approximately {round(offset_time / cursor_time, 1)} times!"
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        print("Checking data...")
        count = BigBook.query.count()
        
        if count < 1000000:
            seed_one_million()
        else:
            print(f"{count} records. Ready for benchmark!")
            
    app.run(port=5005, debug=True)