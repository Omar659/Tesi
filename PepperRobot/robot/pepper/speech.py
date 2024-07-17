class Speech:
    def __init__(self, app):
        self.app = app
        self.tts = self.app.session.service("ALTextToSpeech")
        
    def say(self, text, language="Italian"):
        self.tts.setLanguage(language)
        print("Pepper: " + text)
        self.tts.say(text)