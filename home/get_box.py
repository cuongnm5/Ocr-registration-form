# import the necessary packages
import argparse
import imutils
import cv2
from .google_api import *
from google.protobuf.json_format import MessageToJson
import json
import numpy as np


def getParagraph(block):
    res = []
    paras = block['paragraphs']
    for i in paras:
        para = i
        # print(i['boundingBox'])
        res.append(getWord(para))
    return res
def getWord(para):
    res = []
    words = para['words']
    for i in words:
        word = i
        res.append({'text': getSym(word), 'boundingBox': i['boundingBox']['vertices']})
    return res
def getSym(word):
    res = ''
    symbols = word['symbols']
    for i in symbols:
        res += i['text']
    return res
def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
 
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
 
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
 
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
 
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)
def box_extraction(img_for_box_extraction_path, cropped_dir_path):
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255,
                                    cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255-img_bin  # Invert the image
    # cv2.imwrite("Image_bin.jpg",img_bin)

    # Defining a kernel length
    kernel_length = np.array(img).shape[1]//130
    
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# Morphological operation to detect verticle lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    # cv2.imwrite("verticle_lines.jpg",verticle_lines_img)
# Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    # cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)
# Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# For Debugging
    # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
    cv2.imwrite("img_final_bin.jpg",img_final_bin)
    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort all the contours by top to bottom.
    # print(contours)
    result = []
    checkbox = []
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    idx = 0
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
        if h < 50 and w < 50 and max(w, h)/min(w, h) < 1.2:
            checkbox.append([[x, y], [x + w, y + h]])
        if h > 10:
        # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
            result.append([[x, y], [x+w, y+h]])

    return result, checkbox

def contain_text(thres, paragraphs):
    for parass in paragraphs:
        for paras in parass:
            for para in paras:
                    # print('para: ', para)
                    box = para['boundingBox']
                    if (thres[0][0] - 10 <= box[0]['x'] and thres[1][0] + 10 >= box[2]['x'] and thres[0][1] - 10 <= box[0]['y'] and thres[1][1] + 10 >= box[2]['y']):
                        return thres
    return None
def getPlaceholderBoxAndCoordinate(img_path):
    '''Return 2 value is box contain text, and blank box (box that need to add text to'''
    list_threshold, checkbox = box_extraction(img_path, "")
    api = GoogleAPI()
    ans = api.detect_text(img_path)
    json_res = json.loads(MessageToJson(ans))
    answer = []
    #return list of paragraphs
    paragraphs = []
    blank_box = []
    for para in json_res['pages'][0]['blocks']:
        p = getParagraph(para)
        paragraphs.append(p)
    
    for thres in list_threshold:
        res = contain_text(thres, paragraphs)
        if res != None:
            answer.append(res)
        else:
            blank_box.append(thres)

    return answer, blank_box, checkbox

if __name__ == '__main__':
    text_box, blank_box, checkbox = getPlaceholderBoxAndCoordinate('input9.png')
    # print(text_box)
    img = cv2.imread('input9.png')
    for box in text_box:
        cv2.rectangle(img, tuple(box[0]), tuple(box[1]), (0, 255, 0), 2)
    
    for box in blank_box:
        cv2.rectangle(img, tuple(box[0]), tuple(box[1]), (0, 0, 255), 2)

    for box in checkbox:
        cv2.rectangle(img, tuple(box[0]), tuple(box[1]), (0, 255, 255), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)