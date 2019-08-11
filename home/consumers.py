from channels.generic.websocket import AsyncJsonWebsocketConsumer
import base64
from .google_api import *
from google.protobuf.json_format import MessageToJson
import json
from.get_threshold import *
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
        # img = cv2.imread(filename)

        await self.send_json(content={
            "event": "OCR_response",
            "Question": json.dumps(res),
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
            cv2.putText(img, inp, tuple(q['coordinate'][0]), font, 0.5, (0, 0, 0), 1)
            i+=1
            cv2.imwrite('filled_image.png', img)

        encoded_string = None
        with open("filled_image.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        # print(encoded_string)

        await self.send_json(content = {
            'imgstring': str(encoded_string),
        })
        
