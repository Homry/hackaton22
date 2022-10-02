import numpy as np
import cv2
import mediapipe as mp
import imageio
import io
from processing.data import Point, FaceItem
from processing.presets import CatPreset, LittleDevilPreset


mesh_detector = detector = mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9)

FACE_ITEMS = {
    "nose": FaceItem("nose", [327, 1, 98, 168], True),
    "lips_inner_lower": FaceItem("lips_inner_lower", [95, 88, 178, 87, 14, 317, 402, 318, 324], False, draw=False),
    "lips_inner_upper": FaceItem("lips_inner_upper", [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308], False, draw=False),
    "inner_lips": FaceItem("inner_lips", [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95], True, draw=False),
    "right_eye": FaceItem("right_eye", [246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7, 33], True, draw=True),
    "around_right_eye2": FaceItem("around_right_eye2", [113, 225, 224, 223, 222, 221, 189, 244, 233, 232, 231, 230, 229, 228, 31, 226], True, draw=False, tickness=2),
    "around_right_eye3": FaceItem("around_right_eye3", [143, 111, 117, 118, 119, 120, 121, 128, 245], False, draw=False, tickness=1),
    "left_eye": FaceItem("left_eye", [466, 388, 387, 386, 385, 384, 398, 362, 382, 381, 380, 374, 373, 390, 249, 263], True),
    "around_left_eye1": FaceItem("around_left_eye1", [467, 260, 259, 257, 258, 286, 414, 463, 341, 256, 252, 253, 254, 339, 255, 359], True, draw=False),
    "around_left_eye3": FaceItem("around_left_eye3", [372, 340, 346, 347, 348, 349, 350, 357, 465], False, draw=False   , tickness=1),
    "lips": FaceItem("lips", [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146], True, draw=False),
    "left_brow": FaceItem("left_brow", [46, 53, 52, 65, 55], False, 2),
    "right_brow": FaceItem("right_brow", [276, 283, 282, 295, 285], False, 2),
    "line1": FaceItem("line1", [412, 343, 277, 329, 330, 280, 376], False, 1, draw=False),
    "silhouette": FaceItem(
        "silhouette",
        [
            10,  338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
            397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
            172, 58,  132, 93,  234, 127, 162, 21,  54,  103, 67,  109
        ], True, draw=False),
    "leye": FaceItem("leye", [469, 470, 471, 472], True, tickness=1, draw=False),
    #"leye": FaceItem("leye", [469, 471], True, tickness=1),
    "reye": FaceItem("reye", [474, 475, 476, 477], True, tickness=1, draw=False),
    "cheeks": FaceItem("cheeks", [425, 205], False, tickness=1, draw=False),
}

EPS = 0.02
DRAW_COEFF = 0.7
SKIP_FRAMES = 7

