from flask import request
from flask_restful import Resource
from module_call.stt_recognition import STTRecognizer
from constants import *

class Server_STT(Resource):
    def __init__(self, recognizer):
        """
        Initializes the Server_STT class by setting up the STT recognizer.

        Parameters:
        - 'recognizer': An instance of the STTRecognizer class used for speech-to-text operations.
        """
        self.recognizer = recognizer
        
        # Retrieve the 'req' parameter from the request URL.
        self.req = request.args.get("req")

    def post(self):
        """
        Handles POST requests by processing different types of requests based on the 'req' parameter.
        """
        return {"message": "POST request failed", "error": True}

    def get(self):  
        """
        Handles GET requests by processing different types of requests based on the 'req' parameter.
        """
        if self.req == GET_LISTEN:
            # Calls listen to record audio, then stt to convert it to text, and returns the result.
            self.recognizer.listen()
            listened_message = self.recognizer.stt()
            return {"listened_message": listened_message, "error": False}
        return {"message": "GET request failed", "error": True}

    def put(self):
        """
        Handles PUT requests by processing different types of requests based on the 'req' parameter.
        """
        return {"message": "PUT request failed", "error": True}

    def delete(self):
        """
        Handles DELETE requests by processing different types of requests based on the 'req' parameter.
        """
        return {"message": "DELETE request failed", "error": True}