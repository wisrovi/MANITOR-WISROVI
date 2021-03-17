import cv2
import numpy as np


def ColorAzul():
    black_screen = np.zeros([500, 500, 3], dtype=np.uint8)

    black_screen[:, :, 0] = np.ones([500, 500]) * 255
    black_screen[:, :, 1] = np.ones([500, 500]) * 0
    black_screen[:, :, 2] = np.ones([500, 500]) * 0

    return black_screen


def ColorRojo():
    black_screen = np.zeros([500, 500, 3], dtype=np.uint8)

    black_screen[:, :, 0] = np.ones([500, 500]) * 0
    black_screen[:, :, 1] = np.ones([500, 500]) * 0
    black_screen[:, :, 2] = np.ones([500, 500]) * 255

    return black_screen


fondo_base = True


def back(*args):
    global fondo_base
    if fondo_base:
        fondo_base = False
    else:
        fondo_base = True
    pass


cv2.namedWindow("Frame")
cv2.createButton("Cahnge Color", back)

while True:
    fondo = ColorAzul() if fondo_base else ColorRojo()

    cv2.imshow('Frame', fondo)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
