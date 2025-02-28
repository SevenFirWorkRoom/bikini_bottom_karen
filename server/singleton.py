
"""
单例模式全局变量
"""
class Singleton:
    _instance = None
    # 对话提示词
    chat_prompt = None
    # llm对话客户端
    llm_client = None
    # llm对话上下文
    messages = None
    # llm对话上下文轮数
    chat_num = None
    # 智谱清言模型
    glm_model = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    @classmethod
    def set_chat_prompt(cls, value):
        cls.chat_prompt = value

    @classmethod
    def get_chat_prompt(cls):
        return cls.chat_prompt

    @classmethod
    def set_messages(cls, value):
        cls.messages = value

    @classmethod
    def get_messages(cls):
        return cls.messages

    @classmethod
    def set_llm_client(cls, value):
        cls.llm_client = value

    @classmethod
    def get_llm_client(cls):
        return cls.llm_client

    @classmethod
    def set_glm_model(cls, value):
        cls.glm_model = value

    @classmethod
    def get_glm_model(cls):
        return cls.glm_model

    @classmethod
    def set_chat_num(cls, value):
        cls.chat_num = value

    @classmethod
    def get_chat_num(cls):
        return cls.chat_num