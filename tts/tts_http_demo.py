import base64
import json
import logging
import os
import time
import uuid
import requests
from dotenv import load_dotenv
log = logging.getLogger("uvicorn")


def audio_synthetic(text):
    """
    服务启动与关闭触发方法
    :param text: 文本信息
    :return: 文本信息转换成的音频文件本地路径
    """
    appid = os.environ.get('TTS.APPID')
    # 项目的 token
    access_token = os.environ.get('TTS.ACCESS_TOKEN')
    # 请求的集群
    cluster = os.environ.get('TTS.CLUSTER')
    # 填写平台申请的appid, access_token以及cluster
    voice_type = os.environ.get('TTS.VOICE_TYPE')
    host = os.environ.get('TTS.HOST')
    api_url = f"https://{host}/api/v1/tts"
    header = {"Authorization": f"Bearer;{access_token}"}

    request_json = {
        "app": {
            "appid": appid,
            "token": "access_token",
            "cluster": cluster
        },
        "user": {
            "uid": "388808087185088"
        },
        "audio": {
            "voice_type": voice_type,
            "language": "zh_taipu",
            "emotion": "sad",
            "encoding": "mp3",
            "speed_ratio": 1.0,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"

        }
    }
    timestamp_milliseconds = int(time.time() * 1000)
    path = str(timestamp_milliseconds) + ".mp3"
    path = os.path.join("./temp/tts", path)
    try:
        resp = requests.post(api_url, json.dumps(request_json), headers=header)
        if resp.status_code == 200:
            if "data" in resp.json():
                data = resp.json()["data"]
                file_to_save = open(path, "wb")
                file_to_save.write(base64.b64decode(data))
                log.info("TTS服务,已缓存当前回复音频文件:" + path)
        else:
            path = None
            log.error("TTS服务,请求失败")
    except Exception as e:
        log.error(e)
        path = None
        log.error("TTS服务,服务连接失败")
    return path

if __name__ == '__main__':
    load_dotenv("../.env")
    result_path = audio_synthetic("我没有听到你说了什么，请再说一遍吧")
    print(result_path)