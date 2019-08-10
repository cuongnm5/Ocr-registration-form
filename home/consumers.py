from channels.generic.websocket import AsyncJsonWebsocketConsumer
import base64
from .google_api import *
from google.protobuf.json_format import MessageToJson
import json


class ImageConsumer(AsyncJsonWebsocketConsumer):  
    async def receive_json(self, content, **kwargs):
        # print("Receive package", content) 
        b64_text = content['imgstring']
        img = base64.b64decode(b64_text)
        filename = 'some_image.jpg'

        with open(filename, 'wb') as f:
            f.write(img)
            
        api = GoogleAPI()
        ans = api.detect_text(filename)
        # with open('/home/dodo/WorkSpace/Hackathon/OCR-Finance/home/respone.json', 'r') as f:
        #     ans = json.load(f)
        #     ans = ans['responses'][0]['fullTextAnnotation']
        #     ans = json.dumps(ans)

        # await self.send_json(content={
        #     "event": "OCR_response", 
        #     "Text_Description": ans,
        #     "base64":b64_text
        #     })
        await self.send_json(content={
            "event": "OCR_response", 
            "Text_Description": MessageToJson(ans),
            "base64":b64_text
            })