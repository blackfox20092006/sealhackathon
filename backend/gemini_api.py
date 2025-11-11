from google import genai
import os
import ast
class GeminiClient:
    def __init__(self, api_key: str = 'AIzaSyBmt2jCVpl9g0Fax1VOObOM9ITDiIklZnM', task: str = None):
        self.api_key = api_key or os.getenv("GENAI_API_KEY")
        try:
            with open(f'./input/gemini_{task}.txt', 'r', encoding='utf-8') as file:
                self.system_prompt = file.read()
        except:
            with open(f'./input/gemini_general.txt', 'r', encoding='utf-8') as file:
                self.system_prompt = file.read()
        if not self.api_key:
            raise ValueError("API key must be provided either as an argument or through the GENAI_API_KEY environment variable.")
        self.client = genai.Client(api_key=self.api_key)

    def generate_text(self, prompt: str) -> list:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", contents=self.system_prompt + prompt
        )
        # try:
        #     task_list = ast.literal_eval(response.text)
        #     if isinstance(task_list, list):
        #         return task_list
        #     else:
        #         return []
        # except Exception as e:
        #     return []
        return response.text
# if __name__ == "__main__":
    # gemini_client1 = GeminiClient('AIzaSyBmt2jCVpl9g0Fax1VOObOM9ITDiIklZnM', task='userstory')
    # gemini_client2 = GeminiClient('AIzaSyBmt2jCVpl9g0Fax1VOObOM9ITDiIklZnM', task='srs')
    # with open('userstory-ex.txt', 'r', encoding='utf-8') as f:
    #     user_story = [i.replace('\n', '') for i in f.readlines()]
    # data = ''
    # for i in user_story:
    #     data += i
    # respond1 = gemini_client1.generate_text(data)

    # with open('SRS-ex.txt', 'r', encoding='utf-8') as f:
    #     srs_data = [i.replace('\n', '') for i in f.readlines()]
    # data = ''
    # for i in srs_data:
    #     data += i
    # respond2 = gemini_client2.generate_text(data)

    # gemini_client3 = GeminiClient('AIzaSyBmt2jCVpl9g0Fax1VOObOM9ITDiIklZnM', task='fusion1')
    # gemini_client4 = GeminiClient('AIzaSyBmt2jCVpl9g0Fax1VOObOM9ITDiIklZnM', task='fusion2')

    # # respond3 = gemini_client3.generate_text(
    # #     f'Here is the user story: {respond1} Here is the SRS: {respond2}'
    # # )
    # # print(respond3)
    # respond4 = gemini_client4.generate_text(
    #     f'Here is the user story: {respond1} Here is the SRS: {respond2}'
    # )
    # print(respond4) 
