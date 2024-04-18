# -*- coding: utf-8 -*-
# @Date: 2024/4/18
# @Author: zhongchao
# @FileName: app.py
import os
import gradio as gr
from typing import Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from aisay import DBDIR, STATICDIR


BOTBASE = {}


def init_chatbot(dbname: str, **kwargs):
    db = FAISS.load_local(os.path.join(DBDIR, dbname), OpenAIEmbeddings(),
                          allow_dangerous_deserialization=True)
    llm = ChatOpenAI(temperature=0)
    chatbot = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever(**kwargs))
    chatbot.return_source_documents = True
    global BOTBASE
    BOTBASE[dbname] = chatbot
    return chatbot


def get_chatbot(name: Optional[str] = None):
    chatbot = BOTBASE.get(name)
    if not chatbot:
        return list(BOTBASE.values())[0]
    return chatbot


def do_chat(message, history):
    print(f'[history]{history}')
    print(f'[message]{message}')
    enable_chat = True
    chatbot = get_chatbot()
    ans = chatbot({'query': message})
    if ans['source_documents'] or enable_chat:
        print(f"[source_documents]{ans['source_documents']}")
        print(f"[result]{ans['result']}")
        return ans['result']
    else:
        return "这个问题我要问问领导"


def launch_gradio():
    app = gr.ChatInterface(
        fn=do_chat,
        title='aisay, ai爱说话',
        description='',
        chatbot=gr.Chatbot(height=600, layout='bubble'),
        css=os.path.join(STATICDIR, 'aisay.css')
    )
    app.launch(share=False, server_name='0.0.0.0')


if __name__ == '__main__':
    init_chatbot('real_estates_sale',
                 search_type='similarity_score_threshold',
                 search_kwargs={'score_threshold': 0.7})
    launch_gradio()
