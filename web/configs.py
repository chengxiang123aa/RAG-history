import os
import platform

SYSTEM = platform.system()
ENVIRONMENT = {
    "Linux": {
        "IP": "0.0.0.0",
        "PORT": 8080
    },
    "Windows": {
        "IP": "127.0.0.1",
        "PORT": 8033
    }
}

ZhipuAI_API_KEY = 'ZhipuAI_API_KEY'
DASH_SCOPE_KEY = 'DASH_SCOPE_KEY'
IP = ENVIRONMENT[SYSTEM]["IP"]
PORT = ENVIRONMENT[SYSTEM]["PORT"]
EMBED_MODEL = 'embed_model path'
DATA_PATH = 'E:/Gitlab/RAG-chatbot/data'
CHAT_MODEL = "local chat model"
MILVUS_HOST = "MILVUS_HOST"
MILVUS_PORT = "MILVUS_PORT"
VECTOR_DIMENSION = 768
METRIC_TYPE = 'L2'
SECURE = False
DBNAME = "xc_history"
DEFAULT_TABLE = "novel"

OPEN_CROSS_DOMAIN = True

ROUTE_PREFIX = "novel"
VERSION = "v1"

KB_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")
NLTK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")

TOPK = 5
RANDOM_TOPK = 50

access_key_id = 'access_key_id'
access_key_secret = 'access_key_secret'
bucket_name = 'aigcimage'
endpoint = 'oss-cn-beijing.aliyuncs.com'

