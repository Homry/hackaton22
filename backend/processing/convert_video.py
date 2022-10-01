import numpy as np
import cv2
import mediapipe as mp
from processing.data import Point


mesh_detector = detector = mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

NOSE_LINE = [2, 1, 168]
NOSE_CORNERS = [327, 98]
lipsUpperInner = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
# lipsLowerInner = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]
lipsLowerInner = [95, 88, 178, 87, 14, 317, 402, 318, 324]
rightEyeUpper0 = [246, 161, 160, 159, 158, 157, 173]
rightEyeLower0 = [33, 7, 163, 144, 145, 153, 154, 155, 133]
leftEyeUpper0 = [466, 388, 387, 386, 385, 384, 398]
leftEyeLower0 = [263, 249, 390, 373, 374, 380, 381, 382, 362]
# lipsUpperOuter = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
lipsUpperOuter = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409]
lipsLowerOuter = [146, 91, 181, 84, 17, 314, 405, 321, 375, 291]

silhouette = [
    10,  338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
    397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
    172, 58,  132, 93,  234, 127, 162, 21,  54,  103, 67,  109
]

EPS = 0.02

### COLOR IS BGR!!!!!

def draw_cirlce(size):
    coeff = 0.95
    image = np.ones(size) * 255
    # image[:] = (255, 255, 255)
    h, w = size[:2]
    image = cv2.circle(image, (w // 2, h // 2), round(w // 2 * coeff), (0, 255, 255), -1)
    image = cv2.circle(image, (w // 2, h // 2), round(w // 2 * coeff), (0, 0, 0), 3)
    return image


def convert_mediapipe_point(mp_point, shape):
    return Point(round(mp_point.x * shape[1]), round(mp_point.y * shape[0]))


def get_coords_from_face(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    res = mesh_detector.process(image)
    result_lines = {
        "nose": [],
        "left_eye": [],
        "right_eye": [],
        "lips": [],
        "silhouette": [],
    }
    lips_inner = [[], []]
    if res.multi_face_landmarks:
        for face_landmarks in res.multi_face_landmarks:
            lands = face_landmarks.landmark
            for index in NOSE_LINE:
                result_lines["nose"].append(lands[index])
            for index in lipsLowerOuter:
                result_lines["lips"].insert(0, lands[index])
            for index in lipsUpperOuter:
                result_lines["lips"].append(lands[index])
            for index in rightEyeUpper0:
                result_lines["right_eye"].append(lands[index])
            for index in rightEyeLower0:
                result_lines["right_eye"].insert(0, lands[index])
            for index in leftEyeUpper0:
                result_lines["left_eye"].append(lands[index])
            for index in leftEyeLower0:
                result_lines["left_eye"].insert(0, lands[index])

            # inner lips
            for index in lipsLowerInner:
                lips_inner[0].insert(0, lands[index])
            for index in lipsUpperInner:
                lips_inner[1].append(lands[index])
            # face contour
            sil = np.array([(lands[index].x, lands[index].y) for index in silhouette])
            min_x = min(sil[:, 0])
            max_x = max(sil[:, 0])
            min_y = min(sil[:, 1])
            max_y = max(sil[:, 1])
            face_size = (min_x, max_x, min_y, max_y)
    if len(result_lines["nose"]) == 0:
        return None
    return result_lines, face_size, lips_inner


def draw_lines(image, points: dict, size):
    coeff = 0.8
    h, w = size[:2]
    offset_x = round(w * (1 - coeff) / 2)
    offset_y = round(h * (1 - coeff) / 2)
    h *= coeff
    w *= coeff
    for key, coords in points.items():
        for i in range(len(coords)):
            pt1 = (round(coords[i].x * h) + offset_x, round(coords[i].y * w) + offset_y)
            pt2 = (round(coords[(i + 1) % len(coords)].x * h) + offset_x, round(coords[(i + 1) % len(coords)].y  * w) + offset_y)
            cv2.line(image, pt1, pt2, (0, 0, 0), 3)


def resize_all_points(face_points, face_size):
    min_x, max_x, min_y, max_y = face_size
    passed_idx = set()
    x_len = max_x - min_x
    y_len = max_y - min_y
    for key, values in face_points.items():
        for v in values:
            v.x = (v.x - min_x) / x_len
            v.y = (v.y - min_y) / y_len


def check_open_mouth(draw_image, lips_inner):
    upper, lower = lips_inner
    for i in range(min(len(upper), len(lower))):
        if abs(upper[i].y - lower[i].y) > EPS:
            text = "Mouth is open"
            color = (0, 0, 255)
            break
    else:
        text = "Mouth is closed"
        color = (0, 255, 0)
    cv2.putText(draw_image, text, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color)


def convert_image(image: 'np.ndarry[float]'):
    size = (500, 500, 3)
    new_image = draw_cirlce(size)
    res = get_coords_from_face(image)
    if res is None:
        return None
    face_points, face_size, lips_inner = res
    resize_all_points(face_points,face_size)
    draw_lines(new_image, face_points, size)
    check_open_mouth(new_image, lips_inner)
    return new_image


def convert_video(video: 'np.ndarray[float]', frame_rate):
    if frame_rate < 3:
        return None
    res_video = []
    for i in range(0, len(video), frame_rate // 3):
        cur_frame = video[i]
        converted = convert_image(cur_frame)
        if converted is None:
            continue
        res_video.append(converted)
    return np.array(res_video)
