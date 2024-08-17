from flask import request
from flask_restful import Resource
from module_call.stt_recognition import STTRecognizer
from constants import *

class Server_STT(Resource):
    def __init__(self, recognizer):
        self.recognizer = recognizer
        self.req = request.args.get("req")

    def post(self):
        return {"message": "POST request failed", "error": True}

    def get(self):  
        if self.req == GET_LISTEN:
            self.recognizer.listen()
            listened_message = self.recognizer.stt()
            return {"listened_message": listened_message, "error": False}
        return {"message": "GET request failed", "error": True}

    def put(self):
        return {"message": "PUT request failed", "error": True}

    def delete(self):
        return {"message": "DELETE request failed", "error": True}