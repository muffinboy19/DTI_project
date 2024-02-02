from flask import Flask, make_response, jsonify
from dotenv import load_dotenv
load_dotenv()

from routes.auth_routes import auth_blueprint
from routes.user_routes import user_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint,url_prefix='/')
app.register_blueprint(user_blueprint,url_prefix='/')
@app.route('/<path:default>', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def func(default):
    return make_response(jsonify({
        'status':'error',
        'msg':'not found'
    }),404)

if (__name__ == "__main__"):
    app.run(debug=True,port=5001)
