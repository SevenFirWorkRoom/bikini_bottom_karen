import logging
from tts.tts_http_demo import audio_synthetic

log = logging.getLogger("uvicorn")

def tts_deal(text):
    """
    文件转语音服务
    :param text: 文本信息
    :return: 文本信息转换成的音频文件本地路径
    """
    path = None
    try:
        path = audio_synthetic(text)
    except Exception as e:
        log.error(e)
        log.error("LLM服务处理失败")
    return path