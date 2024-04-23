# -*- coding: utf-8 -*-
# @Date: 2024/4/19
# @Author: zhongchao
# @FileName: chatbot.py
import random
from typing import Optional, List
from langchain.chains import RetrievalQA
from langchain_core.language_models import BaseLanguageModel
from aisay.db import ChatDB


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
                 description: str,
                 db: ChatDB,
                 llm: BaseLanguageModel,
                 search_type: Optional[str] = 'similarity',
                 search_kwargs: Optional[dict] = None,
                 enable_chat_when_no_match: bool = True,
                 default_answers_when_no_match: Optional[List[str]] = None):
        """
        :param name: 机器人名称
        :param description: 场景描述，用于router的提示词
        :param db: 聊天知识数据库
        :param llm: 用于生成对话的大语言模型
        :param search_type: similarity, mmr, similarity_score_threshold
        :param search_kwargs: k, score_threshold, fetch_k, lambda_mult, filter
        :param enable_chat_when_no_match: 没有匹配文档时，是否还采用llm生成的聊天消息
        :param default_answers_when_no_match: 没有匹配文档时，默认从此答复列表中随机返回
        """
        self.name = name
        self.description = description
        self.db = db
        self.llm = llm
        self.search_type = search_type
        self.search_kwargs = search_kwargs
        self.enable_chat_when_no_match = enable_chat_when_no_match
        self.default_answers_when_no_match = \
            default_answers_when_no_match or self.DEFAULT_ANSWERS_WHEN_NO_MATCH[:]
        self._chatbot = None
        self._activated = False

    def activate(self):
        """
        激活聊天机器人
        """
        self._chatbot = RetrievalQA.from_chain_type(self.llm, retriever=self.db.as_retriever(
            search_type=self.search_type, search_kwargs=self.search_kwargs))
        self._chatbot.return_source_documents = True
        self._activated = True

    def reply(self, message: str) -> str:
        if not self._activated:
            self.activate()
        ans = self._chatbot.invoke({'query': message})
        if ans['source_documents'] or self.enable_chat_when_no_match:
            return ans['result']
        else:
            return random.choice(self.default_answers_when_no_match)
