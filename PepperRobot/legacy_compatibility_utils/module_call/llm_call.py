import openai
from openai import OpenAI
import json

class LlmCaller:
    def __init__(self):
        self.client = self.__get_client()
        
    def __get_client(self):
        with open("./token.json", 'r', encoding='utf-8') as file:
            data = json.load(file)

        client = openai.OpenAI(
            api_key= data["api_key"],
            base_url=data["base_url"],
        )
        return client
    
    def get_answer(self, system_prompt, user_prompt, model="codellama/CodeLlama-34b-Instruct-hf", max_tokens=512):
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ]
        
        code_completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens,
            stop=[
                "<step>"
            ],
            frequency_penalty=1,
            presence_penalty=1,
            top_p=0.7
        )
        
        return code_completion.choices[0].message.content