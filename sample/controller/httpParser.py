from ..model import request as Request


class HttpParser:
    def __init__(self):
        pass

    def parse(self, method: str, url: str, httpVersion: str, headers: dict, body: dict):
        request = Request(method, url, httpVersion, headers, body)

        return request
