class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

class UploadFile:
    def __init__(self, file):
        self.file = file
    async def read(self):
        return self.file.read()

def File(*args, **kwargs):
    return None

class FastAPI:
    def __init__(self):
        self.routes = {}
    def add_middleware(self, *args, **kwargs):
        # Middleware is ignored in this lightweight implementation
        pass
    def post(self, path):
        def decorator(func):
            self.routes[("post", path)] = func
            return func
        return decorator

    def get(self, path):
        def decorator(func):
            self.routes[("get", path)] = func
            return func
        return decorator

    def websocket(self, path):
        def decorator(func):
            self.routes[("websocket", path)] = func
            return func
        return decorator

    def include_router(self, router):
        self.routes.update(router.routes)

class APIRouter:
    def __init__(self):
        self.routes = {}
    def websocket(self, path):
        def decorator(func):
            self.routes[("websocket", path)] = func
            return func
        return decorator

class WebSocketDisconnect(Exception):
    pass

class WebSocket:
    def __init__(self):
        self._recv = []
        self._send = []
    async def accept(self):
        pass
    async def receive_bytes(self):
        if not self._recv:
            raise WebSocketDisconnect()
        data = self._recv.pop(0)
        if data is None:
            raise WebSocketDisconnect()
        return data
    async def send_json(self, data):
        self._send.append(data)

from .responses import JSONResponse
from .testclient import TestClient
from .middleware import CORSMiddleware
