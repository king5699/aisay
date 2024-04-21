# -*- coding: utf-8 -*-
# @Date: 2024/4/19
# @Author: zhongchao
# @FileName: chatbot.py
import os
import random
from enum import Enum, auto
from typing import Optional, List
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import OpenAIEmbeddings
from aisay import CORPUSDIR, DBDIR


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class DB(AutoName):
    FAISS = auto()


class ChatBot:
    """聊天机器人类"""
    DEFAULT_ANSWERS_WHEN_NO_MATCH = [
        '抱歉我也不太清楚',
        '这个问题我要问问领导',
        '这个问题暂时无法回答',
        '我稍后帮您问下'
    ]

    def __init__(self,
                 name: str,
                 descrption: str,
                 corpusname: str,
                 dbname: str,
                 dbtype: DB = DB.FAISS,
                 embedding: Optional[Embeddings] = None):
        """
        :param name: 机器人名称
        :param descrption: 场景描述，用于router的提示词
        :param corpusname: 语料文件名
        :param dbname: 数据库名
        :param dbtype: 数据库类型
        :param embedding: embdding函数
        """
        self.name = name
        self.description = descrption
        self.corpus_path = os.path.join(CORPUSDIR, corpusname)
        self.dbname = dbname
        self.dbpath = os.path.join(DBDIR, dbname)
        self.dbtype = dbtype
        self.embedding = embedding or OpenAIEmbeddings()
        self.db_loaded = False
        self.activated = False
        self.db = None
        self._chatbot = None
        self.enable_chat_when_no_match = None
        self.default_answers_when_no_match = self.DEFAULT_ANSWERS_WHEN_NO_MATCH[:]

    def load_db(self):
        if self.dbtype == DB.FAISS:
            self.db = FAISS.load_local(self.dbpath, self.embedding, allow_dangerous_deserialization=True)
            self.db_loaded = True
        else:
            raise ValueError(f'Invalid dbtype: {self.dbtype}')

    def activate(self,
                 llm: BaseLanguageModel,
                 search_type: Optional[str] = 'similarity',
                 search_kwargs: Optional[dict] = None,
                 enable_chat_when_no_match: bool = True,
                 default_answers_when_no_match: Optional[List[str]] = None):
        """
        激活聊天机器人
        :param llm: 用于生成对话的大语言模型
        :param search_type: similarity, mmr, similarity_score_threshold
        :param search_kwargs: k, score_threshold, fetch_k, lambda_mult, filter
        :param enable_chat_when_no_match: 没有匹配文档时，是否还采用llm生成的聊天消息
        :param default_answers_when_no_match: 没有匹配文档时，默认从此答复列表中随机返回
        :return:
        """
        if not self.db_loaded:
            self.load_db()
        self._chatbot = RetrievalQA.from_chain_type(llm, retriever=self.db.as_retriever(
            search_type=search_type, search_kwargs=search_kwargs))
        self._chatbot.return_source_documents = True
        self.activated = True
        self.enable_chat_when_no_match = enable_chat_when_no_match
        if default_answers_when_no_match:
            self.default_answers_when_no_match = default_answers_when_no_match

    def reply(self, message):
        if not self.activated:
            raise Exception('This chatbot has not been activated!')
        ans = self._chatbot.invoke({'query': message})
        if ans['source_documents'] or self.enable_chat_when_no_match:
            return ans['result']
        else:
            return random.choice(self.default_answers_when_no_match)
