# -*- coding: utf-8 -*-
# @Date: 2024/4/19
# @Author: zhongchao
# @FileName: biz.py
from langchain_openai import ChatOpenAI
from aisay.bots import bots_dict


bots_dict['恒小小'].activate(
    llm=ChatOpenAI(temperature=0.5),
    search_type='similarity_score_threshold',
    search_kwargs={'score_threshold': 0.7},
    enable_chat_when_no_match=True
)

bots_dict['海棠'].activate(
    llm=ChatOpenAI(temperature=0.5),
    search_type='similarity_score_threshold',
    search_kwargs={'score_threshold': 0.8},
    enable_chat_when_no_match=False
)

activated_bots = {name: bot for name, bot in bots_dict.items() if bot.activated}
