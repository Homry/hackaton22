import numpy as np
import cv2
import mediapipe as mp
from processing.data import Point, FaceItem


mesh_detector = detector = mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9)

# NOSE_LINE = [2, 1, 168]
# NOSE_CORNERS = [327, 98]
FACE_ITEMS = {
    "nose": FaceItem("nose", [2, 1, 168], True),
    "lips_inner_lower": FaceItem("lips_inner_lower", [95, 88, 178, 87, 14, 317, 402, 318, 324], False, draw=False),
    "lips_inner_upper": FaceItem("lips_inner_upper", [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308], False, draw=False),
    "right_eye": FaceItem("right_eye", [246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7, 33], True),
    "left_eye": FaceItem("left_eye", [466, 388, 387, 386, 385, 384, 398, 362, 382, 381, 380, 374, 373, 390, 249, 263], True),
    "lips": FaceItem("lips", [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146], True),
    "left_brow": FaceItem("left_brow", [46, 53, 52, 65, 55], False, 2),
    "right_brow": FaceItem("right_brow", [276, 283, 282, 295, 285], False, 2),
    "silhouette": FaceItem(
        "silhouette",
        [
            10,  338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
            397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
            172, 58,  132, 93,  234, 127, 162, 21,  54,  103, 67,  109
        ], True, draw=False)
}
'''lipsUpperInner = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
# lipsLowerInner = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]
lipsLowerInner = [95, 88, 178, 87, 14, 317, 402, 318, 324]
rightEyeUpper0 = [246, 161, 160, 159, 158, 157, 173]
rightEyeLower0 = [33, 7, 163, 144, 145, 153, 154, 155, 133]
leftEyeUpper0 = [466, 388, 387, 386, 385, 384, 398]
leftEyeLower0 = [263, 249, 390, 373, 374, 380, 381, 382, 362]
# lipsUpperOuter = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
lipsUpperOuter = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409]
lipsLowerOuter = [146, 91, 181, 84, 17, 314, 405, 321, 375, 291]

rightEyebrowUpper = [46, 53, 52, 65, 55] #[156, 70, 63, 105, 66, 107, 55, 193]
leftEyebrowUpper = [276, 283, 282, 295, 285] #[383, 300, 293, 334, 296, 336, 285, 417]

silhouette = [
    10,  338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
    397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
    172, 58,  132, 93,  234, 127, 162, 21,  54,  103, 67,  109
]'''

EPS = 0.02

### COLOR IS BGR!!!!!

def draw_cirlce(size):
    coeff = 0.95
    image = np.ones(size) * 255
    h, w = size[:2]
    image = cv2.circle(image, (w // 2, h // 2), round(w // 2 * coeff), (0, 255, 255), -1)
    image = cv2.circle(image, (w // 2, h // 2), round(w // 2 * coeff), (0, 0, 0), 3)
    return image


def convert_mediapipe_point(mp_point, shape):
    return Point(round(mp_point.x * shape[1]), round(mp_point.y * shape[0]))


def get_coords_from_face(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    res = mesh_detector.process(image)
    is_find = False
    if res.multi_face_landmarks:
        for face_landmarks in res.multi_face_landmarks:
            lands = face_landmarks.landmark
            is_find = True
            for face_item in FACE_ITEMS.values():
                face_item.process_landmarks(lands)
    sil = np.array([(p.x, p.y) for p in FACE_ITEMS["silhouette"].saved_landmarks])
    min_x = min(sil[:, 0])
    max_x = max(sil[:, 0])
    min_y = min(sil[:, 1])
    max_y = max(sil[:, 1])
    face_size = (min_x, max_x, min_y, max_y)
    if not is_find:
        return None
    return face_size


def draw_lines(image, size):
    coeff = 0.8
    h, w = size[:2]
    offset_x = round(w * (1 - coeff) / 2)
    offset_y = round(h * (1 - coeff) / 2)
    h *= coeff
    w *= coeff

    def transform_func(point):
        return (round(point.x * h) + offset_x, round(point.y * w) + offset_y)

    for face_item in FACE_ITEMS.values():
        face_item.draw_lines(image, transform_func)


def resize_all_points(face_size):
    min_x, max_x, min_y, max_y = face_size
    passed_idx = set()
    x_len = max_x - min_x
    y_len = max_y - min_y

    def transform_func(point):
        return (point.x - min_x) / x_len, (point.y - min_y) / y_len

    for face_item in FACE_ITEMS.values():
        face_item.resize_saved_points(transform_func)


def check_open_mouth(draw_image):
    upper, lower = FACE_ITEMS["lips_inner_upper"].saved_landmarks, FACE_ITEMS["lips_inner_lower"].saved_landmarks
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
    face_size = res
    resize_all_points(face_size)
    draw_lines(new_image, size)
    check_open_mouth(new_image)
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
