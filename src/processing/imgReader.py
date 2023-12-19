from PIL import Image
import cv2
from skimage.morphology import skeletonize
import numpy as np


if __name__ == '__main__':
    img = cv2.imread('img/original.jpg', cv2.IMREAD_GRAYSCALE)

    blobs = np.copy(img)
    blobs[blobs<128] = 0
    blobs[blobs>128] = 1
    blobs = blobs.astype(np.uint8)
    skeleton = skeletonize(blobs)
    skeleton = skeleton.astype(np.uint8)*255
    cv2.namedWindow('skeleton', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('skeleton', 1200, 800)
    cv2.imshow('skeleton', skeleton)
    cv2.waitKey()
    cv2.destroyAllWindows()
    cv2.imwrite("skeleton.png", skeleton)

