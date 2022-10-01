import cv2
import numpy as np
from processing.data import FaceItem, Point


class CatPreset:

    OFFSET_Y = 0.15
    COLOR = (0, 0, 0)
    TICKNESS = 3
    ANGLES = []

    def draw_ear(image, start_point, end_point, transform):
        new_start = Point(start_point.x, start_point.y - CatPreset.OFFSET_Y)
        new_end = Point(end_point.x, end_point.y - CatPreset.OFFSET_Y)
        middle = Point(start_point.x, end_point.y - CatPreset.OFFSET_Y * 3)
        cv2.line(image, transform(new_start), transform(middle), CatPreset.COLOR, CatPreset.TICKNESS)
        cv2.line(image, transform(middle), transform(new_end), CatPreset.COLOR, CatPreset.TICKNESS)


    def draw_mustache(image, center_point, transform):
        pass
        

    def apply_preset(image, left_brow: FaceItem, right_brow: FaceItem, transform):
        left_start = left_brow.saved_landmarks[0]
        left_end = left_brow.saved_landmarks[-1]
        right_start = right_brow.saved_landmarks[0]
        right_end = right_brow.saved_landmarks[-1]
        CatPreset.draw_ear(image, left_start, left_end, transform)
        CatPreset.draw_ear(image, right_start, right_end, transform)

