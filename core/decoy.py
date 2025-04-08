#!/usr/bin/env python3
"""
decoy.py - Fake socket service responder.

This module creates a decoy (honeypot) service that listens on a specified port,
accepts incoming connections, and responds with a realistic banner.
"""

import socket
import threading
import sys
from core.utils import setup_logger, validate_port

logger = setup_logger("SocketShroud:Decoy")

BANNER = (
    "HTTP/1.1 401 Unauthorized\r\n"
    "WWW-Authenticate: Basic realm=\"Decoy Service\"\r\n"
    "Content-Length: 0\r\n"
    "\r\n"
).encode()

def handle_client(client_socket, addr):
    logger.info(f"Decoy: Connection received from {addr[0]}:{addr[1]}")
    try:
        client_socket.sendall(BANNER)
    except Exception as e:
        logger.error(f"Error sending banner to {addr}: {e}")
    finally:
        client_socket.close()

def start_decoy(listen_port: int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', listen_port))
    server.listen(5)
    logger.info(f"Decoy service active on port {listen_port}")
    try:
        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        logger.info("Decoy service shutting down.")
        server.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: decoy.py <listen_port>")
        sys.exit(1)
    port = validate_port(sys.argv[1])
    start_decoy(port)

if __name__ == "__main__":
    main()
    logger.info("Starting Decoy service...")