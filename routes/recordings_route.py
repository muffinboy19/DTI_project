from flask import Blueprint, request, Response, make_response, jsonify
from bson.objectid import ObjectId

from utilities.isAuth import isAuth
from config.db_config import cameras
from dotenv import load_dotenv

load_dotenv()

import cloudinary
from cloudinary.uploader import destroy
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)

recording_blueprint = Blueprint("recording_blueprint", __name__)


# to get all recordings of a camera
@recording_blueprint.route("/get_recordings", methods=["GET"])
def get_recordings_for_camera():
    try:
        token = isAuth()
        if token["status"] == "error":
            return make_response(jsonify({"status": "error", "msg": token["msg"]}), 400)
        user_data = token["msg"]

        camera_id = request.args.get("id")
        print(camera_id)
        if camera_id == None:
            return make_response(
                jsonify({"status": "error", "msg": "camera id not provided"}), 400
            )

        camera = cameras.find_one({"_id": ObjectId(camera_id)})
        recording_list = camera["recordings"]

        return make_response(
            jsonify(
                {
                    "status": "success",
                    "msg": "recordings obtained successfully",
                    "recordings": recording_list,
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


# to delete a particular recording
@recording_blueprint.route("/delete_recording", methods=["DELETE"])
def delete_recording():
    try:
        token = isAuth()
        if token["status"] == "error":
            return make_response(jsonify({"status": "error", "msg": token["msg"]}), 400)
        user_data = token["msg"]

        data = request.get_json()
        camera_id = data["camera_id"]
        filename = data["filename"]

        if camera_id == None or filename == None:
            return make_response(
                jsonify({"status": "error", "msg": "all fields are not provided"}), 400
            )

        update_camera_recordings_list = cameras.update_one(
            {"_id": ObjectId(camera_id)},
            {"$pull": {"recordings": {"filename": filename}}},
        )
        delete_video_from_cloudinary = destroy(
            public_id=filename, resource_type="video"
        )

        return make_response(
            jsonify(
                {
                    "status": "success",
                    "msg": "recording deleted successfully",
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
