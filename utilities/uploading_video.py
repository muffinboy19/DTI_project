import cloudinary
import os
from cloudinary.uploader import upload
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)


def upload_file_from_local_system(filepath, filename):
    try:
        upload_result = upload(filepath, resource_type="video", public_id=filename)
        return upload_result
    except Exception as err:
        return err


def upload_video(filename):
    file_to_upload = "video\\recorded_video.avi"

    upload_result = upload_file_from_local_system(file_to_upload, filename)
    return upload_result["secure_url"]
