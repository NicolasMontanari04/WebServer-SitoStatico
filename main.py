import socket
import os
import mimetypes

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

ROOT = './www'

def get_mime_type(file_path):
    return mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

def handle_request(req):
    try:
        request = req.recv(1024).decode()
        if not request:
            return

        headers = request.split('\r\n')
        request_line = headers[0]
        print(f"[LOG] {request_line}")

        method, path, version = request_line.split()

        if method != 'GET':
            req.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            print(f"[LOG] returned 405 Method Not Allowed")
            return

        if path == '/':
            path = '/index.html'

        file_path = os.path.abspath(os.path.join(ROOT, path.lstrip('/')))

        # Prevent exit from ROOT
        if not file_path.startswith(os.path.abspath(ROOT)):
            response = "HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n<h1>403 Forbidden</h1>"
            print(f"[LOG] returned 403 Forbidden")
            req.sendall(response.encode())
            return

        # Get file
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            content_type = get_mime_type(file_path)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n"
            print(f"[LOG] returned 200 OK")
            req.sendall(response.encode() + content)
        else:
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>"
            req.sendall(response.encode())

    except Exception as e:
        print(f"[ERROR] {e}")
        req.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n<h1>500 Internal Server Error</h1>")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)

    while True:
        client_connection, client_address = server_socket.accept()
        handle_request(client_connection)


if __name__ == '__main__':
    start_server()