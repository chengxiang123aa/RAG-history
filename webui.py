import gradio as gr
from loguru import logger
import gradio as gr 
from operation.search import get_answer

# 定义一个函数，用于计算用户上传的文件数量
def deal_question(question, history):
    try:
        res = get_answer(question)
        return res
    except Exception as e:
        logger.error(e)
        return {'code': 500, 'message': str(e)}
 

demo = gr.ChatInterface(
    fn = deal_question,
    examples = [{"text": "Hello", "files": []}],
    title = "History Bot",
    multimodal=False
)

# 启动 Gradio 服务器
demo.launch(server_name="0.0.0.0", server_port=8080)

