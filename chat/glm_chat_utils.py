from zhipuai import APIConnectionError

from server.singleton import Singleton


def glm_chat(user_input=None):
    """
    智谱清言-LLM对话
    :param user_input: 用户输入消息
    :return: llm回复
    """

    singleton = Singleton()
    # 使用全局的对话历史
    messages =  singleton.get_messages()
    client = singleton.get_llm_client()
    model = singleton.get_glm_model()
    chat_num = singleton.get_chat_num()
    chat_num = int(chat_num) if chat_num is not None else 5
    chat_num = chat_num * 2 + 3
    if user_input is None:
        return None
    # 将用户输入添加到对话历史
    messages.append({"role": "user", "content": user_input})

    # 生成响应
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
    except APIConnectionError:
        return None

    # 获取 AI 的回复
    ai_response = response.choices[0].message.content

    # 将 AI 的回复添加到对话历史
    messages.append({"role": "assistant", "content": ai_response})


    if len(messages) > chat_num:
        # 删除最开始的对话信息
        del messages[1]
        del messages[2]


    # 返回 AI 的回复
    return ai_response
