import datetime
import platform
import socket
import threading
import os
from http.client import BadStatusLine
import urllib.parse
from urllib.request import urlopen

from PIL import Image, ImageSequence

HOST = 'localhost'
PORT = 8080
DOCUMENT_ROOT = './www'  # root folder for static files


def handle_request(client_socket):
    try:
        print('New connection')
        version = None
        method = None
        uri = None
        fl = client_socket.makefile('rb')
        line = fl.readline().decode('utf-8')
        if not line:
            raise BadStatusLine(line)

        try:
            method, uri, version = line.split(None, 2)
        except ValueError:
            try:
                method, uri = line.split(None, 1)
            except ValueError:
                version = ''
        if not version.startswith('HTTP/'):
            raise BadStatusLine(line)

        if method in ['GET', 'HEAD']:
            uri = urllib.parse.urlparse(urllib.parse.unquote(uri)).path
            try:
                extension = os.path.basename(uri).split('.')[-1]
            except IndexError:
                extension = 'html'

            content_type = 'text/html'
            server = platform.system() + ' ' + platform.release() + ' ' + platform.version()

            if extension == 'js':
                content_type = 'text/javascript'
            elif extension == 'css':
                content_type = 'text/css'
            elif extension in ['jpg', 'jpeg']:
                content_type = 'image/jpeg'
            elif extension == 'png':
                content_type = 'image/png'
            elif extension == 'gif':
                content_type = 'image/gif'
            elif extension == 'swf':
                content_type = 'application/x-shockwave-flash'

            if os.path.isfile(f"{DOCUMENT_ROOT}{uri}"):
                if 'image' in content_type or extension == 'swf':
                    file = open(f"{DOCUMENT_ROOT}{uri}", 'rb').read()
                else:
                    file2 = ''
                    with open(f"{DOCUMENT_ROOT}{uri}", 'r', encoding='utf-8') as f:
                        file2 += f.read()
                    file = bytes(file2, encoding='utf-8')
            else:
                try:
                    file = bytes(open(f"{DOCUMENT_ROOT}{uri}/index.html").read(), encoding='utf-8')
                except FileNotFoundError:
                    error_req = f'HTTP/1.1 404 Not Found\r\n' \
                                f'Server: {server} \r\n\r\n'
                    client_socket.send(bytes(error_req, encoding='utf-8'))
                    return

            success_req = f'HTTP/1.1 200 OK\r\n' \
                          f'Data: {datetime.datetime.now()} \r\n' \
                          f'Server: {server} \r\n' \
                          f'Content-Length: {len(file)}\r\n' \
                          f'Content-Type:{content_type}\r\n' \
                          f'Connection: close \r\n\r\n'

            success_req = success_req.encode('utf-8')
            client_socket.send(success_req)
            client_socket.send(file)

        else:
            client_socket.send(b'HTTP/1.1 405 Method Not Allowed\r\n\r\n')

        return
    except Exception as e:
        print(e)
        client_socket.shutdown(socket.SHUT_RDWR)
        print('Exception')
    finally:
        print('Connection closed')
        client_socket.close()


def start_server():
    # 1. create sockets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. bind socket to address and port
    client_socket.bind((HOST, PORT))
    # 3. listen for incoming connections
    client_socket.listen(5)
    # 4. accept incoming connections
    # 3. in while loop create threads with function for handle_request
    while True:
        accepted_socket, addr = client_socket.accept()
        # 5. in while loop create threads with function for handle_request
        threading.Thread(target=handle_request, args=(accepted_socket,)).start()


if __name__ == "__main__":
    start_server()
