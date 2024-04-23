# -*- coding: utf-8 -*-
# @Date: 2024/4/18
# @Author: zhongchao
# @FileName: init_db.py
import time
from typing import List
from aisay.bots import bots_db
from aisay.db import ChatDB
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader


def create_docs_from_corpus(corpus_path: str) -> List[Document]:
    """
    根据语料创建切分好的文档
    :param corpus_path: 语料文档路径
    """
    docs = TextLoader(corpus_path, encoding='utf-8').load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True
    )
    docs = text_splitter.split_documents(docs)
    return docs


def init_db(db: ChatDB):
    stime = time.perf_counter()
    print(f'dbname="{db.dbname}"')
    print(f'corpus_path="{db.corpus_path}"')
    docs = create_docs_from_corpus(db.corpus_path)
    db.save(docs)
    print(f'success，cost time：{time.perf_counter()-stime:.2f}s\n')


if __name__ == '__main__':
    print('=== aisay.init_db ===\n')
    for k, v in bots_db.items():
        print(f'{k}\n------------------------------')
        init_db(v)
