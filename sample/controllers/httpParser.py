from model.request import Request
from model.response import Response


class HttpParser:
    def __init__(self):
        pass

    def parse(self, method: str, url: str, httpVersion: str, headers: dict, body: dict):

        request = Request(method, url, httpVersion, headers, body)

        return request
