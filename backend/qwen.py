from google import genai
import os
import ast
import dotenv
import pathlib
import os
from openai import OpenAI
class QwenClient:
    def __init__(self, api_key: str = None, system_prompt_file: str = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.client = OpenAI(
            # The API keys for the Singapore and China (Beijing) regions are different. To obtain an API key, see https://modelstudio.console.alibabacloud.com/?tab=model#/api-key
            # If you have not configured an environment variable, replace the following line with your Model Studio API key: api_key="sk-xxx",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            # The following URL is for the Singapore region. If you use a model in the China (Beijing) region, replace the URL with: https://dashscope.aliyuncs.com/compatible-mode/v1
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
        # Load system prompt if file path is provided
        self.system_prompt = ""
        if system_prompt_file and os.path.exists(system_prompt_file):
            with open(system_prompt_file, 'r', encoding='utf-8') as file:
                self.system_prompt = file.read()
        
        if not self.api_key:
            raise ValueError("API key must be provided either as an argument or through the GENAI_API_KEY environment variable.")
        self.client = genai.Client(api_key=self.api_key)

    def generate_text(self, prompt: str) -> list:
        completion = self.client.chat.completions.create(
            model="Qwen3-Max",
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        try:
            task_list = ast.literal_eval(completion.choices[0].message.content)
            if isinstance(task_list, list):
                return task_list
            else:
                return []
        except Exception as e:
            return []
if __name__ == "__main__":
    system_prompt_user_story = './input/gemini.txt'
    system_prompt_SRS = './input/SRS.txt'
    
    # Test 1: với system_prompt_user_story
    gemini_client = QwenClient('', system_prompt_file=system_prompt_user_story)
    prompt_user_story = "I want to create a quantum computing application that can solve complex optimization problems, buy me a coffee, or even robe the bank"
    generated_text_user_story = gemini_client.generate_text(prompt_user_story)
    
    # Test 2: với system_prompt_SRS (khởi tạo lại client với system prompt khác)
    gemini_client = QwenClient('', system_prompt_file=system_prompt_SRS)
    prompt_SRS = "List my to-do list"
    generated_text_SRS = gemini_client.generate_text(prompt_SRS)
    
    print("Ans SRS:", generated_text_SRS)
    print("Ans list:", generated_text_user_story)