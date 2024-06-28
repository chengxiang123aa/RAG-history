#对接milvus数据库，包括建表，查询，插入等
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from loguru import logger
from web.configs import MILVUS_HOST, MILVUS_PORT, VECTOR_DIMENSION, METRIC_TYPE, DBNAME, SECURE
class MilvusHelper:
    """
    Say something about the Example Class...

    Args:
        args_0 (`type`):
        ...
    """
    def __init__(self):
        try:
            self.collection = None
            connections.connect(host=MILVUS_HOST, port=MILVUS_PORT, db_name=DBNAME, secure=SECURE)
            logger.debug(f"Successfully connect to Milvus with IP:{MILVUS_HOST} and PORT:{MILVUS_PORT}")
        except Exception as e:
            logger.error(f"Failed to connect Milvus: {e}")
            raise e

    def set_collection(self, collection_name):
        """
        加载指定表格的数据到 Milvus
        :param collection_name:
        :return:
        """
        try:
            if self.has_collection(collection_name):
                self.collection = Collection(name=collection_name)
            else:
                raise Exception(f"There is no collection named:{collection_name}")
        except Exception as e:
            logger.error(f"Failed to load data to Milvus: {e}")
            raise e

    def has_collection(self, collection_name):
        """
        查询是否存在该表
        :param collection_name:
        :return:
        """
        try:
            return utility.has_collection(collection_name)
        except Exception as e:
            logger.error(f"Failed to load data to Milvus: {e}")
            # sys.exit(1)
            raise e

    def create_collection(self, collection_name):
        """
        如果表不存在则创建新的表
        :param collection_name:
        :return:
        """
        try:
            if not self.has_collection(collection_name):
                field1 = FieldSchema(name="id", dtype=DataType.INT64, description="int64", is_primary=True, auto_id=True)
                field2 = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, description="float vector",
                                     dim=VECTOR_DIMENSION, is_primary=False)
                field3 = FieldSchema(name="content", dtype=DataType.VARCHAR, description="related content",
                                     max_length=1000, is_primary=False)
                
                schema = CollectionSchema(fields=[field1, field2, field3], description="collection description")
                self.collection = Collection(name=collection_name, schema=schema)
                logger.debug(f"Create Milvus collection: {collection_name}")
            else:
                self.set_collection(collection_name)
            return "OK"
        except Exception as e:
            logger.error(f"Failed to load data to Milvus: {e}")
            raise e

    def insert(self, collection_name, data):
        """
        向指定的表中插入数据
        :param collection_name:
        :param data:
        :return:
        """
        self.set_collection(collection_name)
        mr = self.collection.insert(data)
        ids = mr.primary_keys
        self.collection.load()
        logger.debug(
            f"Insert vectors to Milvus in collection: {collection_name} with {len(data)} rows")
        return ids

    def create_index(self, collection_name):
        """
        为表格创建索引
        :param collection_name:
        :return:
        """
        try:
            self.set_collection(collection_name)
            if self.collection.has_index():
                return None
            # nlist是聚类中心的个数
            default_index = {"index_type": "IVF_SQ8", "metric_type": METRIC_TYPE, "params": {"nlist": 16384}}
            status = self.collection.create_index(field_name="embedding", index_params=default_index, timeout=60)
            if not status.code:
                logger.debug(
                    f"Successfully create index in collection:{collection_name} with param:{default_index}")
                return status
            else:
                raise Exception(status.message)
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            raise e

    def delete_collection(self, collection_name):
        """
        删除指定名称的表格
        :param collection_name:
        :return:
        """
        try:
            self.set_collection(collection_name)
            self.collection.drop()
            logger.debug("Successfully drop collection!")
            return "ok"
        except Exception as e:
            logger.error(f"Failed to drop collection: {e}")
            #  # sys.exit(1)
            raise e

    def search_vectors(self, collection_name, vectors, top_k):
        """
        从表格中搜索topk个相似的图片
        :param collection_name:
        :param vectors:
        :param top_k:
        :return:
        """
        # Search vector in milvus collection
        try:
            self.set_collection(collection_name)
            search_params = {"metric_type": METRIC_TYPE, "params": {"nprobe": 16}}
            res = self.collection.search(
                vectors,
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=["id", "content"]
            )
            return res
        except Exception as e:
            logger.error(f"Failed to search vectors in Milvus: {e}")
            raise e

    def count(self, collection_name):
        """
        统计表格中有多少条记录
        :param collection_name:
        :return:
        """
        try:
            self.set_collection(collection_name)
            num = self.collection.num_entities
            logger.debug(f"Successfully get the num:{num} of the collection:{collection_name}")
            return num
        except Exception as e:
            logger.error(f"Failed to count vectors in Milvus: {e}")
            raise e

    def delete(self, collection_name, expr):
        """
        删除表格，返回表格中有多少条记录
        :param collection_name:
        :param expr:
        :return:
        """
        self.set_collection(collection_name)
        num = self.collection.delete(expr)
        logger.info(f"Successfully delete the expr:{expr} of the collection:{collection_name}")
        return num

