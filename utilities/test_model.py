import cv2
import tensorflow as tf
import numpy as np
import time
from utilities.notify_user import send_notification

def detect(rtsp_url):
    camera=cv2.VideoCapture(rtsp_url)
    model=tf.keras.models.load_model('exp_vs_acc_vs_normal_for_img.h5')

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            buffer_frame=frame
            resized_frame=cv2.resize(frame, (100,100))
            
            list.append(resized_frame)
            if len(list)==10:
                ct=[0]*4
                result=model.predict(np.asarray(list))
                for i in range(10):
                    if np.argmax(result)==0 and result[i][0]>0.60:
                        ct[0]+=1
                    elif np.argmax(result)==1 and result[i][1]>0.6:
                        ct[1]+=1
                    elif np.argmax(result)==2 and result[i][2]>0.6:
                        ct[2]+=1
                    else : ct[3]+=1
                max_value = max(ct)
                max_indices = [i for i, value in enumerate(ct) if value == max_value]
                if max_indices==1 or max_indices==2:
                    send_notification()
                    break
                list=[]
        time.sleep(0.1)

    return "ended"