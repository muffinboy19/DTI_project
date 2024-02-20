from flask import Blueprint, request, Response, make_response, jsonify
from bson.objectid import ObjectId
from bson import json_util

import cv2
import json
import asyncio
from threading import Thread

from config.db_config import users, cameras
from utilities.isAuth import isAuth
from utilities.test_model import detect
from utilities.view_video import live_stream, record_video
from utilities.uploading_video import upload_video
from utilities.save_video import save_video_toDB


def parse_json(data):
    return json.loads(json_util.dumps(data))


user_blueprint = Blueprint("user_blueprint", __name__)


# start service
@user_blueprint.route("/start", methods=["GET"])
def start_service():
    try:
        token = isAuth()
        if token["status"] == "error":
            return make_response(jsonify({"status": "error", "msg": token["msg"]}), 400)

        user_data = token["msg"]

        camera_id = request.args.get("id")
        if camera_id == None:
            return make_response(
                jsonify({"status": "error", "msg": "camera id not provided"}), 400
            )

        camera = cameras.find_one({"_id": ObjectId(camera_id)})
        rtsp_url = camera["rtsp_url"]
        update_cuurent_status = cameras.update_one(
            {"_id": ObjectId(camera_id)}, {"$set": {"camera_status": "on"}}
        )

        thread = Thread(
            target=detect,
            args=(
                rtsp_url,
                camera_id,
            ),
        )
        thread.start()

        return make_response(
            jsonify({"status": "success", "msg": "testing started successfully"}), 200
        )
    except Exception as err:
        print(err)
        return make_response(
            jsonify({"status": "internal server error", "msg": "something went wrong"}),
            500,
        )


# view live recording
@user_blueprint.route("/view", methods=["GET"])
def view_video():
    try:
        token = isAuth()
        if token["status"] == "error":
            return make_response(jsonify({"status": "error", "msg": token["msg"]}), 400)
        user_data = token["msg"]

        camera_id = request.args.get("id")
        if camera_id == None:
            return make_response(
                jsonify({"status": "error", "msg": "camera id not provided"}), 400
            )

        camera = cameras.find_one({"_id": ObjectId(camera_id)})
        rtsp_url = camera["rtsp_url"]
        rtsp_url=int(rtsp_url)

        return Response(
            live_stream(rtsp_url), mimetype="multipart/x-mixed-replace; boundary=frame"
        )
    except Exception as err:
        print(err)
        return make_response(
            jsonify({"status": "internal server error", "msg": "something went wrong"}),
            500,
        )

