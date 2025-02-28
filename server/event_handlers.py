import os

from fastapi import FastAPI
import logging
from zhipuai import ZhipuAI
from server.singleton import Singleton

log = logging.getLogger("uvicorn")


def register_events(app: FastAPI):
    """
    服务启动与关闭触发方法
    :param app: FastAPI框架服务应用对象
    :return: pass
    """

    @app.on_event("startup")
    async def startup_event():
        """
        服务启动触发方法
        :return:
        """

        # 初始化系统变量
        singleton = Singleton()
        disposition_prompt = os.environ.get('CHAT.PROMPT')
        singleton.set_chat_prompt(disposition_prompt)

        chat_num = os.environ.get('CHAT.NUM')
        chat_num = int(chat_num) if chat_num is not None else None
        singleton.set_chat_num(chat_num)

        # 初始化对话历史
        messages = [
            {"role": "system", "content": disposition_prompt}
        ]
        singleton.set_messages(messages)

        # 智谱AI token密钥
        api_key = os.environ.get('ZHIPU.TOKEN')
        # 初始化 ZhipuAI 客户端
        client = ZhipuAI(api_key=api_key)
        singleton.set_llm_client(client)
        model = os.environ.get('ZHIPU.MODEL')
        singleton.set_glm_model(model)



        log.info("服务启动成功!")

    @app.on_event("shutdown")
    async def shutdown_event():
        """
        服务关闭触发方法
        :return:
        """
        log.info("服务关闭!")
