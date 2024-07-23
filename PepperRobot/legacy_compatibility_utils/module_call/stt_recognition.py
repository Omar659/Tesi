import speech_recognition as sr

class STTRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def listen(self, path="./../model_inputs/", filename="pepper_listen.wav"):
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Speak now...")
            audio = self.recognizer.listen(source)
            self.save(audio, path, filename)
            
    def save(self, audio, path, filename):
        with open(path + filename, "wb") as f:
            f.write(audio.get_wav_data())