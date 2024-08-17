import speech_recognition as sr
from models.stt import *

class STTRecognizer:
    def __init__(self):
        """
        Initializes the STTRecognizer class by setting up the speech recognizer and speech-to-text model.
        - Initializes the 'Recognizer' from the speech_recognition library.
        - Creates an instance of the 'WhisperLarge3Call' model for speech-to-text conversion.
        """
        # Initialize the speech recognizer for capturing and processing audio.
        self.recognizer = sr.Recognizer()
        # DECOMMENTARE QUI
        # # Initialize the WhisperLarge3Call model for converting speech to text.
        # self.model = WhisperLarge3Call()
        
    def listen(self, path="./../model_inputs/", filename="pepper_listen.wav"):
        """
        Listens to audio from the microphone, saves the audio file, and prints status messages.

        Parameters:
        - path (str): The directory path where the audio file will be saved.
        - filename (str): The name of the audio file to save.
        """
        # Use the microphone as the audio source.
        with sr.Microphone(device_index=1) as source:
            print("Adjusting for ambient noise...")
            # Adjust the recognizer sensitivity to ambient noise.
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Speak now...")
            # Listen to audio from the microphone.
            audio = self.recognizer.listen(source)
            # Save the recorded audio to a file.
            self.save(audio, path, filename)
            print("Listened")
            
    def save(self, audio, path, filename):
        """
        Saves the audio data to a file.

        Parameters:
        - audio: The audio data to save.
        - path (str): The directory path where the audio file will be saved.
        - filename (str): The name of the audio file to save.
        """
        print("Saving file...")
        # Write the audio data to a WAV file.
        with open(path + filename, "wb") as f:
            f.write(audio.get_wav_data())
        print("File saved")
            
    def stt(self, filepath="./../model_inputs/pepper_listen.wav"):
        """
        Converts speech in the provided audio file to text using the WhisperLarge3Call model.

        Parameters:
        - filepath (str): Path to the audio file to be converted to text.

        Returns:
        - str: The text output from the speech-to-text model.
        """
        # Use the WhisperLarge3Call model to convert the audio file to text.
        return self.model.stt(filepath)
        