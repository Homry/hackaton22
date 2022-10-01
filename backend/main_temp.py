import cv2
import numpy as np
from processing.convert_video import convert_image, convert_video_to_gif

def process_test_image(filename: str):
    img = cv2.imread(filename)
    new_img = convert_image(img)
    if new_img is None:
        print("No face")
        exit(1)
    cv2.imshow("Original", img)
    cv2.imshow("Emotinal", new_img)
    cv2.waitKey(0)


def process_from_camera():
    vid = cv2.VideoCapture(0)
    while True:
        ret, frame = vid.read()
        if not ret:
            continue
        converted_image = convert_image(frame, "yellow", "cat")
        if converted_image is not None:
            cv2.imshow("Emotinal", converted_image)
        cv2.imshow("Original", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def record_and_convert_video():
    vid = cv2.VideoCapture(0)
    frame_rate = round(vid.get(cv2.CAP_PROP_FPS))
    seconds = 5
    frames = []
    while True:
        ret, frame = vid.read()
        if not ret:
            continue
        frames.append(frame)
        if len(frames) >= seconds * frame_rate:
            break
    result_video = convert_video_to_gif (np.array(frames), "yellow", "cat")
    if result_video is None:
        print("Video is None")
        return
    with open("../test_res_video.gif", "wb") as f:
        f.write(result_video)


if __name__ == "__main__":
    # record_and_convert_video()
    process_from_camera()
    # process_test_image("../test_image.png")
    # process_test_image("../test_image5.jpeg")
