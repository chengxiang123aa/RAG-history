from web.configs import DEFAULT_TABLE,TOPK
from router import MILVUS_CLI
from collections import defaultdict
from LLM.llm_chat import QwenChat
from data_process.embedding import get_embedding

def do_search_in_db(table_name, text, top_k):
    if not table_name:
        table_name = DEFAULT_TABLE
    embedding=get_embedding(text)
    vectors = MILVUS_CLI.search_vectors(table_name,[embedding], top_k)
    res = []
    for x in vectors[0]:
        score = 1 - x.distance
        id = x.entity.get('id')
        content = x.entity.get('content')
        res.append({'score': score, 'id': id, 'content': content})
    return res

def process_related_content(info):
    d = defaultdict(list)
    for item in info:
        d['可供参考的文献'].append(item['content'])
    return d


def get_answer(question):
    content = do_search_in_db(DEFAULT_TABLE,question,TOPK)
    related_info=process_related_content(content)
    chat = QwenChat()
    return f"知识库输出：{chat.chat(question, [], related_info)}"



