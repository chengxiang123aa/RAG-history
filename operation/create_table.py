from router import MILVUS_CLI
from web.configs import DEFAULT_TABLE
from loguru import logger


def do_create_table(table):
    table_name = table
    if not table_name:
        table_name = DEFAULT_TABLE
    try:
        MILVUS_CLI.create_collection(table_name)
        MILVUS_CLI.create_index(table_name)
    except Exception as e:
        raise e


