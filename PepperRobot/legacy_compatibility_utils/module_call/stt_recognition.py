import speech_recognition as sr
from models.stt import *

class STTRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # self.model = WhisperLarge3Call()
        
    def listen(self, path="./../model_inputs/", filename="pepper_listen.wav"):
        with sr.Microphone(device_index=1) as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Speak now...")
            audio = self.recognizer.listen(source)
            self.save(audio, path, filename)
            print("Listened")
            
    def save(self, audio, path, filename):
        print("Saving file...")
        with open(path + filename, "wb") as f:
            f.write(audio.get_wav_data())
        print("File saved")
            
    def stt(self, filepath="./../model_inputs/pepper_listen.wav"):
        return self.model.stt(filepath)
        