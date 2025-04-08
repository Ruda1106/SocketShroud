#!/usr/bin/env python3
"""
recon.py - Real-time socket recon and passive analysis.

This script lists current TCP/UDP connections along with process information.
It uses psutil to gather socket data and rich to output a formatted table.
"""

import psutil
from rich.console import Console
from rich.table import Table
from core.utils import setup_logger

logger = setup_logger("SocketShroud:Recon")
console = Console()

def list_sockets():
    table = Table(title="Active Socket Connections")
    table.add_column("Proto", style="cyan", no_wrap=True)
    table.add_column("Local Address", style="magenta")
    table.add_column("Remote Address", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("PID", style="red")
    table.add_column("Process", style="white")

    connections = psutil.net_connections(kind='inet')
    if not connections:
        logger.warning("No active connections found.")
        return

    for conn in connections:
        proto = "TCP" if conn.type == psutil.SOCK_STREAM else "UDP"
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
        # For listening sockets, remote address is empty
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "LISTEN"
        status = conn.status if conn.status else ""
        pid = str(conn.pid) if conn.pid else "N/A"
        try:
            proc_name = psutil.Process(conn.pid).name() if conn.pid else "N/A"
        except Exception:
            proc_name = "N/A"
        table.add_row(proto, laddr, raddr, status, pid, proc_name)
    console.print(table)

if __name__ == "__main__":
    logger.info("Starting Socket Recon...")
    list_sockets()
    logger.info("Recon complete.")
