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

@app.route("/users", methods=["POST"])
def create_user():

    data = request.json

    new_user = {
        "id": len(users) + 1,
        "name": data["name"]
    }

    users.append(new_user)

    return jsonify(new_user)

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

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    global users

    users = [u for u in users if u["id"] != user_id]

    return jsonify({"message": "deleted"})


@app.route("/users/<int:user_id>/orders", methods=["GET"])
def get_user_orders(user_id):

    user_orders = [o for o in orders if o["user_id"] == user_id]

    return jsonify(user_orders)

if __name__ == "__main__":
    app.run(debug=True, port=3005)