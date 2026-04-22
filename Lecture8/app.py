from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

# GET all
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    for u in users:
        if u["id"] == id:
            return jsonify(u), 200
    return jsonify({"error": "User not found"}), 404

# POST
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = {"id": len(users)+1, "name": data["name"]}
    users.append(new_user)
    return jsonify(new_user), 201

# PUT
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    for u in users:
        if u["id"] == id:
            u["name"] = data["name"]
            return jsonify(u), 200
    return jsonify({"error": "User not found"}), 404

# DELETE
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    global users
    users = [u for u in users if u["id"] != id]
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)