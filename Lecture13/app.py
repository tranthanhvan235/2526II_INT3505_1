from flask import Flask, render_template, request, jsonify
import uuid
import datetime

app = Flask(__name__)

# Mock database for API keys and analytics
users_db = {}
api_analytics = {
    "total_calls": 0,
    "total_errors": 0,
    "registered_developers": 0
}

@app.route("/")
def home():
    return render_template("index.html", analytics=api_analytics)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
