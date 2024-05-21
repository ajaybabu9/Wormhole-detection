#!/usr/bin/env python3

import os, sys
import socket
import threading

if len(sys.argv) > 1:
    server_port = int(sys.argv[1])
else:
    server_port = 8080

def process_request(csock):
    print("Client:", "\n", csock)
    try:
        req = csock.recv(4096).decode().split("\r\n")
        req = req[0].split()
        if req[0] == "GET":
            file = os.path.join(os.getcwd(), req[1][1:])
            if os.path.exists(file):
                print("Client requested:", file)
                csock.send(b"HTTP/1.1 200 OK\r\n\r\n")
                f = open(file, "rb")
                csock.sendfile(f, 0)
                f.close()
                csock.send(b"\r\n")
            else:
                resp = b"HTTP/1.1 404 Not Found\r\n\r\n"
                resp += b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
                csock.send(resp)
        else:
            resp = b"HTTP/1.1 400 Bad Request\r\n\r\n"
            resp += b"<html><head></head><body><h1>400 Bad Request</h1></body></html>\r\n"
            csock.send(resp)
        csock.close()
    except Exception as err:
        print(err)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Development purposes
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(("localhost", server_port))
print(f"[+] Server listening at localhost:{server_port}", "\n")
sock.listen(22)

while True:
    csock, (_cip, _cport) = sock.accept()
    thread = threading.Thread(target=process_request, args=[csock])
    thread.start()
sock.close()
