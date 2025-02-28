from fastapi import FastAPI

from server.event_handlers import register_events
from server.ws_server import sys_router


def ws_server_run():
    app = FastAPI()

    app.include_router(sys_router)
    # 服务启动与关闭触发方法
    register_events(app)
    return app