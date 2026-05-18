import os
from flask import Flask, jsonify
from models import db
from api.crud import crud_bp

app = Flask(__name__)

# Database Config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register Blueprints
app.register_blueprint(crud_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to Advanced API Design Patterns API"}), 200

def setup_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    setup_db()
    app.run(debug=True, port=5000)
