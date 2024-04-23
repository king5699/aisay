# -*- coding: utf-8 -*-
# @Date: 2024/4/21
# @Author: zhong
# @FileName: bots.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from aisay.chatbot import ChatBot
from aisay.db import LocalFAISSDB

openai_embbeding = OpenAIEmbeddings()


# 数据库注册表
bots_db = {
    '房地产销售': LocalFAISSDB(
        dbname='real_estates_sale',
        description='70条实用的房地产销售话术',
        corpusname='real_estate_sales_data.txt',
        embedding=openai_embbeding
    ),
    'AI课程销售': LocalFAISSDB(
        dbname='ai_education_sale',
        description='90条实用的AI课程销售话术',
        corpusname='ai_education_sales_data.txt',
        embedding=openai_embbeding
    ),
}

# 聊天机器人注册表
bots_base = [
    ChatBot(
        name='恒小小',
        description='房地产销售聊天机器人，为买家解答房屋购买相关的问题',
        db=bots_db['房地产销售'],
        llm=ChatOpenAI(temperature=0.5),
        search_type='similarity_score_threshold',
        search_kwargs={'score_threshold': 0.7},
        enable_chat_when_no_match=True),
    ChatBot(
        name='海棠',
        description='教育培训机构聊天机器人，为学员解答购买AI课程相关的问题',
        db=bots_db['AI课程销售'],
        llm=ChatOpenAI(temperature=0.5),
        search_type='similarity_score_threshold',
        search_kwargs={'score_threshold': 0.8},
        enable_chat_when_no_match=False),
]

bots_dict = {bot.name: bot for bot in bots_base}
