

# 中国历史的RAG外部知识库构建，大模型私有化领域检索增强

History RAG，其由 最爱吃香菜 与独立完成，通过构建一个外部数据库，当作大模型的上下文参考，以减小大模型幻觉，提高回答正确率，不一定都适用，不过是我随便做的一个小项目，也参考了很多开源的资料。

本项目开源出来，主要是记录一下自己的学习痕迹，如果顺便能帮到某位爱好者学习的话，请给我一个小星星鼓励！


## 目录
- [上手指南](#上手指南)
  - [环境支持](#环境支持)
  - [安装步骤](#安装步骤)
- [文件目录说明](#文件目录说明)
- [使用文档](#使用文档)
  - [脚本调用](#i-脚本调用)
  - [API调用](#ii-api调用)
  - [chatbot](#ii-chatbot交互)
- [版本控制](#版本控制)
- [作者](#作者)


### 上手指南
###### **安装步骤**

**ii. 从源码安装**
```sh
git clone https://github.com/chengxiang123aa/RAG-history.git
cd RAG-history
pip install -r requirements.txt
```
### 文件目录说明
eg:

```
History RAG
├── LLM                       你自己的部署到本地的大模型可以放在这里
├── Milvus                    对milvus数据库的操作
├── arg
├── data_process
│  │── embedding.py           对切割文本embedding  （下载到本地的embedding模型）
│  │── sentence_embedding.py  对切割文本embedding （使用大模型embedding）
│  │── textspliter.py         文本切割方法 
├── operation
│  │── __init__.py
│  │── create_table.py        在milvus建表
│  │── data_upload.py         仅需要将你的参考资料放在data目录下，执行该文件，会自动切分，embeding，上传milvus （目前只支持.txt,.md,.pdf）
│  │── download_model.py      下载embedding的模型，或者你可以选择调用api来embedding
├── router                    这里是封装api用的，不必理会
├── web
│  │── config.py              各种key，本机ip，端口或者服务器ip，端口，路径等，提前设置好。
├── requirements.txt          坏境配置，可能报错，自己上网查资料，都是小问题
├── answer.py                 脚本启动（前提是条件满足）
├── api.py                    api启动，利用FastAPI
├── webui.py                  web端的chatbot交互


```

### 使用文档

##### i. 脚本调用

主要用于小领域，小场景的应用，因为在这些领域大模型往往表现效果较差，如果有上下文的参考，效果会更好。

```python

from operation.search import get_answer

if __name__=="__main__":
    question = '评价一下宋朝的科技水平？'
    result = get_answer(question)
    print(result)

```
<img src="https://chengxiangstore.oss-cn-shanghai.aliyuncs.com/%E8%84%9A%E6%9C%AC.png?Expires=1719565866&OSSAccessKeyId=TMP.3KfQJX26j4R2DnzgQ8SfDHzBdhg7j7otPupcakbyoEdMnrNa3CF1KcMhJgWcUbsXF5xRR6JoRzB3Rp3mNDeuSuH6wUDeyq&Signature=RzKc9CQZG%2F12KyDODaQCERiLLks%3D" alt="captcha" width="150">

**注意**
注意第一次运行会产生一些缓存文件，比如 __pycache__ 这是正常的，这是在下一次就可以避免反复的调来调去，增加速度。


##### ii. api调用

通过Swagger UI端上传参数，参数是 question：str，也就是你的问题，这里还支持想milvus上传数据和建表。

```python
python api.py
```
然后根据链接跳转过去交互

<img src="https://chengxiangstore.oss-cn-shanghai.aliyuncs.com/API%E8%B0%83%E7%94%A8.png?Expires=1719566017&OSSAccessKeyId=TMP.3KfQJX26j4R2DnzgQ8SfDHzBdhg7j7otPupcakbyoEdMnrNa3CF1KcMhJgWcUbsXF5xRR6JoRzB3Rp3mNDeuSuH6wUDeyq&Signature=FqyDfrf3AvejZHprkpfdXxyUSg4%3D" alt="captcha" width="200">


##### ii. web交互
```python
python webui.py

```
<img src='https://chengxiangstore.oss-cn-shanghai.aliyuncs.com/web%E7%AB%AF%E4%BA%A4%E4%BA%92.png?Expires=1719565922&OSSAccessKeyId=TMP.3KfQJX26j4R2DnzgQ8SfDHzBdhg7j7otPupcakbyoEdMnrNa3CF1KcMhJgWcUbsXF5xRR6JoRzB3Rp3mNDeuSuH6wUDeyq&Signature=oB6%2Fsp6MiHVtyp3H4aYOugCpiZA%3D' alt="captcha" width="200">

### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。

### 作者
2443369158@qq.com 
有问题可以给我发邮件，或者在issue里面留言，我会及时回复！








