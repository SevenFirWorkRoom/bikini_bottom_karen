import logging
from fastapi import WebSocket, APIRouter
from server.chat_utils import chatchat


log = logging.getLogger("uvicorn")
sys_router = APIRouter(tags=["ws长连接"])


class WebSocketServer:
    def __init__(self):
        # 存储所有连接的客户端
        self.clients = set()

    async def handle_client(self, websocket: WebSocket):
        # 新的客户端连接
        await websocket.accept()
        self.clients.add(websocket)
        log.info(f"客户端已经连接: {websocket.client}")
        try:
            while True:
                # 接收二进制消息
                message = await websocket.receive_bytes()
                # 处理前端音频，得到音频回复
                num = len(self.clients)
                audio_data = await chatchat(message, num)
                # 发送结果
                await websocket.send_bytes(audio_data)

        except Exception as e:
            log.error(f"客户端断开连接或发生错误: {e}")
        finally:
            # 移除断开的客户端
            self.clients.remove(websocket)
            log.error(f"客户端断开连接: {websocket.client}")


# 创建 WebSocketServer 实例
websocket_server = WebSocketServer()

# 定义 WebSocket 路由
@sys_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_server.handle_client(websocket)