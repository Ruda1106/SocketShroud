#!/usr/bin/env python3
"""
utils.py - Shared utilities for SocketShroud.
Provides logging configuration, argument validation, and helper functions.
"""

import logging
import sys

def setup_logger(name: str = "SocketShroud", level: int = logging.INFO):
    """Configure and return a logger."""
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(level)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def validate_port(port_str: str) -> int:
    """Validate and return a port number (integer)."""
    try:
        port = int(port_str)
        if port < 1 or port > 65535:
            raise ValueError("Port out of range")
    except ValueError as ve:
        raise ValueError(f"Invalid port number '{port_str}': {ve}")
    return port
