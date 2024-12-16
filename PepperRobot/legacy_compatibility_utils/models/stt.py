import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

class WhisperLarge3Call:
    def __init__(self):
        """
        Initializes the WhisperLarge3Call class by loading the model and processor.
        - Determines the device (GPU or CPU) and data type (float16 or float32) based on the availability of CUDA.
        - Loads the model and processor from the specified path.
        - Configures the pipeline for automatic speech recognition (ASR).
        """
        # Set the computation device to GPU if available, otherwise CPU.
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        # Set the data type for torch tensors based on CUDA availability.
        # self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        # # Define the model ID or path to the pre-trained model.
        # self.model_id = "./../whisper-large-v3"

        # # Load the model for speech-to-text using the specified ID and configuration.
        # self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
        #     self.model_id,  # Path or identifier for the pre-trained model.
        #     torch_dtype=self.torch_dtype,  # Set tensor data type to float16 or float32.
        #     low_cpu_mem_usage=True,  # Optimize CPU memory usage during model loading.
        #     use_safetensors=True  # Use safetensors for safe tensor operations.
        # )
        # # Move the model to the designated device (GPU or CPU).
        # self.model.to(self.device)
        # # Configure the model's generation settings for transcription.
        # self.model.generation_config.language = "<|it|>" # Language setting for transcription (empty for auto-detection).
        # self.model.generation_config.task = "transcribe" # Set the task to transcription.

        # # Load the processor, which includes tokenizers and feature extractors.
        # self.processor = AutoProcessor.from_pretrained(self.model_id)

        # # Set up a pipeline for automatic speech recognition (ASR) using the loaded model and processor.
        # self.pipe = pipeline(
        #     "automatic-speech-recognition",  # Task type for the pipeline.
        #     model=self.model,  # Model to use for ASR.
        #     tokenizer=self.processor.tokenizer,  # Tokenizer for processing text data.
        #     feature_extractor=self.processor.feature_extractor,  # Feature extractor for processing audio data.
        #     max_new_tokens=128,  # Maximum number of tokens to generate.
        #     chunk_length_s=30,  # Length of audio chunks to process in seconds.
        #     batch_size=16,  # Number of audio samples to process in each batch.
        #     return_timestamps=True,  # Include timestamps in the output.
        #     torch_dtype=self.torch_dtype,  # Data type for torch tensors.
        #     device=self.device,  # Device to run the model on.
        # )
        
    def stt(self, filepath="./../model_inputs/pepper_listen.wav"):
        """
        Converts speech to text from the provided audio file.

        Parameters:
        - filepath (str): Path to the audio file for transcription.

        Returns:
        - str: The transcribed text from the audio file.
        """
        with torch.no_grad():  # Disable gradient calculation for inference.
            result = self.pipe(filepath)  # Perform speech-to-text on the given file.
            return result["text"]  # Extract and return the transcribed text.