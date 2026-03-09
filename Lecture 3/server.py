from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Van"},
    {"id": 2, "name": "Tung"},
    {"id": 3, "name": "Viet"},
    {"id": 4, "name": "Vinh"}
]

orders = [
    {"id" : 1, "user_id": 1, "product": "lipstick"},
    {"id" : 2, "user_id": 2, "product": "Iphone 17"},
]

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    for u in users:
        if u["id"] == id:
            return jsonify(u)
    return {"message": "User not found"}, 404

@app.route("/orders/<int:id>")
def get_orders(id):
    for u in users:
        if u["id"] == id:
            return jsonify(u)
    return {"message": "User not found"}, 404

if __name__ == "__main__":
    app.run(debug=True, port=3333)