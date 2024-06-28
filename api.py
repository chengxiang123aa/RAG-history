import os
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from arg.args import parser

from fastapi import FastAPI
from router import service, search
from web.configs import OPEN_CROSS_DOMAIN,KB_ROOT_PATH

app = FastAPI()
env = os.getenv('env')
if env != 'develop':
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI()
os.makedirs(KB_ROOT_PATH, exist_ok=True)

app.include_router(search.router_search)
app.include_router(service.router_milvus)

def api_start(host, port):
    if OPEN_CROSS_DOMAIN:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default="8080")
    # 初始化消息
    args = parser.parse_args()
    args_dict = vars(args)
    api_start(args.host, args.port)