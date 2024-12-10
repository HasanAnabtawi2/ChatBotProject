import json
import os
import ssl
from typing import List
import urllib
from dotenv import load_dotenv
from DTOs.PromptDTO import PromptDTO, PromptMessagesDTO
from Services.VectorDatabaseService import VectorDatabaseService













class LlmService:

    def __init__(self):
        self.allowSelfSignedHttps(True)

    def gpt(self, messages: list, temperature = None) -> str:
        if temperature is None:
            temperature = 0
        load_dotenv()
        data = {
            "messages":messages,
            "max_tokens": 5000,
            "temperature": temperature,
            "top_p": 0.95
        }

        body = str.encode(json.dumps(data))

        url = os.getenv("llama_endpoint") + '/v1/chat/completions'

        api_key = os.getenv("llama_key")

        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        headers = {'Content-Type': 'application/json',
                   'Authorization': ('Bearer ' + api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            json_string = result.decode('utf-8')
            answer = json.loads(json_string)

            return answer['choices'][0]['message']['content']

        except urllib.error.HTTPError as error:
            raise Exception("The request failed with status code: " + str(error.code))

    def allowSelfSignedHttps(self, allowed):
      if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
          ssl._create_default_https_context = ssl._create_unverified_context


    
    def rag_llm_call(self,prompt:PromptMessagesDTO,documents):


        


        system_prompt=f'''You are a helpful C# teacher. The user will ask questions about C# \
                            and you must answer the question from the reference \
                         documents provided to you with answer dpending on it. \

                        - Your task is to answer these questions based on the information contained in \
                              the provided documents. 
                        - Return your answers in plain text format.\
                        - if the question in another language like arabic, answer in the question language
                
                        - The reference documents are: {documents["documents"]}.
                        -if the question not related to provided documents, reply with : "The question not related to C#"
                       '''

        context=[
            {
                'role':'system',
                'content': system_prompt
            }
            
        ]
        for p in prompt:

            context.append(p)
      
        response =  self.gpt(context)
        

        return response