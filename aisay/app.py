# -*- coding: utf-8 -*-
# @Date: 2024/4/18
# @Author: zhongchao
# @FileName: app.py
import os
import gradio as gr
from aisay import STATICDIR
from aisay.biz import activated_bots


def do_chat(message, history):
    print(f'[history]{history}')
    print(f'[message]{message}')
    chatbot = activated_bots['海棠']
    return chatbot.reply(message)


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
    launch_gradio()
