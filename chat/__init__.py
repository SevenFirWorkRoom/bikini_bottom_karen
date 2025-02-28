import logging
from chat.glm_chat_utils import glm_chat

log = logging.getLogger("uvicorn")


def llm_chat_deal(user_input=None):
    """
    LLM对话
    :param user_input: 用户输入消息
    :return: llm回复
    """
    answer = None
    try:
        answer = glm_chat(user_input)
        log.info(f"LLM大模型回答：{answer}")
    except Exception as e:
        log.error(e)
        log.error("LLM服务处理失败")
    return answer
