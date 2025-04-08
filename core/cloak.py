#!/usr/bin/env python3
"""
cloak.py - Socket cloaking module.

This module cloaks (hides) traffic on a given TCP port using iptables.
It adds rules to drop both outgoing and incoming packets for the specified port.
Requires root privileges.
"""

import sys
import subprocess
from core.utils import setup_logger, validate_port

logger = setup_logger("SocketShroud:Cloak")

def cloak_port(port: int):
    try:
        logger.info(f"Applying cloak rules for TCP port {port}...")

        # Remove existing rules for idempotency (optional, uncomment if needed)
        subprocess.run(f"iptables -D OUTPUT -p tcp --dport {port} -j DROP".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(f"iptables -D INPUT -p tcp --sport {port} -j DROP".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Drop outgoing traffic on the specified port.
        cmd_out = ["iptables", "-A", "OUTPUT", "-p", "tcp", "--dport", str(port), "-j", "DROP"]
        # Drop incoming traffic from the specified port.
        cmd_in = ["iptables", "-A", "INPUT", "-p", "tcp", "--sport", str(port), "-j", "DROP"]

        subprocess.run(cmd_out, check=True)
        subprocess.run(cmd_in, check=True)
        logger.info(f"[+] Port {port} cloaked successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error applying iptables rules: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: cloak.py <port>")
        sys.exit(1)
    try:
        port = validate_port(sys.argv[1])
    except ValueError as ve:
        logger.error(ve)
        sys.exit(1)
    cloak_port(port)
    logger.info("Cloaking complete.")