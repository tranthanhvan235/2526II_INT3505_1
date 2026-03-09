from flask import Flask, jsonify, request

app = Flask(__name__)


users = [
    {"id": 1, "name": "Van"},
    {"id": 2, "name": "Tung"},
    {"id": 3, "name": "Vinh"}
]

items = [
    {"id": 1, "items": "lipstick"},
    {"id": 2, "items": "snack"},
    {"id": 3, "items": "iphone17"}
]
user_items = [
    {"user_id": 1, "item_id": 1},
    {"user_id": 1, "item_id": 3},
    {"user_id": 2, "item_id": 2},
]

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    users.append(data)
    return {"message": "User added", "data": data}

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    for u in users:
        if u["id"] == id:
            return jsonify(u)
    return {"message": "User not found"}, 404

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    for u in users:
        if u["id"] == id:
            u["name"] = data["name"]
    return {"message":"updated"}

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    global users
    users = [u for u in users if u["id"] != id]
    return {"message":"deleted"}

@app.route("/users/<int:user_id>/items", methods=["GET"])
def get_user_items(user_id):
    user = None
    for u in users:
        if u["id"] == user_id:
            user = u
            break

    if not user:
        return {"message": "User not found"}, 404

    owned_items = []

    for ui in user_items:
        if ui["user_id"] == user_id:
            for item in items:
                if item["id"] == ui["item_id"]:
                    owned_items.append(item)
    
    return jsonify({
        "user": user,
        "items": owned_items
    })   

if __name__ == "__main__":
    app.run(debug=True, port=2305)