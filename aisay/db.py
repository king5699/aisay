# -*- coding: utf-8 -*-
# @Date: 2024/4/23
# @Author: zhongchao
# @FileName: db.py
import os
from abc import ABC, abstractmethod
from typing import Optional, List
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from aisay.conf import CORPUSDIR, DBDIR


class ChatDB(ABC):
    """
    聊天机器人知识库
    """
    def __init__(self,
                 dbname: str,
                 description: str,
                 corpusname: str,
                 embedding: Optional[Embeddings] = None):
        """
        :param dbname: 数据库名
        :param description: 描述
        :param corpusname: 语料文件名
        :param embedding: embdding函数
        """
        self.dbname = dbname
        self.dbpath = os.path.join(DBDIR, dbname)
        self.description = description
        self.corpus_path = os.path.join(CORPUSDIR, corpusname)
        self.embedding = embedding or OpenAIEmbeddings()
        self._db = None
        self._loaded = False

    @abstractmethod
    def load(self):
        """加载数据"""

    @abstractmethod
    def save(self, docs: List[Document]):
        """保存数据"""

    def as_retriever(self,
                     search_type: Optional[str] = 'similarity',
                     search_kwargs: Optional[dict] = None):
        """
        转换为检索器
        :param search_type: similarity, mmr, similarity_score_threshold
        :param search_kwargs: k, score_threshold, fetch_k, lambda_mult, filter
        :return:
        """
        if not self._loaded:
            self.load()
        return self._db.as_retriever(search_type=search_type, search_kwargs=search_kwargs)


class LocalFAISSDB(ChatDB):
    """
    本地FAISS数据库
    """

    def load(self):
        self._db = FAISS.load_local(self.dbpath, self.embedding,
                                    allow_dangerous_deserialization=True)
        self._loaded = True

    def save(self, docs: List[Document]):
        self._db = FAISS.from_documents(docs, self.embedding)
        self._db.save_local(self.dbpath)
        self._loaded = True
