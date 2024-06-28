import os
from typing import Dict, List, Optional, Tuple, Union
from zhipuai import ZhipuAI
from web.configs import ZhipuAI_API_KEY,DASH_SCOPE_KEY
import torch
from modelscope import AutoTokenizer, AutoModelForCausalLM
import dashscope
import random
from http import HTTPStatus
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0

PROMPT_TEMPLATE = dict(
    RAG_PROMPT_TEMPALTE="""使用以上下文来回答用户的问题。如果你不知道答案，就说你不知道。总是使用中文回答。
        问题: {question}
        可参考的上下文：
        ···
        {context}
        ···
        如果给定的上下文无法让你做出回答，请回答数据库中没有这个内容，你不知道。
        有用的回答:""",
    InternLM_PROMPT_TEMPALTE="""先对上下文进行内容总结,再使用上下文来回答用户的问题。如果你不知道答案，就说你不知道。总是使用中文回答。
        问题: {question}
        可参考的上下文：
        ···
        {context}
        ···
        如果给定的上下文无法让你做出回答，请回答数据库中没有这个内容，你不知道。
        有用的回答:"""
)


class BaseModel:
    def __init__(self, path: str = '') -> None:
        self.path = path

    def chat(self, prompt: str, history: List[dict], content: str) -> str:
        pass

    def load_model(self):
        pass

class GLM4Chat(BaseModel):
    def __init__(self, path: str = '', model: str = "glm-4") -> None:
        super().__init__(path)
        self.model = model

    def chat(self, prompt: str, history: List[dict], content: str) -> str:
        client = ZhipuAI(api_key=os.getenv(ZhipuAI_API_KEY))  # 填写您自己的APIKey
        history.append({'role': 'user', 'content': PROMPT_TEMPLATE['RAG_PROMPT_TEMPALTE'].format(question=prompt, context=content)})
        response = client.chat.completions.create(
            model="glm-4",  #填写需要调用的模型名称
            messages=history
        )
        return response.choices[0].message

class QwenChat(BaseModel):
    def __init__(self, path: str = '', model: str = "qwen-turbo") -> None:
        super().__init__(path)
        dashscope.api_key = DASH_SCOPE_KEY
        self.model = model
    def chat(self, prompt: str, history: List[dict], content: str) -> str:
        history.append({'role': 'user', 'content': PROMPT_TEMPLATE['RAG_PROMPT_TEMPALTE'].format(question=prompt, context=content)})
        response = Generation.call(model="qwen-turbo",
                                messages=history,
                                # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                                seed=random.randint(1, 10000),
                                # 将输出设置为"message"格式
                                result_format='message')
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message["content"]
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))


class OpenAIChat(BaseModel):
    def __init__(self, path: str = '', model: str = "gpt-3.5-turbo-1106") -> None:
        super().__init__(path)
        self.model = model

    def chat(self, prompt: str, history: List[dict], content: str) -> str:
        from openai import OpenAI
        client = OpenAI()   
        history.append({'role': 'user', 'content': PROMPT_TEMPLATE['RAG_PROMPT_TEMPALTE'].format(question=prompt, context=content)})
        response = client.chat.completions.create(
            model=self.model,
            messages=history,
            max_tokens=150,
            temperature=0.1
        )
        return response.choices[0].message.content

class LocalModelChat(BaseModel):
    def __init__(self, path: str = '') -> None:
        super().__init__(path)
        self.load_model()

    def chat(self, prompt: str, history: List = [], content: str='') -> str:
        prompt = PROMPT_TEMPLATE['InternLM_PROMPT_TEMPALTE'].format(question=prompt, context=content)
        response, history = self.model.chat(self.tokenizer, prompt, history)
        return response
    
    def load_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.path, torch_dtype=torch.float16, trust_remote_code=True).cuda()