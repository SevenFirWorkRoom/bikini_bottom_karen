import logging
import os

from asr import asr_deal
from chat import llm_chat_deal
from tts import tts_deal

log = logging.getLogger("uvicorn")

async def chatchat(message, num):
    log.info(f"服务端收到客户端音频，文件大小为: {len(message)} 字节")

    # 生成唯一的文件名
    file_name = f"audio_{num}.wav"
    file_path = os.path.join("./temp/recordings", file_name)
    with open(file_path, "wb") as audio_file_1:
        # 将接收到的音频数据写入文件
        audio_file_1.write(message)
        # 确保数据立即写入文件
        audio_file_1.flush()

    # 默认错误语音
    listen_error_path = "./acquiesce/listen_error.mp3"
    asr_error_path = "./acquiesce/asr_error.mp3"
    llm_error_path = "./acquiesce/llm_error.mp3"
    tts_error_path = "./acquiesce/tts_error.mp3"
    # 处理问题
    if file_path is not None:
        # 调用 ASR 模块（第一步，将前端用户说话的音频，转换为文本文字信息）
        user_text = asr_deal(file_path)
        if user_text is not None:
            # 调用聊天模块（第二步，将前端用户转换后文本文字信息与大模型进行对话）
            answer = llm_chat_deal(user_text)
            if answer is not None:
                # 调用 TTS 模块（第三步，大模型进行对话回复文本转换为音频）
                audio_file_path = tts_deal(answer)
                audio_file_path = audio_file_path if audio_file_path is not None else tts_error_path
            else:
                audio_file_path = llm_error_path
        else:
            audio_file_path = asr_error_path
    else:
        audio_file_path = listen_error_path



    if not os.path.exists(audio_file_path):
        log.info(f"音频文件 {audio_file_path} 不存在")
        return

    # 打开音频文件并读取内容
    with open(audio_file_path, "rb") as audio_file:
        audio_data = audio_file.read()
        # 发送音频数据给客户端
        log.info(f"LLM大模型回答音频已发送，文件大小 {len(audio_data)} 字节")
        return audio_data