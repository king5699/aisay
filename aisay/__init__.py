# -*- coding: utf-8 -*-
# @Date: 2024/4/18
# @Author: zhongchao
# @FileName: __init__.py
import os

ROOTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DBDIR = os.path.join(ROOTDIR, 'db')
CORPUSDIR = os.path.join(ROOTDIR, 'corpus')
STATICDIR = os.path.join(ROOTDIR, 'static')
