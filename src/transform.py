import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
import os 

def transform(imgPath:str, debug=False):
    '''
        将图片中的轮廓旋转摆正, 并平移到图片中心。

        Args:
            - `imgPath`: input img path.

        Return:
            - `centerImg`: image of transform img to center.
            - `crop`: crop rect of centerImg. 
    '''

    ## img load
    img = cv2.imread(imgPath, 0)
    edges = cv2.Canny(img, 50, 150)

    ## 霍夫叶变换
    transImg = np.fft.fft2(edges)
    shift = np.fft.fftshift(transImg)
    magnitude = np.log(np.abs(shift)+1)
    magnitude = magnitude.astype(np.uint8)

    ## 二值化图片获取直线
    thresh = cv2.threshold(magnitude, 12, 255, cv2.THRESH_BINARY)[1]

    imgLine = np.ones(thresh.shape, dtype=np.uint8)*255

    ## 取值范围：`200` 效果最好
    lines = cv2.HoughLinesP(thresh, 2, np.pi/180, 200, minLineLength=40, maxLineGap=100)
    piThresh = np.pi/180
    pi2 = np.pi/2

    ## 画线
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(imgLine, (x1, y1), (x2, y2), (0, 255, 0), 2)
        if x2 - x1 == 0:
            continue
        else:
            theta = (y2 - y1) / (x2 - x1)
        # if abs(theta) < piThresh or abs(theta - pi2) < piThresh:
        #     continue
        # else:
        #     print(theta)
    

    ## 获取旋转角度
    h,w = img.shape[:2]         
    angle = math.atan(theta)
    # print('angle:',angle)
    angle = angle * (180 / np.pi)
    # print('angle:',angle)
    angle = (angle - 90)/(w/h)
    # print('angle:',angle)

    ## 通过旋转角度进行旋转
    center = (w// 2, h// 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    rectImg = np.copy(rotated)

    ## 膨胀轮廓方便找到最大外接矩形
    kernel = np.ones((15,15), np.uint8)
    dilated = cv2.dilate(rectImg, kernel, iterations=1)

    ## 获取物体轮廓,找到最大外接矩形
    contours = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    
    x2,y2,w2,h2 = cv2.boundingRect(max(contours, key=cv2.contourArea)) # x,y,w,h
    cv2.rectangle(rectImg, (x2, y2), (x2+w2, y2+h2), (255, 255, 255), 2)
    
    # print(x2,y2,w2,h2)
    centerRect = (x2 + w2//2, y2 + h2//2)
    # print(center,centerRect)
    
    ## 平移到图片中心点
    M2 = np.float32([[1,0,center[0]-centerRect[0]], [0,1,center[1]-centerRect[1]]])
    centerImg = cv2.warpAffine(rotated, M2, (w,h))
    dilated = cv2.dilate(centerImg, kernel, iterations=1)
    contours = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    x2,y2,w2,h2 = cv2.boundingRect(max(contours, key=cv2.contourArea)) # x,y,w,h
    crop = centerImg[y2:y2+h2, x2:x2+w2]
    if debug:
        # cv2.drawContours(rectImg, max(contours, key=cv2.contourArea), -1, (255, 255, 255), 2)
        debugPath = 'debug/'
        os.makedirs(debugPath, exist_ok=True)
        cv2.imwrite(debugPath + 'magnitude.png',thresh)
        cv2.imwrite(debugPath + 'line.png', imgLine)
        cv2.imwrite(debugPath + 'rect.png',rectImg)
        cv2.imwrite(debugPath + 'center.png',centerImg)
        cv2.imwrite(debugPath + 'crop.png',crop)

    return centerImg, crop



def connectLine(imgPath:str, savePath:str, cropImg=False, debug=False) -> None:
    '''
        将图中物体的外观线画出来。通过二值化, 收缩膨胀, 闭运算, 将线段连接成一个整体后画出轮廓。
        - `mergeLine`: 在原图上画出轮廓线
        - `outLine`: 在白色背景新图中画出轮廓线

        Args:
            - `imgPath`: input img path.
            - `savePath`: result img path.

        Return:
            - None
    '''
    img, crop = transform(imgPath, debug=debug)
    if cropImg:
        img = crop

    thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
    blur = cv2.blur(thresh,(5,5))
    dst = cv2.equalizeHist(blur)
    gaussian = cv2.GaussianBlur(dst, (5,5),0)
    kernel = np.ones((5,5), np.uint8)
    eroded = cv2.erode(gaussian, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, iterations=7)
    thresh = cv2.threshold(closing, 50, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL,  cv2.CHAIN_APPROX_SIMPLE)[0]

    bgrImg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    blackImg = np.ones((img.shape[0],img.shape[1],3), dtype=np.uint8)*255
    cv2.drawContours(bgrImg, contours, -1, (0,128,255), 3)
    cv2.drawContours(blackImg, contours, -1, (0,128,255), 3)
    os.makedirs(savePath, exist_ok=True)
    cv2.imwrite(savePath + 'mergeLine.png', bgrImg)
    cv2.imwrite(savePath + 'outLine.png', blackImg)
    
if __name__ == "__main__":
    imgPath = 'img/img2.jpg'
    savePath = 'result/'

    connectLine(imgPath, savePath, cropImg=False, debug=True)
 