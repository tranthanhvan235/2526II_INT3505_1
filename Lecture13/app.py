from flask import Flask, render_template, request, jsonify, redirect, url_for
import uuid
import datetime
import random

app = Flask(__name__)

# Mock database for API keys and analytics
users_db = {}
api_analytics = {
    "total_calls": 0,
    "total_errors": 0,
    "registered_developers": 0
}

# Pricing Plans Configuration
PLANS = {
    "freemium": {"limit": 5, "price_per_call": 0},
    "pay_per_call": {"limit": float('inf'), "price_per_call": 0.05} # $0.05 per call
}

@app.route("/")
def home():
    return render_template("index.html", analytics=api_analytics, users=users_db)

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    plan = request.form.get("plan")
    
    if not username or plan not in PLANS:
        return redirect(url_for('home'))
        
    api_key = str(uuid.uuid4())
    users_db[api_key] = {
        "username": username,
        "plan": plan,
        "calls_made": 0,
        "bill": 0.0,
        "registered_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    api_analytics["registered_developers"] += 1
    
    return render_template("index.html", api_key=api_key, analytics=api_analytics, users=users_db)

@app.route("/api/v1/data", methods=["GET"])
def get_data():
    api_key = request.headers.get("X-API-Key")
    
    if not api_key or api_key not in users_db:
        api_analytics["total_errors"] += 1
        return jsonify({"error": "Unauthorized. Missing or invalid API Key."}), 401
        
    user = users_db[api_key]
    plan_details = PLANS[user["plan"]]
    
    # Check rate limit for freemium
    if user["calls_made"] >= plan_details["limit"]:
        api_analytics["total_errors"] += 1
        return jsonify({"error": "Rate limit exceeded. Please upgrade your plan."}), 429
        
    # Simulate a possible random error
    if random.random() < 0.1: # 10% error rate
        api_analytics["total_errors"] += 1
        return jsonify({"error": "Internal server error"}), 500
        
    # Successful call
    user["calls_made"] += 1
    user["bill"] += plan_details["price_per_call"]
    api_analytics["total_calls"] += 1
    
    return jsonify({
        "data": "Here is your valuable data!",
        "calls_made": user["calls_made"],
        "current_bill": round(user["bill"], 2)
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
