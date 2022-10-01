import cv2
import math
import numpy as np
from processing.data import FaceItem, Point



class CatPreset:

    OFFSET_Y = 0.15
    COLOR = (0, 0, 0)
    TICKNESS = 3
    ANGLES = [30, 0, -30]
    LINE_LEN = 0.4
    STEP_LINE = 0.05
    STEP_TO_NOSE = 0.1
    EAR_STEP = 0.05

    def __draw_ear(image, new_start, middle, new_end, color):
        cv2.drawContours(image, [np.array([new_start, middle, new_end], dtype=np.int32)], -1, color, -1)
        cv2.line(image, new_start, middle, CatPreset.COLOR, CatPreset.TICKNESS)
        cv2.line(image, middle, new_end, CatPreset.COLOR, CatPreset.TICKNESS)

    def draw_ear(image, start_point, end_point, transform, color, direction=1):
        new_start = Point(start_point.x, start_point.y - CatPreset.OFFSET_Y)
        new_end = Point(end_point.x, end_point.y - CatPreset.OFFSET_Y)
        middle = Point(start_point.x, end_point.y - CatPreset.OFFSET_Y * 3)
        CatPreset.__draw_ear(image, transform(new_start), transform(middle), transform(new_end), np.array(color, dtype=np.uint8) * 0.75)
        middle.y += CatPreset.EAR_STEP * 1.5
        middle.x -= direction * CatPreset.EAR_STEP
        new_start.x -= direction * CatPreset.EAR_STEP
        new_end.x += direction * CatPreset.EAR_STEP
        CatPreset.__draw_ear(image, transform(new_start), transform(middle), transform(new_end), np.array(color, dtype=np.uint8) * 1.25)
        


    def draw_mustache(image, center_point, transform, direction=1):
        for angle in CatPreset.ANGLES:
            cos, sin = direction * math.cos(math.radians(angle)), direction * math.sin(math.radians(angle))
            pt1 = Point(center_point.x + cos * CatPreset.STEP_LINE - direction * CatPreset.STEP_TO_NOSE, center_point.y + sin * CatPreset.STEP_LINE)
            pt2 = Point(center_point.x + cos * CatPreset.LINE_LEN - direction * CatPreset.STEP_TO_NOSE, center_point.y + sin * CatPreset.LINE_LEN)
            cv2.line(image, transform(pt1), transform(pt2), CatPreset.COLOR, CatPreset.TICKNESS // 2)
        

    def apply_preset(image, left_brow: FaceItem, right_brow: FaceItem, cheeks: FaceItem, transform, color):
        left_start = left_brow.saved_landmarks[0]
        left_end = left_brow.saved_landmarks[-1]
        right_start = right_brow.saved_landmarks[0]
        right_end = right_brow.saved_landmarks[-1]
        CatPreset.draw_ear(image, left_start, left_end, transform, color, direction=-1)
        CatPreset.draw_ear(image, right_start, right_end, transform, color)
        CatPreset.draw_mustache(image, cheeks.saved_landmarks[0], transform)
        CatPreset.draw_mustache(image, cheeks.saved_landmarks[1], transform, -1)

