from dataclasses import dataclass
import cv2

@dataclass
class Point:
    x: int
    y: int


class FaceItem:

    def __init__(self, key: str, indecies: list, cycled: bool, tickness: int = 3, draw: bool = True, color: tuple[int, int, int] = (0, 0, 0)):
        self.key = key
        self.mp_indecies = indecies
        self.cycled = cycled
        self.draw = draw
        self.color = color
        self.tickness = tickness
        self.saved_landmarks = []

    def process_landmarks(self, landmarks):
        self.saved_landmarks.clear()
        for index in self.mp_indecies:
            self.saved_landmarks.append(landmarks[index])

    def resize_saved_points(self, transform_func: callable):
        for point in self.saved_landmarks:
            new_x, new_y = transform_func(point)
            point.x = new_x
            point.y = new_y

    def draw_lines(self, image, to_opencv_point: callable):
        if not self.draw:
            return
        last_index = len(self.saved_landmarks)
        if not self.cycled:
            last_index -= 1
        for i in range(last_index):
            pt1 = to_opencv_point(self.saved_landmarks[i])
            pt2 = to_opencv_point(self.saved_landmarks[(i + 1) % len(self.saved_landmarks)])
            cv2.line(image, pt1, pt2, self.color, self.tickness)
