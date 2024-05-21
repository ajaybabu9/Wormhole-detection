#!/usr/bin/env python3

import os, sys
import time
from socket import gethostname, gethostbyname, getaddrinfo
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from socket import socket

# Parse server details
if len(sys.argv) == 4:
    host_ip = sys.argv[1]
    cport = int(sys.argv[2])
    file_path = os.path.join("/", sys.argv[3])
else:
    host_ip = "localhost"
    cport = 8080
    file_path = "/"

# Initialize a connection to server
with socket(AF_INET, SOCK_STREAM) as csock:
    start_time = time.time()

    csock.connect((host_ip, cport))
    csock.send(f"GET {file_path} HTTP/1.1".encode())

    # Response Code
    data = csock.recv(4096)
    print(str(data, "utf-8"), end="")

    while True:
        data = csock.recv(4096)
        if not data:
            break
        print(str(data, "utf-8"), end="")

    print("RTT calculated:", f"{(time.time() - start_time) * 1e3:.4f} ms")
    print("Server :", csock, "\n")
