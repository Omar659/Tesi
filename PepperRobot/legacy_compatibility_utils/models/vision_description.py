import torch
from transformers import AutoProcessor, AutoModelForCausalLM 
from PIL import Image

class Florence2Call:
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model = AutoModelForCausalLM.from_pretrained("./../Florence-2-base", torch_dtype=self.torch_dtype, trust_remote_code=True).to(self.device)
        self.processor = AutoProcessor.from_pretrained("./../Florence-2-base", trust_remote_code=True)
        
    def run(self, task_prompt="<MORE_DETAILED_CAPTION>", image_path="./../model_inputs/pepper_view.png", text_input=None):
        image = Image.open(image_path)
        with torch.no_grad():
            if text_input is None:
                prompt = task_prompt
            else:
                prompt = task_prompt + text_input
            inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.device, self.torch_dtype)
            generated_ids = self.model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=1024,
                num_beams=3
            )
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
            return self.processor.post_process_generation(generated_text, task=task_prompt, image_size=(image.width, image.height))[task_prompt]