
class Request:
    def __init__(self, method: str, url: str, httpVersion: str, headers: dict, body: dict):
        self.method = method
        self.url = url
        self.httpVersion = httpVersion
        self.headers = headers
        self.body = body
        self.params = None
        self.data = None
        self.stream = None
        self.status_code = None
        self.content = None
        self.text = None
        self.json = None
        self.content_type = None
        self.elapsed = None
        self.start_time = None
        self.end_time = None

    def request_form(self):
        return f"\
                {self.method} {self.url} {self.httpVersion}\r\n\
                Host: {self.host}\r\n\
                User-Agent: {self.__str__}\r\n\
                Connection: close\r\n\
                \r\n\
                "

    def set_method(self, method: str):
        self.method = method
        return self

    def set_url(self, url: str):
        self.url = url
        return self

    def set_headers(self, headers: dict):
        self.headers = headers
        return self

    def set_params(self, params: dict):
        self.params = params
        return self

    def set_data(self, data: dict):
        self.data = data
        return self

    def set_stream(self, stream: bool):
        self.stream = stream
        return self

    def set_status_code(self, status_code: int):
        self.status_code = status_code
        return self

    def set_content(self, content: str):
        self.content = content
        return self

    def set_text(self, text: str):
        self.text = text
        return self

    def set_json(self, json: dict):
        self.json = json
        return self

    def set_content_type(self, content_type: str):
        self.content_type = content_type
        return self

    def set_elapsed(self, elapsed: float):
        self.elapsed = elapsed
        return self

    def set_start_time(self, start_time: float):
        self.start_time = start_time
        return self

    def set_end_time(self, end_time: float):
        self.end_time = end_time
        return self

    def get_method(self):
        return self.method

    def get_url(self):
        return self.url

    def get_httpVersion(self):
        return self.httpVersion
