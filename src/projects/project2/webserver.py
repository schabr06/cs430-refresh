"""Python Web server implementation"""
from logging import NOTSET
from socket import  socket, SOL_SOCKET, SO_REUSEADDR, AF_INET, SOCK_STREAM
import logging
import os, time
from datetime import datetime

ADDRESS = "127.0.0.2"  # Local client is going to be 127.0.0.1
PORT = 4300  # Open http://127.0.0.2:4300 in a browser
LOGFILE = "webserver.log"

def main():
    """Main loop"""
    with socket(AF_INET, SOCK_STREAM) as server_sock:
        server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_sock.bind((ADDRESS, PORT))
        while True:
            server_sock.listen(1)
            conn, addr = server_sock.accept()
            request = conn.recv(2048).decode()
            headers = request_parser(request)
            if headers.get('method') == 'GET':
                logger.info("",extra=headers)
                response = response_header('GET', headers.get('GET')).encode()
                conn.send(response)
            elif headers.get('method') == 'POST':
                logger.info("",extra=headers)
                response = response_header('POST', headers.get('POST')).encode()
                conn.send(response)
            else:
                keys = headers.keys()
                method_key = (list(keys))[0]
                headers['method'] = headers[method_key]
                logger.info("",extra=headers)
                response = response_header(method_key, headers.get(f'{method_key}')).encode()
                conn.send(response)

def request_parser(req):
    parsed_dict = {}
    req = req.split(f"\r\n")
    for i in req:
        if i.find(':') == -1:
            local = i.split(" ")
            if local[0]:
                parsed_dict['request'] = local[1]
                parsed_dict['method'] = local[0]
                parsed_dict[local[0]] = local[1]
            else:
                pass
        else:
            local = i.split(":")
            if local[0] == 'User-Agent':
                parsed_dict['User_Agent'] = local[1].strip()
            elif local[1]:
                parsed_dict[local[0]] = local[1].strip()
            else:
                pass
    return parsed_dict

def response_header(method, file):
    today = datetime.now().strftime('%c')
    headers = ''
    if method == 'POST':
        message = "<!DOCTYPE html><html><head></head><body>Method not allowed, try a GET request instead</body></html>"
        headers += 'HTTP/1.1 405 Method Not Allowed\r\n'
        headers += 'Content-Type: text/html; charset=utf-8\r\n'
        headers += f'Content-Length: {len(message)}\r\n'
        headers += f'Date: {today}\r\n'
        headers += 'Server: CS430-Brent\r\n'
        headers += '\r\n'
        headers += '\r\n'
        headers += f'{message}'
    elif method != 'GET':
        message = (f"<!DOCTYPE html><html><head></head><body><h3>Whoops</h3><p>We're sorry, the method: {method} is not implemented. Try using the GET method instead</p></body></html>")
        headers += 'HTTP/1.1 501 Not Implemented\r\n'
        headers += 'Content-Type: text/html; charset=utf-8\r\n'
        headers += f'Content-Length: {len(message)}\r\n'
        headers += f'Date: {today}\r\n'
        headers += 'Server: CS430-Brent\r\n'
        headers += '\r\n'
        headers += '\r\n'
        headers += f'{message}'
    elif file != '/alice30.txt':
        message = (f"<!DOCTYPE html><html><head></head><body><h3>Whoops</h3><p>We're sorry, the file {file} doesn't exist. Try searching the url for /alice30.txt</p></body></html>")
        headers += 'HTTP/1.1 404 Not Found\r\n'
        headers += 'Content-Type: text/html; charset=utf-8\r\n'
        headers += f'Content-Length: {len(message)}\r\n'
        headers += f'Date: {today}\r\n'
        headers += 'Server: CS430-Brent\r\n'
        headers += '\r\n'
        headers += '\r\n'
        headers += f'{message}'
    else:
        file = open('alice30.txt', 'r')
        content = file.read()
        time.ctime(os.path.getmtime('alice30.txt'))
        headers += 'HTTP/1.1 200 OK\r\n'
        headers += 'Content-Type: text/plain; charset=utf-8\r\n'
        headers += f'Content-Length: {len(content)}\r\n'
        headers += f'Date: {today}\r\n'
        headers += f'Last-Modified: {time.ctime(os.path.getmtime("alice30.txt"))}\r\n'
        headers += 'Server: CS430-Brent\r\n'
        headers += '\r\n'
        headers += f'{content}'
    return headers

if __name__ == "__main__":
    logger = logging.getLogger("root")
    formatter = '%(asctime)s.%(msecs)06d | %(request)s | %(Host)s | %(User_Agent)s' 
    logging.basicConfig(format=formatter,datefmt='%Y-%m-%d %H:%M:%S',filename=LOGFILE, level=NOTSET)
    main()