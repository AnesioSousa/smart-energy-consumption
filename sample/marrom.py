import socket

HOST = '127.0.0.1'
PORT = 8080

def handle_request(request):
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html\r\n"
    response += "\r\n"
    response += "<html><body><h1>Hello, world!</h1></body></html>"
    return response

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    continue
                request = data.decode()
                print(f"Request:\n{request}")
                response = handle_request(request)
                conn.sendall(response.encode())
                print(f"Response:\n{response}")

if __name__ == '__main__':
    run_server()
