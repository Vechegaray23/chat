from . import UploadFile, HTTPException, WebSocket
import asyncio
from urllib.parse import urlparse, parse_qs


class _WSSession:
    def __init__(self, handler, params):
        self.ws = WebSocket()
        self.handler = handler
        self.params = params
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.task = self.loop.create_task(self.handler(self.ws, **self.params))

    def send_bytes(self, data: bytes):
        self.ws._recv.append(data)
        self.loop.run_until_complete(asyncio.sleep(0))

    def receive_json(self):
        while not self.ws._send:
            self.loop.run_until_complete(asyncio.sleep(0))
        return self.ws._send.pop(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.ws._recv.append(None)
        self.loop.run_until_complete(self.task)
        self.loop.close()

class Response:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data
    def json(self):
        return self._data

class TestClient:
    def __init__(self, app):
        self.app = app
    def post(self, path, files=None):
        handler = self.app.routes.get(("post", path))
        if handler is None:
            raise Exception("Route not found")
        file_tuple = files.get("file")
        filename, fileobj, _ = file_tuple
        upload = UploadFile(fileobj)
        try:
            data = asyncio.run(handler(upload))
            if hasattr(data, 'content'):
                return Response(getattr(data, 'status_code', 200), data.content)
            return Response(200, data)
        except HTTPException as e:
            return Response(e.status_code, {"detail": e.detail})

    def get(self, path):
        handler = None
        params = {}
        for (method, route_path), func in self.app.routes.items():
            if method != "get":
                continue
            rp = route_path.strip("/").split("/")
            pp = path.strip("/").split("/")
            if len(rp) != len(pp):
                continue
            tmp_params = {}
            match = True
            for rseg, pseg in zip(rp, pp):
                if rseg.startswith("{") and rseg.endswith("}"):
                    tmp_params[rseg[1:-1]] = pseg
                elif rseg != pseg:
                    match = False
                    break
            if match:
                handler = func
                params = tmp_params
                break
        if handler is None:
            raise Exception("Route not found")
        try:
            data = asyncio.run(handler(**params))
            if hasattr(data, 'content'):
                return Response(getattr(data, 'status_code', 200), data.content)
            return Response(200, data)
        except HTTPException as e:
            return Response(e.status_code, {"detail": e.detail})

    def websocket_connect(self, path):
        url = urlparse(path)
        handler = self.app.routes.get(("websocket", url.path))
        if handler is None:
            raise Exception("Route not found")
        params = {k: v[0] for k, v in parse_qs(url.query).items()}
        return _WSSession(handler, params)
