from channels.generic.websocket import AsyncJsonWebsocketConsumer
import base64
from .google_api import *
from google.protobuf.json_format import MessageToJson
import json
from .get_threshold import *
from .get_box import *
import cv2

class ImageConsumer(AsyncJsonWebsocketConsumer):  
    async def receive_json(self, content, **kwargs):
        # print("Receive package", content) 
        b64_text = content['imgstring']
        img = base64.b64decode(b64_text)
        filename = 'some_image.jpg'
        with open(filename, 'wb') as f:
            f.write(img)
        res = getPlaceholderTextAndCoordinate(filename)

        text_box, blank_box, checkbox = getPlaceholderBoxAndCoordinate(filename)
        img = cv2.imread(filename)
        i=1
        for box in blank_box:
            cv2.rectangle(img, tuple(box[0]), tuple(box[1]), (0, 0, 255), 2)
            cv2.putText(img,str(i), (int((box[0][0]+box[1][0])/2),int((box[0][1]+box[1][1])/2) ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2 )
            i+=1
            
        img = cv2.imwrite('result_image.jpg', img)
        
        # encoded_string = None
        # with open("result_image.jpg", "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read())

        await self.send_json(content={
            "event": "OCR_response",
            "Question": json.dumps(res),
            # "base64":str(encoded_string),
            "base64":b64_text,
        })

class InfoConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content, **kwargs):
        info = content['infomation']
        info = json.loads(info)
        filename = 'some_image.jpg'
        res  = getPlaceholderTextAndCoordinate(filename)
        print(res)
        img = cv2.imread(filename)
        i = 0
        # print(info.items())
        for key, value in info.items():
            if (key == ''):
                break
            inp = value
            font = cv2.FONT_HERSHEY_SIMPLEX
            q = res[i]
            cv2.putText(img, inp, tuple([q['boundingBox'][0]['x'], q['boundingBox'][0]['y']]), font, 0.5, (0, 0, 0), 1)
            i+=1
            cv2.imwrite('home/static/images/filled_image.png', img)
        
