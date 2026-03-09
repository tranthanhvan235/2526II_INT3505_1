from flask import Flask, jsonify, request, make_response

app = Flask(__name__)


users = [
    {"id": 1, "name": "Van"},
    {"id": 2, "name": "Tung"},
    {"id": 3, "name": "Vinh"}
]

@app.route("/users", methods=["GET"])
def get_users():
    response = make_response(jsonify(users))

    response.headers["Cache-Control"] = "public, max-age=60"
    return response


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

@app.route("/profile", methods=["GET"])
def get_profile():
    user_id = request.args.get("user_id")

    if not user_id:
        return {"message": "Missing user_id"}, 400

    user_id = int(user_id)

    for u in users:
        if u["id"] == user_id:
            return jsonify(u)
        
    return {"message": "User not found"}, 404

if __name__ == "__main__":
    app.run(debug=True, port=3333)