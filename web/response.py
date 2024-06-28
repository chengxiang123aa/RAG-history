import pydantic
from pydantic import BaseModel
from typing import List, Optional


class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="HTTP status code")
    msg: str = pydantic.Field("success", description="HTTP status message")


class FileResponse(BaseResponse):
    filenames: List = pydantic.Field(..., description="")
    contents: List = pydantic.Field(...)


class AnalysisResponse(BaseResponse):
    response: str = pydantic.Field(..., description="模型返回结果")
    knowledge: str = pydantic.Field("", description="搜索的知识")


class AnalysisMilvusResponse(AnalysisResponse):
    filename: str = pydantic.Field(..., description="模型返回结果")


class AnalyzeFAQResponse(BaseResponse):
    response: str = pydantic.Field(..., description="搜索返回结果")
    recommend: list = pydantic.Field([], description="推荐的问题")


class ContentResponse(BaseResponse):
    response: str = pydantic.Field(..., description="模型返回结果")
    knowledge: str = pydantic.Field("", description="搜索的知识")


class PartitionsListResponse(BaseResponse):
    partitions: List = pydantic.Field(..., description="模型返回结果")


class AnswerGenResponse(BaseResponse):
    response: list = pydantic.Field(..., description="模型返回结果")


class AgentResponse(BaseResponse):
    prompt: str = pydantic.Field(..., description="模型返回结果")
    opening_remarks: str = pydantic.Field(..., description="开场白")


class QAResponse(BaseResponse):
    data: List = pydantic.Field([], description="")
