import argparse
import os

from dotenv import load_dotenv

from server import ws_server_run

import uvicorn

from server.initialize_utils import initialize_trigger


def mian():
    # 执行项目启动前的初始化
    initialize_trigger()

    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="Example script to demonstrate command line arguments.")
    # 添加参数
    parser.add_argument('--active', type=str)
    # 解析命令行参数
    args = parser.parse_args()
    env_active = args.active
    if env_active is None:
        env_active = ""
    env_file = f'{env_active}.env'
    if os.path.exists(env_file):
        load_dotenv(env_file)
        uvicorn.run(ws_server_run(), host="0.0.0.0", port=9700, log_config="uvicorn_config.json",
                    use_colors=True,
                    loop="asyncio",
                    )
    else:
        raise Exception(".启动失败--env配置文件不存在")



if __name__ == "__main__":
    mian()