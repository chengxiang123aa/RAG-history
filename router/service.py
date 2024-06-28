import os.path
from fastapi import APIRouter
from loguru import logger
from operation.create_table import do_create_table
from operation.data_upload import upload_data
from router import MILVUS_CLI
from web.configs import ROUTE_PREFIX, VERSION, DEFAULT_TABLE,DATA_PATH
from web.response import BaseResponse


router_milvus = APIRouter(
    prefix=rf'/{ROUTE_PREFIX}/{VERSION}',  # 路由前缀
    tags=['milvus operations']  # API文档标签
)


@router_milvus.post('/milvus/table', response_model=BaseResponse)
def create_table(table: str = DEFAULT_TABLE):
    """
    创建指定名称的collection
    :param table: 表格的名称
    :return:
    """
    try:
        status = do_create_table(table)
        logger.info(f'status: {status}')
        return BaseResponse(code=200, msg=f"表格 '{table}' 已成功创建。")
    except Exception as e:
        return BaseResponse(code=500, msg=f"表格创建时发生错误：{str(e)}")
    
@router_milvus.post('/milvus/data', response_model=BaseResponse)
def add_data(path: str = DATA_PATH):
    """
    创建指定名称的collection
    :param table: 表格的名称
    :return:
    """
    try:
        status = upload_data(path)
        logger.info(f'status: {status}')
        return BaseResponse(code=200, msg=f"表格数据已上传到milvus。")
    except Exception as e:
        return BaseResponse(code=500, msg=f"上传数据发生错误：{str(e)}")
    

    



    
    






