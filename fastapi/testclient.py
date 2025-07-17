from . import UploadFile, HTTPException
import asyncio

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
