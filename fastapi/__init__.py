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

from .responses import JSONResponse
from .testclient import TestClient
from .middleware import CORSMiddleware
