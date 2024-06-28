import pydantic
from pydantic import BaseModel
from typing import List, Dict


class BaseRequest(BaseModel):
    app_id: str = pydantic.Field('')
    sign: str = pydantic.Field('')
    path: str = pydantic.Field('')
    timestamp: int = pydantic.Field(None)
    
class SearchRequest(BaseModel):
    question: str = pydantic.Field("", description="获取答案")
    

class UserRequest(BaseRequest):
    user_id: str = pydantic.Field("", description="用户ID")
    k: int = pydantic.Field(5, description="")


class ServiceRequest(BaseRequest):
    ids: List[str] = pydantic.Field([], description="权限")


class AnalysisRequest(BaseRequest):
    user_id: str = pydantic.Field("", description="用户ID")
    question: str = pydantic.Field("", description="问题")
    history: List[Dict] = pydantic.Field(None, description="")
    partitions: List[str] = pydantic.Field(["_default"], description="")


class AnalysisDocumentRequest(BaseRequest):
    user_id: str = pydantic.Field("", description="用户ID")
    question: str = pydantic.Field("", description="问题")
    partitions: List[str] = pydantic.Field(["_default"], description="")


class ContentRequest(BaseRequest):
    content: str = pydantic.Field("", description="内容")
    filename: str = pydantic.Field("", description="文件名")
    partition: str = pydantic.Field(..., description="分区名")


class AnalyzeFAQRequest(AnalysisDocumentRequest):
    num: int = pydantic.Field(10, description="FAQ数量")


class FAQRequest(BaseRequest):
    question: str = pydantic.Field("", description="问题")
    answer: str = pydantic.Field("", description="答案")
    partition: str = pydantic.Field(..., description="分区名")


class AnswerGenRequest(BaseRequest):
    user_id: str = pydantic.Field("", description="用户ID")
    document: str = pydantic.Field("", description="文档")
    num: int = pydantic.Field(10, description="生成数量")


class AgentRequest(BaseRequest):
    user_id: str = pydantic.Field("", description="用户ID")
    prompt: str = pydantic.Field("", description="一句话提示词")
