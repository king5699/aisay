# -*- coding: utf-8 -*-
# @Date: 2024/4/18
# @Author: zhongchao
# @FileName: init_db.py
import time
from typing import List
from aisay.biz import bots_base
from aisay.chatbot import DB
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS


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


def init_local_faiss_db(docs: List[Document], embedding: Embeddings, dbpath: str):
    db = FAISS.from_documents(docs, embedding)
    db.save_local(dbpath)


def run(bots):
    print('=== aisay.init_db.run(bots) ===')
    dbnames = []
    for bot in bots:
        stime = time.perf_counter()
        print(f'bot.name="{bot.name}"')
        print(f'bot.dbname="{bot.dbname}"')
        print(f'bot.corpus_path="{bot.corpus_path}"')
        if bot.dbname in dbnames:
            print(f'Duplicate dbname Error')
            continue
        docs = create_docs_from_corpus(bot.corpus_path)
        if bot.dbtype == DB.FAISS:
            init_local_faiss_db(docs, bot.embedding)
            print(f'success，cost time：{time.perf_counter()-stime:.2f}s\n')
        else:
            print(f'fail, unsupported dbtype="{bot.dbtype}"\n')


if __name__ == '__main__':
    run(bots_base)
