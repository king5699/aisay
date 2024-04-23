# -*- coding: utf-8 -*-
# @Date: 2024/4/18
# @Author: zhongchao
# @FileName: app.py
import os
import gradio as gr
from aisay.conf import STATICDIR
from aisay.bots import bots_dict


def do_chat(message, history):
    print(f'[history]{history}')
    print(f'[message]{message}')

    chatbot = bots_dict['海棠']
    answer = chatbot.reply(message)
    print(f'[answer]{answer}')
    return answer


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
