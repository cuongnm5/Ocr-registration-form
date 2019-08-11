from channels.generic.websocket import AsyncJsonWebsocketConsumer
import base64
from .google_api import *
from google.protobuf.json_format import MessageToJson
import json
from.get_threshold import *

class ImageConsumer(AsyncJsonWebsocketConsumer):  
    async def receive_json(self, content, **kwargs):
        # print("Receive package", content) 
        b64_text = content['imgstring']
        img = base64.b64decode(b64_text)
        filename = 'input2.png'
        res = getPlaceholderTextAndCoordinate(filename)
        img = cv2.imread(filename)

        await self.send_json(content={
            "event": "OCR_response",
            "Question": json.dumps(res),
            "base64":b64_text,
        })