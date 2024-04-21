# aisay
a simple chatbot based on llm and vectorstore

### 一个简单的基于llm和向量数据库的RAG聊天机器人，默认提供的本地知识库包括：
1. [恒小小] 房地产销售话术
2. [海棠] AI课程销售话术

### 部署步骤
1. 通过 poetry 创建虚拟环境，并安装依赖包  
``poetry install``
2. 配置对应语言模型的环境变量  
``export OPENAI_API_KEY=xxxxxx``
3. 初始化本地数据库:  
``python aisay/init_db.py``
4. 启动web应用:  
``python aisay/app.py``
5. 打开浏览器访问:  
http://127.0.0.1:7860

### demo演示
![demo.png](/static/demo.png "demo: 海棠")
