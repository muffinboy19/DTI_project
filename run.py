import cv2
import tensorflow as tf
import numpy as np
from utilities.save_video import save_video_toDB
from googlesol import ColabArgs, main
import tracemalloc

tracemalloc.start()

def model2(frame_list):
    """
    Load a pre-trained TensorFlow model and make predictions on the provided frames.
    
    Parameters:
    - frame_list (list): A list of resized frames to be analyzed by the model.
    
    Returns:
    - str: The prediction made by the model, which can be "explosion", "accident", or "normal".
    """
    print("Executing model2...")  # Log execution
    print(f"Input frame list size: {len(frame_list)}")  # Log input size

    model = tf.keras.models.load_model("models/exp_vs_acc_vs_normal_for_img.h5")
    result = model.predict(np.asarray(frame_list))
    
    print("Model output:", result)  # Log the model output

    ct = [0] * 4
    for i in range(10):
        if np.argmax(result) == 0:
            ct[0] += 1
        elif np.argmax(result) == 1:
            ct[1] += 1
        elif np.argmax(result) == 2:
            ct[2] += 1

    max_value = max(ct)
    max_indices = [i for i, value in enumerate(ct) if value == max_value]
    print("Count of predictions:", ct)  # Log the counts

    if max_indices == 1:
        prediction = "explosion"
    elif max_indices == 2:
        prediction = "accident"
    else:
        prediction = "normal"
        
    print("Final prediction from model2:", prediction)  # Log the final prediction
    return prediction


def read_video_frames(video_path):
    """
    Read and resize frames from the provided video file.
    
    Parameters:
    - video_path (str): The path to the video file to read.
    
    Returns:
    - list: A list of resized frames extracted from the video.
    """
    cap = cv2.VideoCapture(video_path)
    frame_list = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize frame for the model
        resized_frame = cv2.resize(frame, (100, 100))
        frame_list.append(resized_frame)

    cap.release()
    print(f"Total frames read from video: {len(frame_list)}")  # Log total frames read
    return frame_list


def detect(video_path, camera_id, device_token):
    """
    Detect violence in a video by analyzing frames with two models.
    
    Parameters:
    - video_path (str): The path to the video file to analyze.
    - camera_id (str): The ID of the camera that recorded the video.
    - device_token (str): A token identifying the device.
    
    Returns:
    - None: This function performs analysis and saves predictions to the database.
    """
    print(f"Detecting violence in video from camera: {camera_id}")  # Log camera ID
    print(f"Device Token: {device_token}")  # Log device token
    flag = 0

    # Read frames from the video file
    frame_list_for_model2 = read_video_frames(video_path)

    # Log the number of frames read
    print(f"Number of frames read for model2: {len(frame_list_for_model2)}")

    # Check if we got enough frames
    if len(frame_list_for_model2) < 10:
        print("Not enough frames for analysis.")  # Log insufficient frames
        flag = 1
    else:
        # Run the first model prediction here
        test_data = ColabArgs(
            "models/model_16_m3_0.8888.pth",
            False,
            video_path,
            "video/vd1.mp4",
            16,
            20,
            True,
        )
        result_from_model1 = main(test_data)
        print("Result from model1:", result_from_model1)  # Log the result from model1

        if len(result_from_model1) == 0:
            print("No result from model1.")  # Log if no result
            flag = 1
        else:
            fighting_prob = result_from_model1[0][0]
            normal_prob = result_from_model1[0][1]

            fighting_prob_ = float(f"{fighting_prob:.5f}")
            normal_prob_ = float(f"{normal_prob:.5f}")

            # Check if the probability of fighting is high
            if fighting_prob_ >= 0.92:
                prediction = "fighting"
                print(f"Prediction based on model1: {prediction}")  # Log prediction from model1
            elif normal_prob_ >= 0.92:
                print("Normal activity detected, no action taken.")  # Log normal activity
                prediction = "normal"  # Explicitly setting prediction to normal
            else:
                print("Calling model2 function...")  # Log before calling model2
                model2_result = model2(frame_list_for_model2)  # Call to model2
                prediction = model2_result if model2_result != "normal" else None

                if prediction:
                    print(f"Prediction from model2: {prediction}")  # Log prediction from model2

    # Save the prediction to the database if a prediction was made
    if flag == 0 and prediction:
        save_video_toDB(camera_id, prediction, device_token)
        print(f"Prediction saved to database: {prediction}")  # Log saved prediction


if __name__ == "__main__":
    # Hardcoded parameters
    video_path = r"C:\Users\gaura\OneDrive\Desktop\model\AnomAlert-Backend\video\vd1.mp4"  # Using raw string
    camera_id = "camera_001"  # Replace with your actual camera ID
    device_token = "device_ABC123"  # Replace with your actual device token

    # Call the detect function with hardcoded parameters
    detect(video_path, camera_id, device_token)
    model2(read_video_frames(video_path))
