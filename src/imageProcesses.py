from cv2 import *
import base64
import numpy as np
import datetime
from PIL import Image

def convertToPNG(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    image = Image.fromarray(img)
    image = image.convert("RGBA")
    datas = image.getdata()
    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 255 and item[2] == 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    image.putdata(newData)
    path = "./TransparentImage.png"
    image.save(path, "PNG") #converted Image name
    return path

def bgRemover(img):
    BLUR = 1
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 50
    MASK_DILATE_ITER = 15
    MASK_ERODE_ITER = 5
    MASK_COLOR = (0,1,0)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))

    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    mask = np.zeros(edges.shape)

    cv2.fillConvexPoly(mask, max_contour[0], (255))
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask] * 3)
    mask_stack = mask_stack.astype('float32') / 255.0
    img = img.astype('float32') / 255.0
    masked = (mask_stack * img) + ((1 - mask_stack) * MASK_COLOR)
    masked = (masked * 255).astype('uint8')

    cv2.imshow('img', masked)

    return convertToPNG(masked)

def openImage(imageBase64):

    decoded_data = base64.b64decode(imageBase64)
    np_data = np.fromstring(decoded_data,np.uint8)
    img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
    return bgRemover(img)

def encodeImage(data):
    data_string = base64.b64encode(data.read())
    return data_string
