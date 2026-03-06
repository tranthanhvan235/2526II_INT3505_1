from flask import Flask, jsonify, request

app = Flask(__name__)


users = [
    {"id": 1, "name": "Van"},
    {"id": 2, "name": "Tung"},
    {"id": 3, "name": "Vinh"}
]

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    users.append(data)
    return {"message": "User added", "data": data}

if __name__ == "__main__":
    app.run(debug=True)