import os


def system_folder_initialize():
    """
    系统文件夹创建
    :return: pass
    """
    system_folder_lis =[
        "./temp/logs",
        "./temp",
        "./temp/tts",
        "./temp/asr"
    ]

    for system_folder in system_folder_lis:
        if not os.path.exists(system_folder):
            os.makedirs(system_folder)


def initialize_trigger():
    """
    执行服务的初始化
    :return: pass
    """
    system_folder_initialize()
