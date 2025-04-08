#!/usr/bin/env python3
"""
proxy.py - Traffic redirector / MITM proxy module.

This module implements a basic TCP proxy that listens on a specified local port
and forwards all traffic to a remote target. It supports bidirectional data transfer.
"""

import socket
import threading
import sys
from core.utils import setup_logger, validate_port

logger = setup_logger("SocketShroud:Proxy")

def forward(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    except Exception as e:
        logger.error(f"Forwarding error: {e}")

def handle_client(client_socket, remote_host, remote_port):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
    except Exception as e:
        logger.error(f"Could not connect to {remote_host}:{remote_port} - {e}")
        client_socket.close()
        return

    t1 = threading.Thread(target=forward, args=(client_socket, remote_socket))
    t2 = threading.Thread(target=forward, args=(remote_socket, client_socket))
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    client_socket.close()
    remote_socket.close()

def start_proxy(listen_port: int, remote_host: str, remote_port: int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', listen_port))
    server.listen(5)
    logger.info(f"Proxy listening on 0.0.0.0:{listen_port} forwarding to {remote_host}:{remote_port}")
    try:
        while True:
            client_socket, addr = server.accept()
            logger.info(f"Accepted connection from {addr[0]}:{addr[1]}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        logger.info("Proxy shutting down.")
        server.close()

def main():
    if len(sys.argv) != 4:
        print("Usage: proxy.py <listen_port> <remote_host> <remote_port>")
        sys.exit(1)
    listen_port = validate_port(sys.argv[1])
    remote_host = sys.argv[2]
    remote_port = validate_port(sys.argv[3])
    start_proxy(listen_port, remote_host, remote_port)

if __name__ == "__main__":
    main()
    logger.info("Starting proxy...")