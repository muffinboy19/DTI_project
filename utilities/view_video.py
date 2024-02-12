import cv2


def live_stream(rtsp_url):
    camera = cv2.VideoCapture(rtsp_url)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            res = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n")


def record_video(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("video\\recorded_video.avi", fourcc, 40.0, (640, 480))

    max_frames = 400
    frame_count = 0
    list = []
    while frame_count < max_frames:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            resized_frame = cv2.resize(frame, (100, 100))
            list.append(resized_frame)
        frame_count += 1

    new_list = []
    iterate_over_frames = 0
    while iterate_over_frames < max_frames:
        new_list.append(list[iterate_over_frames])
        iterate_over_frames += 40

    cap.release()
    out.release()
    return new_list
