import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Sto regolando il rumore di fondo...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Parla ora...")
    audio = recognizer.listen(source)
    
    
with open("recorded_audio.wav", "wb") as f:
    f.write(audio.get_wav_data())

# try:
#     text = recognizer.recognize_google(audio, language='it-IT')
#     print("Hai detto: " + text)
# except sr.UnknownValueError:
#     print("Google Web Speech API non ha capito l'audio")
# except sr.RequestError as e:
#     print("Impossibile richiedere i risultati da Google Web Speech API; {0}".format(e))
