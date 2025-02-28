import os

from dotenv import load_dotenv
from pydub import AudioSegment

from asr.baidu.aip.speech import AipSpeech

client = None

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def asr_path(audio_path, audio_format="wav"):
    # 识别本地文件
    o = {
        'dev_pid': 1537,
    }
    de = get_file_content(audio_path)
    return asr(de, audio_format)


def asr_change_rate(audio_path, audio_format="wav"):
    # 识别本地文件
    audio = AudioSegment.from_file(audio_path)
    # 设置采样率为 16000 Hz，声道数为 1（单声道），采样格式为 16 位
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)  # 16 位 = 2 字节

    audio_bytes = audio.raw_data
    return asr(audio_bytes, audio_format)


def asr(audio: bytes, audio_format="wav"):
    global client
    options = {
        'dev_pid': 1537,
    }

    if client is None:
        APP_ID = os.environ.get('BAIDU.STT.APP_ID')
        API_KEY = os.environ.get('BAIDU.STT.ACCESS_TOKEN')
        SECRET_KEY = os.environ.get('BAIDU.STT.SECRET_KEY')
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    aaa = client.asr(speech=audio, format=audio_format, rate=16000, options=options)
    return aaa["result"][0]


def test_main():
    audio_file = "D:\Application\system\Desktop\\audio_2.wav"
    audio = AudioSegment.from_file(audio_file)
    # 设置采样率为 16000 Hz，声道数为 1（单声道），采样格式为 16 位
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)  # 16 位 = 2 字节

    audio_bytes = audio.raw_data
    ss = asr(audio_bytes)
    # ss = asr_path(audio_file)
    print(ss)


if __name__ == '__main__':
    load_dotenv("../../.env")
    test_main()
