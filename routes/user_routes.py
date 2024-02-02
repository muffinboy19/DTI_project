from flask import Blueprint, request, Response, make_response, jsonify

import cv2
import json

from config.db_config import cameras
from utilities.isAuth import isAuth
from utilities.test_model import detect
from utilities.view_video import live_stream

user_blueprint=Blueprint('user_blueprint', __name__)

# add camera
@user_blueprint.route('/addCamera',methods=['POST'])
def add_camera():
    try:
        token=isAuth()

        if token['status']=='error':
            return make_response(jsonify({
                'status':'error',
                'msg':token['msg']
            }),400)
        
        user_data=token['msg']

        camera_data = request.get_json()
        rtsp=camera_data.get('rtsp_url')

        if rtsp == None:
            return make_response(jsonify({
                'status': 'error',
                'msg': 'all fields are not provided'
            }), 400)
        
        cameras.insert_one({
            'rtsp_url':rtsp,
            'user_id':user_data['user_id'],
            'user_name':user_data['name'],
            'user_email':user_data['email']
        })

        return make_response(jsonify({
                'status': 'success',
                'msg': 'camera added successfully',
            }), 200)
    
    except Exception as err:
        print(err)
        return make_response(jsonify({
            'status': 'internal server error',
            'msg': 'something went wrong'
        }),500)

# start service
@user_blueprint.route('/start',methods=['POST'])
def start_service():
    try:
        token=isAuth()
        if token['status']=='error':
            return make_response(jsonify({
                'status':'error',
                'msg':token['msg']
            }),400)
        user_data=token['msg']

        data=request.get_json()
        rtsp_url=data.get('rtsp_url')

        result=detect(rtsp_url)

        return make_response(jsonify({
            'status': 'success',
            'msg': 'testing started successfully'
        }),200)
    except Exception as err:
        print(err)
        return make_response(jsonify({
            'status': 'internal server error',
            'msg': 'something went wrong'
        }),500)

# view recording
@user_blueprint.route('/view')
def view_video():
    try:
        token=isAuth()
        if token['status']=='error':
            return make_response(jsonify({
                'status':'error',
                'msg':token['msg']
            }),400)
        user_data=token['msg']

        data=request.get_json()
        rtsp_url=data.get('rtsp_url')

        return Response(live_stream(rtsp_url), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        print(err)
        return make_response(jsonify({
            'status': 'internal server error',
            'msg': 'something went wrong'
        }),500)