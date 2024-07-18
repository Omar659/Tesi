import speech_recognition as sr

class STTRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def listen(self, language = "it-IT"): # "en-US"
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Speak now...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language=language)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API; {0}".format(e))