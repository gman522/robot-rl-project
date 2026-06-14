import cv2
import numpy as np


def detect_walls(frame):

    h, w, _ = frame.shape

    left = frame[:, 0:w//3]
    center = frame[:, w//3:2*w//3]
    right = frame[:, 2*w//3:w]

    def is_wall(region):

        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

        dark_pixels = np.sum(gray < 80)
        total = region.shape[0] * region.shape[1]

        ratio = dark_pixels / total

        return ratio > 0.15  # umbral ajustable

    return (
        int(is_wall(left)),
        int(is_wall(center)),
        int(is_wall(right))
    )