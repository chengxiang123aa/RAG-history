from fastapi import APIRouter
from loguru import logger
from answer import get_answer
from operation.search import get_answer
from web.configs import VERSION, ROUTE_PREFIX
from web.request import SearchRequest

router_search = APIRouter(
    prefix=rf'/{ROUTE_PREFIX}/{VERSION}/milvus',  # 路由前缀
    tags=['require answer']  # API文档标签
)


@router_search.post('/search')
async def answer(params: SearchRequest):
    try:
        res = get_answer(params.question)
        return {'code': 200, 'message': 'Successfully', 'result': res}
    except Exception as e:
        logger.error(e)
        return {'code': 500, 'message': str(e)}
