import logging

from asr.baidu import asr_change_rate

log = logging.getLogger("uvicorn")


def asr_deal(file_path):
    """
    语音转文字服务
    :param file_path: 音频文件本地路径
    :return: 音频文件转换成的文本信息
    """
    user_text = None
    try:
        user_text = asr_change_rate(file_path)
        log.info(f"asr服务处理结果：{user_text}")
    except Exception as e:
        log.error(e)
        log.error("asr服务处理失败")
    return user_text