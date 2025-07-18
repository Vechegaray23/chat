class JSONResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code

class RedirectResponse:
    def __init__(self, url, status_code=307):
        self.headers = {'Location': url}
        self.status_code = status_code
