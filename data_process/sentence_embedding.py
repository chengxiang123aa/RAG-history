import os
from copy import copy
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from zhipuai import ZhipuAI
from dotenv import load_dotenv, find_dotenv
from web.configs import ZhipuAI_API_KEY

_ = load_dotenv(find_dotenv())

class BaseEmbeddings:
    """
    Base class for embeddings
    """
    def __init__(self, path: str, is_api: bool) -> None:
        self.path = path
        self.is_api = is_api
    
    def get_embedding(self, text: str, model: str) -> List[float]:
        raise NotImplementedError

    def get_embeddings(self, text: List[str], model: str) -> List[List[float]]:
        raise NotImplementedError
    
    @classmethod
    def cosine_similarity(cls, vector1: List[float], vector2: List[float]) -> float:
        """
        calculate cosine similarity between two vectors
        """
        dot_product = np.dot(vector1, vector2)
        magnitude = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        if not magnitude:
            return 0
        return dot_product / magnitude
    
class ZhipuEmbedding(BaseEmbeddings):
    """
    class for Zhipu embeddings
    """
    def __init__(self, path: str = '', is_api: bool = True, embedding_dim = 1024) -> None:
        super().__init__(path, is_api)
        if self.is_api:
            self.client = ZhipuAI(api_key=ZhipuAI_API_KEY) 
        self.embedding_dim = embedding_dim


    def get_embedding(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
        model="embedding-2",
        input=text,
        )
        return response.data[0].embedding