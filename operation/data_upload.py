from data_process.embedding import get_embedding
from router import MILVUS_CLI
from data_process.textspliter import ReadFiles
from web.configs import DEFAULT_TABLE,DATA_PATH
from operation.create_table import do_create_table
from loguru import logger

def do_upload(content, table_name):
    if not table_name:
        table_name = DEFAULT_TABLE
    try:
        res = get_embedding(content)
        data = [
            {
                "embedding": res,
                "content": content,
            }
        ]
        ids = MILVUS_CLI.insert(table_name, data)
        return ids
    except Exception as e:
        return f"上传失败，错误信息：{str(e)}"
    
def upload_data(path):
    if not path:
        path = DATA_PATH
    try:
        test = ReadFiles(path)
        res=test.get_content()
        do_create_table(DEFAULT_TABLE)
        for i in res:
            result=do_upload(i,DEFAULT_TABLE)
            logger.info(f'current content is embedded,id:{result}')
    except Exception as e:
        raise e
        
        
    
        

