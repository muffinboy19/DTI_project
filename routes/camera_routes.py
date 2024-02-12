from flask import Blueprint, request, Response, make_response, jsonify
from bson.objectid import ObjectId
from bson import json_util

import json

from utilities.isAuth import isAuth
from config.db_config import cameras, users

import cloudinary
from cloudinary.uploader import destroy
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)

camera_blueprint = Blueprint("camera_blueprint", __name__)


def parse_json(data):
    return json.loads(json_util.dumps(data))


# add camera
@camera_blueprint.route("/addCamera", methods=["POST"])
def add_camera():
    try:
        token = isAuth()

        if token["status"] == "error":
            return make_response(jsonify({"status": "error", "msg": token["msg"]}), 400)

        user_data = token["msg"]
        id_object = user_data["user_id"]
        id = id_object["$oid"]

        camera_data = request.get_json()
        rtsp = camera_data.get("rtsp")
        camera_name = camera_data.get("camera_name")

        if rtsp == None or camera_name == None:
            return make_response(
                jsonify({"status": "error", "msg": "all fields are not provided"}), 400
            )

        camera = {
            "camera_name": camera_name,
            "rtsp_url": rtsp,
            "current_status": "off",
            "recordings": [],
        }
        saved_camera = cameras.insert_one(camera)
        camera_id = str(saved_camera.inserted_id)

        userlist_camera = {**camera, "_id": camera_id}
        updated_user = users.update_one(
            {"_id": ObjectId(id)}, {"$push": {"camera_list": userlist_camera}}
        )

        return make_response(
            jsonify(
                {
                    "status": "success",
                    "msg": "camera added successfully",
                    "camera": userlist_camera,
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


# for getting the camera list for a user
@camera_blueprint.route("/camera_list", methods=["GET"])
def get_camera_list():
    try:
        token = isAuth()

        if token["status"] == "error":
            return make_response(jsonify({"status": "error", "msg": token["msg"]}), 400)

        user_data = token["msg"]
        id = user_data["user_id"]["$oid"]

        user = users.find_one({"_id": ObjectId(id)})
        result = user["camera_list"]
        return make_response(
            jsonify(
                {
                    "status": "success",
                    "msg": "camera list obtained successfully",
                    "camera_list": result,
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


# for deleting camera
@camera_blueprint.route("/delete_camera", methods=["DELETE"])
def delete_camera():
    try:
        token = isAuth()

        if token["status"] == "error":
            return make_response(jsonify({"status": "error", "msg": token["msg"]}), 400)

        user_data = token["msg"]
        user_id = user_data["user_id"]["$oid"]

        data = request.get_json()
        camera_id = data["camera_id"]

        delete_camera_from_user = users.update_one(
            {"_id": ObjectId(user_id)}, {"$pull": {"camera_list": {"_id": camera_id}}}
        )

        camera = cameras.find_one({"_id": ObjectId(camera_id)})
        recordings = camera["recordings"]

        for i in range(len(recordings)):
            filename = recordings[i]["filename"]
            delete_file = destroy(public_id=filename, resource_type="video")

        delete_camera = cameras.delete_one(
            {"_id": ObjectId(camera_id)},
        )

        return make_response(
            jsonify(
                {
                    "status": "success",
                    "msg": "camera deleted successfully",
                }
            )
        )

    except Exception as err:
        print(err)
        return make_response(
            jsonify({"status": "internal server error", "msg": "something went wrong"}),
            500,
        )


# for updating camera name
@camera_blueprint.route("/update_camera_name", methods=["PATCH"])
def update_camera_name():
    try:
        token = isAuth()

        if token["status"] == "error":
            return make_response(jsonify({"status": "error", "msg": token["msg"]}), 400)

        user_data = token["msg"]
        user_id = user_data["user_id"]["$oid"]

        data = request.get_json()
        camera_id = data["camera_id"]
        new_camera_name = data["new_camera_name"]

        update_in_user_list = users.update_one(
            {"_id": ObjectId(user_id), "camera_list._id": camera_id},
            {"$set": {"camera_list.$.camera_name": new_camera_name}},
        )

        update_camera_name = cameras.update_one(
            {"_id": ObjectId(camera_id)}, {"$set": {"camera_name": new_camera_name}}
        )

        return make_response(
            jsonify(
                {
                    "status": "success",
                    "msg": "camera name updated successfully",
                }
            )
        )

    except Exception as err:
        print(err)
        return make_response(
            jsonify({"status": "internal server error", "msg": "something went wrong"}),
            500,
        )
