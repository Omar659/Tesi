# import speech_recognition as sr

# recognizer = sr.Recognizer()

# with sr.Microphone() as source:
#     print("Sto regolando il rumore di fondo...")
#     recognizer.adjust_for_ambient_noise(source, duration=1)

#     print("Parla ora...")
#     audio = recognizer.listen(source)
    
    
# with open("recorded_audio.wav", "wb") as f:
#     f.write(audio.get_wav_data())

# try:
#     text = recognizer.recognize_google(audio, language='it-IT')
#     print("Hai detto: " + text)
# except sr.UnknownValueError:
#     print("Google Web Speech API non ha capito l'audio")
# except sr.RequestError as e:
#     print("Impossibile richiedere i risultati da Google Web Speech API; {0}".format(e))


# Use a pipeline as a high-level helper
# from transformers import pipeline
# import torch

# device = "cuda:0" if torch.cuda.is_available() else "cpu"

# print(device)


# import torch
# from PIL import Image
# from transformers import AutoProcessor, AutoModelForCausalLM 

# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# model = AutoModelForCausalLM.from_pretrained("./Florence-2-base", torch_dtype=torch_dtype, trust_remote_code=True).to(device)
# processor = AutoProcessor.from_pretrained("./Florence-2-base", trust_remote_code=True)

# # url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"

# def run_example(task_prompt, image, text_input=None):
#     if text_input is None:
#         prompt = task_prompt
#     else:
#         prompt = task_prompt + text_input
#     inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)
#     generated_ids = model.generate(
#         input_ids=inputs["input_ids"],
#         pixel_values=inputs["pixel_values"],
#         max_new_tokens=1024,
#         num_beams=3
#     )
#     generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

#     parsed_answer = processor.post_process_generation(generated_text, task=task_prompt, image_size=(image.width, image.height))

#     print(parsed_answer)    
    
# image = Image.open("./../test.jpg")
# prompt = "<MORE_DETAILED_CAPTION>"
# run_example(prompt, image)


import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
# from datasets import load_dataset

with torch.no_grad():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "./whisper-large-v3"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    model.generation_config.language = "<|en|>"
    model.generation_config.task = "transcribe"

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

    # dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
    # sample = dataset[0]["audio"]

    result = pipe("./../test3.m4a")
    print(result["text"])
