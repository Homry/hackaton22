import cv2
from processing.convert_video import convert_image

if __name__ == "__main__":
    img = cv2.imread("../test_image.png")
    new_img = convert_image(img)
    if new_img is None:
        print("No face")
        exit(1)
    cv2.imshow("Original", img)
    cv2.imshow("Emotinal", new_img)
    cv2.waitKey(0)
