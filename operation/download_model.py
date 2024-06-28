from modelscope import snapshot_download
model_dir = snapshot_download('AI-ModelScope/m3e-base', cache_dir='E:/Gitlab/RAG-chatbot/model/',
                              revision='master')