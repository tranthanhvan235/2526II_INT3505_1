from flask import Flask
from api.v1 import v1 as api_v1
from api.v2 import v2 as api_v2
from Lecture9.payment_api.middleware.deprecation import add_deprecation_headers

app = Flask(__name__)

app.register_blueprint(api_v1)
app.register_blueprint(api_v2)

app.after_request(add_deprecation_headers)

if __name__ == '__main__':
    app.run(debug=True, port=5000)