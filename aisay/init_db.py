# -*- coding: utf-8 -*-
# @Date: 2024/4/18
# @Author: zhongchao
# @FileName: init_db.py
import os
import time
from aisay import CORPUSDIR, DBDIR
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS


def init_real_estate_sales_data_db():
    """初始化房地产销售数据库"""
    print('初始化房地产销售数据库')
    stime = time.perf_counter()
    docs = TextLoader(os.path.join(CORPUSDIR, 'real_estate_sales_data.txt'), encoding='utf-8').load()
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True
    )
    docs = text_spliter.split_documents(docs)
    db = FAISS.from_documents(docs, OpenAIEmbeddings())
    db.save_local(os.path.join(DBDIR, 'real_estates_sale'))
    print(f'已完成，耗时：{time.perf_counter()-stime:.2f}s')


def run():
    init_real_estate_sales_data_db()


if __name__ == '__main__':
    run()