COLORS = {
    "yellow": (0, 255, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "red": (0, 0, 255),
    "purple": (128, 0, 128),
    "pink": (180, 105, 255),
}

### COLOR IS BGR!!!!!
SIZE = (600, 600, 3)
H, W = SIZE[:2]
SIZE_OFFSET_X = round(W * (1 - DRAW_COEFF) / 2)
SIZE_OFFSET_Y = round(H * (1 - DRAW_COEFF) / 2)
H *= DRAW_COEFF
W *= DRAW_COEFF

def transform_func(point):
    return (round(point.x * W) + SIZE_OFFSET_X, round(point.y * H) + SIZE_OFFSET_Y)

####

def draw_cirlce(size, fill_color):
    coeff = 0.95
    image = np.ones(size, dtype=np.uint8) * 255
    h, w = size[:2]
    image = cv2.circle(image, (w // 2, h // 2), round(w // 2 * coeff), fill_color, -1)
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
    if not is_find:
        return None
    sil = np.array([(p.x, p.y) for p in FACE_ITEMS["silhouette"].saved_landmarks])
    min_x = min(sil[:, 0])
    max_x = max(sil[:, 0])
    min_y = min(sil[:, 1])
    max_y = max(sil[:, 1])
    face_size = (min_x, max_x, min_y, max_y)
    return face_size


def draw_lines(image, size, color, draw_lips=False):
    for face_item in FACE_ITEMS.values():
        face_item.draw_lines(image, transform_func)
    if draw_lips:
        if check_open_mouth(image):
            cv2.drawContours(image, [np.array([transform_func(p) for p in FACE_ITEMS["inner_lips"].saved_landmarks])], -1, np.array(color, dtype=np.uint8) * 0.75, -1)
            FACE_ITEMS["inner_lips"]._always_draw_lins(image, transform_func)
        else:
            FACE_ITEMS["lips_inner_upper"]._always_draw_lins(image, transform_func)


def resize_all_points(face_size):
    min_x, max_x, min_y, max_y = face_size
    passed_idx = set()
    x_len = max_x - min_x
    y_len = max_y - min_y

    def resize_func(point):
        return (point.x - min_x) / x_len, (point.y - min_y) / y_len

    for face_item in FACE_ITEMS.values():
        face_item.resize_saved_points(resize_func)


def check_open_mouth(draw_image):
    upper, lower = FACE_ITEMS["lips_inner_upper"].saved_landmarks, FACE_ITEMS["lips_inner_lower"].saved_landmarks
    for i in range(min(len(upper), len(lower))):
        if abs(upper[i].y - lower[i].y) > EPS:
            return True
    return False


def apply_preset(preset_name: str, image, size, color):

    if preset_name == "cat":
        CatPreset.apply_preset(image, FACE_ITEMS["left_brow"], FACE_ITEMS["right_brow"], FACE_ITEMS["cheeks"], transform_func, color)
    elif preset_name == "little_devil":
        LittleDevilPreset.apply_preset(image, FACE_ITEMS["left_brow"], FACE_ITEMS["right_brow"], transform_func, color)


def calculate_distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5


def find_closest_points(points, point1, point2):
    min_dist = calculate_distance(point1, points[0]) + calculate_distance(point2, points[0])
    min_point = points[0]
    for point in points[1:]:
        cur_dist = calculate_distance(point1, point) + calculate_distance(point2, point)
        if min_dist > cur_dist:
            min_dist = cur_dist
            min_point = point
    return min_point


def draw_eye(image, eye: FaceItem, eyelid: FaceItem, ):
    left, right = eye.saved_landmarks[2], eye.saved_landmarks[0]
    up, down = eye.saved_landmarks[1], eye.saved_landmarks[3]
    new_points = [
        left,
        find_closest_points(eyelid.saved_landmarks, left, up),
        find_closest_points(eyelid.saved_landmarks, right, up),
        right,
        find_closest_points(eyelid.saved_landmarks, right, down),
        find_closest_points(eyelid.saved_landmarks, left, down),
    ]
    contour = [np.array([transform_func(p) for p in new_points], dtype=np.int32)]
    cv2.drawContours(image, contour, -1, (0, 0, 0), -1)


def convert_image(image: 'np.ndarry[float]', color_name, preset_name):
    size = SIZE
    if COLORS.get(color_name) is None:
        return None
    color = COLORS[color_name]
    new_image = draw_cirlce(size, color)
    res = get_coords_from_face(image)
    if res is None:
        return None
    face_size = res
    resize_all_points(face_size)
    draw_lines(new_image, size, color, True)
    draw_eye(new_image, FACE_ITEMS["leye"], FACE_ITEMS["right_eye"])
    draw_eye(new_image, FACE_ITEMS["reye"], FACE_ITEMS["left_eye"])
    apply_preset(preset_name, new_image, size, color)
    return cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)


def convert_video(video: 'np.ndarray[float]', color_name, preset_name, skip_frames=None):
    step = 1 if skip_frames is None else skip_frames
    res_video = []
    for i in range(0, len(video), step):
        cur_frame = video[i]
        converted = convert_image(cur_frame, color_name, preset_name)
        if converted is None:
            continue
        res_video.append(converted)
    if len(res_video) == 0:
        return None
    return res_video

def create_gif(video):
    output = imageio.mimsave("<bytes>", video, format="gif")
    return output

def convert_video_to_gif(video: 'np.ndarray[float]', color_name='yellow', preset_name=''):
    new_video = convert_video(video, color_name, preset_name, None)

    if new_video is None:
        return None
    new_video = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in video]
    return create_gif(new_video)
