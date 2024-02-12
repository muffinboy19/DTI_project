from flask import Flask, make_response, jsonify
from dotenv import load_dotenv

load_dotenv()

from routes.auth_routes import auth_blueprint
from routes.user_routes import user_blueprint
from routes.recordings_route import recording_blueprint
from routes.camera_routes import camera_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint, url_prefix="/auth/")
app.register_blueprint(user_blueprint, url_prefix="/user/")
app.register_blueprint(recording_blueprint, url_prefix="/recording/")
app.register_blueprint(camera_blueprint, url_prefix="/camera/")


@app.route("/<path:default>", methods=["GET", "POST", "DELETE", "PATCH"])
def func(default):
    return make_response(jsonify({"status": "error", "msg": "not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
