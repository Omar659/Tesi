import speech_recognition as sr
from models.stt import *
from constants import *

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
        # Initialize the WhisperLarge3Call model for converting speech to text.
        self.model = WhisperLarge3Call()
        
    def list_mic():
        """
        List of aveilable microphones printed out.
        """
        # List available microphones
        mic_list = sr.Microphone.list_microphone_names()
        print("Available microphones:", mic_list)
        
    def listen(self, path="./../model_inputs/", filename="pepper_listen.wav", device_index=1, timeout=None, phrase_time_limit=None):
        """
        Listens to audio from the microphone, saves the audio file, and prints status messages.

        Parameters:
        - path (str): The directory path where the audio file will be saved.
        - filename (str): The name of the audio file to save.
        - device_index (int): The index of the microphone to use. Default is 1.
        - timeout (float): The maximum number of seconds that this function will wait for a phrase to start. Default is None.
        - phrase_time_limit (float): The maximum number of seconds that this function will listen for a single phrase. Default is None.
        """
        try:            
            # Use the selected microphone as the audio source.
            with sr.Microphone(device_index=device_index) as source:
                print("Adjusting for ambient noise, please wait...")
                # Adjust the recognizer sensitivity to ambient noise.
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                print("Listening, you may speak now...")
                # Listen to audio from the microphone.
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
                # Save the recorded audio to a file.
                self.save(audio, path, filename)
                print("Audio captured and saved successfully.")
                return OK
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return WAIT_TIMEOUT_ERROR
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return UNKNOWN_VALUE_ERROR
        except sr.RequestError as e:
            print(f"Could not request results from the speech recognition service; {e}")
            return REQUEST_ERROR
        except Exception as e:
            print(f"An error occurred: {e}")
            return GENERIC_ERROR
            
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
        