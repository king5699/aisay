# -*- coding: utf-8 -*-
# @Date: 2024/4/21
# @Author: zhong
# @FileName: bots.py
from langchain_openai import OpenAIEmbeddings
from aisay.chatbot import ChatBot, DB

openai_embbeding = OpenAIEmbeddings()


# 聊天机器人注册表
bots_base = [
    ChatBot(
        name='恒小小',
        descrption='房地产销售聊天机器人，为买家解答房屋购买相关的问题',
        corpusname='real_estate_sales_data.txt',
        dbname='real_estates_sale',
        dbtype=DB.FAISS,
        embedding=openai_embbeding),
    ChatBot(
        name='海棠',
        descrption='教育培训机构聊天机器人，为学员解答购买AI课程相关的问题',
        corpusname='ai_education_sales_data.txt',
        dbname='ai_education_sale',
        dbtype=DB.FAISS,
        embedding=openai_embbeding),
]

bots_dict = {bot.name: bot for bot in bots_base}
