from flask import Blueprint, request, make_response, jsonify
from config.db_config import users
from flask_bcrypt import Bcrypt
import jwt
import os
import json
from bson import json_util
from datetime import datetime, timedelta


def parse_json(data):
    return json.loads(json_util.dumps(data))

bcrypt = Bcrypt()
auth_blueprint = Blueprint("auth_blueprint", __name__)


# login
@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        user_data = request.get_json()
        email = user_data.get("email")
        password = user_data.get("password")
        if email == None or password == None:
            return make_response(
                jsonify({"status": "error", "msg": "all fields are not provided"}), 400
            )

        existing_user = users.find_one({"email": email})
        if existing_user is None:
            return make_response(
                jsonify({"status": "error", "msg": "user not registered"}), 400
            )

        isSame = bcrypt.check_password_hash(existing_user["password"], password)
        if not isSame:
            return make_response(
                jsonify({"status": "error", "msg": "password does not matched"}), 400
            )

        id = parse_json(existing_user["_id"])
        token = jwt.encode(
            {
                "user_id": id,
                "email": existing_user["email"],
                "name": existing_user["name"],
                "exp": datetime.utcnow() + timedelta(days=150)
            },
            os.getenv("SECRET_KEY"),
            algorithm="HS256",
        )

        return make_response(
            jsonify(
                {
                    "status": "success",
                    "msg": "user logged in successfully",
                    "token": token,
                }
            ),
            200,
        )
    except Exception as err:
        print(err)
        return make_response(
            jsonify({"status": "internal server error", "msg": "something went wrong"}),
            500,
        )


# register
@auth_blueprint.route("/register", methods=["POST"])
def register():
    try:
        user_data = request.get_json()

        name = user_data.get("name")
        email = user_data.get("email")
        password = user_data.get("password")

        if name == None or email == None or password == None:
            return make_response(
                jsonify({"status": "error", "msg": "all fields are not provided"}), 400
            )

        existing_user = users.find_one({"email": email})
        if existing_user != None:
            return make_response(
                jsonify(
                    {
                        "status": "error",
                        "msg": "user already registered. login to continue",
                    }
                ),
                400,
            )

        hashed_password = bcrypt.generate_password_hash(password, rounds=10)
        new_user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "camera_list": [],
        }

        saved_user = users.insert_one(new_user)
        id = parse_json(saved_user.inserted_id)

        token = jwt.encode(
            {
                "user_id": id,
                "email": email, 
                "name": name,
                "exp": datetime.utcnow() + timedelta(days=150)
            },
            os.getenv("SECRET_KEY"),
            algorithm="HS256",
        )

        return make_response(
            jsonify(
                {
                    "status": "success",
                    "msg": "user registered successfully",
                    "token": token,
                }
            ),
            200,
        )
    except Exception as err:
        print(err)
        return make_response(
            jsonify({"status": "internal server error", "msg": "something went wrong"}),
            500,
        )

