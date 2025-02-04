from flask import request
from flask_restful import Resource
from constants import *

class Server_STT(Resource):
    def __init__(self):#, recognizer):
        """
        Initializes the Server_STT class by setting up the STT recognizer.

        Parameters:
        - 'recognizer': An instance of the STTRecognizer class used for speech-to-text operations.
        """
        # self.recognizer = recognizer
        
        # Retrieve the 'req' parameter from the request URL.
        self.req = request.args.get("req")
        self.timeout = request.args.get("timeout", default=None)

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
            # Calls the 'listen' method of the recognizer to record audio.
            timeout = self.timeout
            if self.timeout is not None:
                timeout = int(self.timeout)
            listen_status = whisper.listen(device_index=0, timeout=timeout) # device_index: 1 pc lab; 2 my pc
            
            # Check the status returned by the 'listen' method to determine the next step.
            if listen_status == OK:
                # If listening is successful (status is OK), convert the recorded audio to text.
                listened_message = whisper.stt()
                # Return the transcribed text along with an error OK.
                return {"listened_message": listened_message, "error": OK}
            elif listen_status == WAIT_TIMEOUT_ERROR:
                # If a timeout error occurred during listening, return an empty message and the corresponding error code.
                return {"listened_message": "", "error": WAIT_TIMEOUT_ERROR}
            elif listen_status == UNKNOWN_VALUE_ERROR:
                # If the system couldn't understand the audio, return an empty message and the corresponding error code.
                return {"listened_message": "", "error": UNKNOWN_VALUE_ERROR}
            elif listen_status == REQUEST_ERROR:
                # If there was an issue with the request to the speech recognition service, return an empty message and the corresponding error code.
                return {"listened_message": "", "error": REQUEST_ERROR}
            elif listen_status == GENERIC_ERROR:
                # If a generic error occurred, return an empty message and the corresponding error code.
                return {"listened_message": "", "error": GENERIC_ERROR}
            
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