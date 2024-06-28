import os
from typing import Dict, List, Optional, Tuple, Union
import PyPDF2
import markdown
import html2text
import json
from tqdm import tqdm
import tiktoken
from bs4 import BeautifulSoup
import re
import os
tiktoken_cache_dir = "./"
os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir
enc = tiktoken.get_encoding("cl100k_base")
class ReadFiles:
    """
    class to read files
    """
    def __init__(self, path: str) -> None:
        self._path = path
        self.file_list = self.get_files()

    def get_files(self):
        # args：dir_path，目标文件夹路径
        file_list = []
        for filepath, dirnames, filenames in os.walk(self._path):
            # os.walk 函数将递归遍历指定文件夹
            for filename in filenames:
                # 通过后缀名判断文件类型是否满足要求
                if filename.endswith(".md"):
                    # 如果满足要求，将其绝对路径加入到结果列表
                    file_list.append(os.path.join(filepath, filename))
                elif filename.endswith(".txt"):
                    file_list.append(os.path.join(filepath, filename))
                elif filename.endswith(".pdf"):
                    file_list.append(os.path.join(filepath, filename))
        return file_list

    def get_content(self, max_token_len: int = 300):
        docs = []
        # 读取文件内容
        for file in self.file_list:
            content = self.read_file_content(file)
            #chunk只涉及min
            # chunk_content = self.get_chunk(
            #     content, min_token_len=min_token_len, cover_content=cover_content)
            chunk_content = tqdm(self.get_chunk2(
                content, max_token_len=max_token_len))
            docs.extend(chunk_content)
        return docs

    @classmethod
    def get_chunk(cls, text: str, min_token_len: int = 600, cover_content: int = 150):
        chunk_text = []
        curr_len = 0
        curr_chunk = ''
        lines = text.split('\n')                                   # 假设以换行符分割文本为行
        for line in lines:
            line = line.replace(' ', '')
            line_len = len(enc.encode(line))
            if line_len > min_token_len:
                print('warning line_len = ', line_len)
            if curr_len + line_len <= min_token_len:
                curr_chunk += line
                curr_chunk += '\n'
                curr_len += line_len
                curr_len += 1
            else:
                if curr_chunk:
                    chunk_text.append(curr_chunk)
                    curr_chunk = curr_chunk[-cover_content:] + line
                    curr_len = line_len + cover_content

        if curr_chunk:
            chunk_text.append(curr_chunk)

        return chunk_text
    
    @classmethod
    def get_chunk2(cls, text: str, max_token_len: int):
        chunk_text = []
        curr_chunk = ""
        curr_len = 0
        lines = text.split('。')
        for line in lines:
            line = line.strip()  # 去除首尾空格和换行符
            line_len = len(line)  # 计算行的长度
            if curr_len + line_len > max_token_len:
                # 如果当前片段加上当前行超过了最大长度，将当前片段添加到结果列表中，并重新开始记录新的片段
                if curr_chunk:
                    chunk_text.append(curr_chunk.strip())
                curr_chunk = line
                curr_len = line_len
            else:
                # 否则，将当前行添加到当前片段中，更新当前长度
                curr_chunk += " " + line if curr_chunk else line
                curr_len += line_len
        # 将最后一段记录的片段添加到结果列表中
        if curr_chunk:
            chunk_text.append(curr_chunk.strip())

        return chunk_text
    

    @classmethod
    def get_chunk3(cls, text: str, min_token_len: int = 10, max_token_len: int = 100, cover_content: int = 10):
        chunk_text = []
        chunk_lenth = []

        curr_len = 0
        curr_chunk = ''

        lines = text.split('\n')  # 假设以换行符分割文本为行
        for line in lines:
            line = line.replace(' ', '')
            line_len = len(enc.encode(line))
            if curr_len > max_token_len:
                while (curr_len > max_token_len):
                    split_a = enc.encode(curr_chunk)[:max_token_len]
                    split_b = enc.encode(curr_chunk)[max_token_len:]
                    curr_chunk = enc.decode(split_a)
                    chunk_text.append(curr_chunk)
                    chunk_lenth.append(max_token_len)
                    curr_chunk = curr_chunk[-cover_content:] + enc.decode(split_b)
                    curr_len = cover_content + curr_len - max_token_len
            else:
                if (curr_len <= min_token_len):
                    curr_chunk += line
                    curr_chunk += '\n'
                    curr_len += line_len
                    curr_len += 1
                else:
                    chunk_text.append(curr_chunk)
                    chunk_lenth.append(curr_len)
                    curr_chunk = curr_chunk[-cover_content:] + line
                    curr_len = line_len + cover_content
        if curr_chunk:
            chunk_text.append(curr_chunk)
            chunk_lenth.append(curr_len)
        return chunk_text

    @classmethod
    def read_file_content(cls, file_path: str):
        # 根据文件扩展名选择读取方法，暂时只支持pdf，md,txt
        if file_path.endswith('.pdf'):
            return cls.read_pdf(file_path)
        elif file_path.endswith('.md'):
            return cls.read_markdown(file_path)
        elif file_path.endswith('.txt'):
            return cls.read_text(file_path)
        else:
            raise ValueError("Unsupported file type")

    @classmethod
    def read_pdf(cls, file_path: str):
        # 读取PDF文件
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
            return text

    @classmethod
    def read_markdown(cls, file_path: str):
        # 读取Markdown文件
        with open(file_path, 'r', encoding='utf-8') as file:
            md_text = file.read()
            html_text = markdown.markdown(md_text)
            # 使用BeautifulSoup从HTML中提取纯文本
            soup = BeautifulSoup(html_text, 'html.parser')
            plain_text = soup.get_text()
            # 使用正则表达式移除网址链接
            text = re.sub(r'http\S+', '', plain_text) 
            return text

    @classmethod
    def read_text(cls, file_path: str):
        # 读取文本文件
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

class Documents:
    """
        获取已分好类的json格式文档
    """
    def __init__(self, path: str = '') -> None:
        self.path = path
    
    def get_content(self):
        with open(self.path, mode='r', encoding='utf-8') as f:
            content = json.load(f)
        return content