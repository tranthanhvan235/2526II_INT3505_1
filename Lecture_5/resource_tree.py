from flask import jsonify
from database_setup import app, Loan

@app.route('/users/<int:user_id>/loans', methods=['GET'])
def get_user_loans(user_id):
    # Resource Tree: /users/{id}/loans
    loans = Loan.query.filter_by(user_id=user_id).all()
    return jsonify({
        "resource": f"List of loans for user {user_id}",
        "data": [{"loan_id": l.id, "book_id": l.book_id} for l in loans]
    })

if __name__ == '__main__':
    app.run(port=5001)