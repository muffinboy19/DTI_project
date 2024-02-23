from uuid import uuid4
import datetime
import json

from utilities.uploading_video import upload_video
from utilities.notify_user import send_notification
from config.db_config import cameras
from bson.objectid import ObjectId

from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))


def save_video_toDB(camera_id,prediction,device_token):
    random_name = uuid4().hex
    current_time = str(datetime.datetime.now())

    update_camera_current_status=cameras.update_one(
        {'_id':ObjectId(camera_id)},
        {'$set':{'current_status':'off'}}
    )

    video_url = upload_video(random_name)
    recording = {
        "video_url": video_url,
        "current_time": current_time,
        "filename": random_name,
        "anomaly":prediction
    }

    save_recording_to_camera = cameras.update_one(
        {"_id": ObjectId(camera_id)}, {"$push": {"recordings": recording}}
    )

    user_camera=cameras.find_one({"_id": ObjectId(camera_id)})
    camera_name=user_camera['camera_name']

    token_list=[]
    token_list.append(device_token)

    send_notification(f'{prediction} detected!', f'we detected an anomaly in your {camera_name}', token_list)
    return 
    
