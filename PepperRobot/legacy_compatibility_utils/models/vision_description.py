import torch
from transformers import AutoProcessor, AutoModelForCausalLM 
from PIL import Image

class Florence2Call:
    def __init__(self):
        """
        Initializes the Florence2Call class by setting up the device and model/processor.
        - Determines the computation device (GPU or CPU).
        - Currently commented out: model and processor loading.
        """
        # Set the computation device to GPU if available; otherwise, use CPU.
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        # Set the tensor data type to float16 for GPU or float32 for CPU.
        # self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        # # DECOMMENTARE QUI
        # # Load the pre-trained model for causal language modeling.
        # # The model and processor are loaded from the specified path and moved to the appropriate device.
        # self.model = AutoModelForCausalLM.from_pretrained(
        #     "./../Florence-2-base",  # Path to the pre-trained model directory.
        #     torch_dtype=self.torch_dtype,  # Set tensor data type to float16 or float32.
        #     trust_remote_code=True  # Trust code from the remote repository.
        # ).to(self.device)  # Move the model to the specified device (GPU or CPU).
        

        # # Load the processor associated with the pre-trained model.
        # self.processor = AutoProcessor.from_pretrained(
        #     "./../Florence-2-base",  # Path to the pre-trained processor directory.
        #     trust_remote_code=True  # Trust code from the remote repository.
        # )
        
    def run(self, task_prompt="<MORE_DETAILED_CAPTION>", image_path="./../model_inputs/pepper_view.png", text_input=None):
        """
        Runs the model inference to generate text based on the image and prompt provided.

        Parameters:
        - task_prompt (str): The prompt describing the task or the type of caption to generate.
        - image_path (str): Path to the image file that will be processed.
        - text_input (str or None): Optional additional text input to be appended to the prompt.

        Returns:
        - str: The generated caption or text based on the image and prompt.
        """
        # Open the image file using PIL (Python Imaging Library).
        # image = Image.open(image_path)
        
        # with torch.no_grad():  # Disable gradient computation during inference to save memory and computation.
        #     # Combine the task prompt with the optional text input if provided.
        #     if text_input is None:
        #         prompt = task_prompt
        #     else:
        #         prompt = task_prompt + text_input
                
        #     # Process the prompt and image using the processor.
        #     # Convert the text prompt and image into tensors suitable for the model.
        #     inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.device, self.torch_dtype)
            
        #     # Generate text using the model with the processed inputs.
        #     # Set generation parameters such as maximum tokens and beam search.
        #     generated_ids = self.model.generate(
        #         input_ids=inputs["input_ids"],
        #         pixel_values=inputs["pixel_values"],
        #         max_new_tokens=1024,
        #         num_beams=3
        #     )
            
        #     # Decode the generated IDs into text and post-process the result.
        #     generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        #     return self.processor.post_process_generation(
        #         generated_text,  # The raw generated text.
        #         task=task_prompt,  # Task prompt used for post-processing.
        #         image_size=(image.width, image.height)  # Size of the image to be used in post-processing.
        #     )[task_prompt]  # Return the post-processed result corresponding to the task prompt.
        return ""