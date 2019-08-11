# import the necessary packages
import argparse
import imutils
import cv2
from .google_api import *
from google.protobuf.json_format import MessageToJson
import json


def getParagraph(block):
    res = []
    paras = block['paragraphs']
    for i in paras:
        para = i
        # print(i['boundingBox'])
        res.append({'text': getWord(para), 'boundingBox': i['boundingBox']['vertices']})
    return res

def getWord(para):
    res = ''
    words = para['words']
    for i in words:
        word = i
        res += getSym(word) + ' '
    return res

def getSym(word):
    res = ''
    symbols = word['symbols']
    for i in symbols:
        res += i['text']
    return res


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

        # return the name of the shape
        return shape
        
def getThresholdCoordinate(img_path):
    # construct the argument parse and parse the arguments
    img = cv2.imread(img_path, 0)

    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # Thresholding the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    # Invert the image
    img_bin = 255-img_bin

    # Defining a kernel length
    kernel_length = 15#np.array(img).shape[1]//80
    
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Morphological operation to detect vertical lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    # cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)
    #........................................................


    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    image = cv2.cvtColor(horizontal_lines_img, cv2.COLOR_GRAY2RGB)
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])
    
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)[1]
    
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    # print(sd)
    list_threshold = []
    for i in range(len(cnts)):
        c = cnts[i]
        minx = 100000
        miny = 100000
        maxx = -1
        maxy = -1
        for coor in c:
            coordinate = coor[0]
            miny = int(min(coordinate[0] * ratio, miny))
            maxy = int(max(coordinate[0] * ratio, maxy))
            minx = int(min(coordinate[1] * ratio, minx))
            maxx = int(max(coordinate[1] * ratio, maxx))
        cv2.rectangle(image, (miny, minx), (maxy, maxx), (0, 255, 0), 2)
        list_threshold.append([[miny, minx], [maxy, maxx]])
    return list_threshold

def is_threshold(text_obj, list_threshold):
    # print(text_obj['boundingBox'])
    for thres in list_threshold:
        # print(thres)
        y = (thres[0][1] + thres[1][1]) / 2
        x = thres[0][0]
        if (y >= text_obj['boundingBox'][1]['y'] and y <= text_obj['boundingBox'][2]['y']) and (x <= text_obj['boundingBox'][1]['x'] + 20):
            return thres
    return None

def getPlaceholderTextAndCoordinate(img_path):
    
    list_threshold = getThresholdCoordinate(img_path)
    api = GoogleAPI()
    ans = api.detect_text(img_path)
    json_res = json.loads(MessageToJson(ans))
    answer = []
    # print(json_res['pages'][0]['blocks'])
    for para in json_res['pages'][0]['blocks']:
        paras = getParagraph(para)
        for par in paras:
            res = is_threshold(par, list_threshold)
            if (res != None):
                answer.append({'text': par['text'], 'coordinate': res})
            # print(getParagraph(par)[0]['text'], ': ', res)
    # print(json.loads(MessageToJson(ans))['text'])
    return answer


if __name__ == '__main__':
    res = getPlaceholderTextAndCoordinate('input2.png')
    img = cv2.imread('input2.png')

    for q in res:
        print(q['text'], ':')
        inp = input()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, inp, tuple(q['coordinate'][0]), font, 0.5, (0, 0, 0), 1)

    cv2.imshow('img', img)
    cv2.waitKey(0)
