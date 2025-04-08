#!/usr/bin/env bash
#
# socketshroud.sh - SocketShroud main launcher script.
# Requires root. Sets up a Python virtual environment and dispatches module commands.
#

if [[ $EUID -ne 0 ]]; then
  echo "[-] Please run as root (sudo). Exiting."
  exit 1
fi

# Check for required commands
for cmd in iptables python3; do
  if ! command -v "$cmd" &> /dev/null; then
    echo "[-] $cmd is not installed. Please install $cmd."
    exit 1
  fi
done

# Set up Python virtual environment if not present
if [ ! -d "./venv" ]; then
  echo "[+] Setting up Python virtual environment..."
  if ! python3 -m venv venv; then
    echo "[-] Failed to create virtual environment"
    exit 1
  fi
  if ! ./venv/bin/pip install --upgrade pip; then
    echo "[-] Failed to upgrade pip"
    exit 1
  fi
  # Install required Python modules for SocketShroud core
  if ! ./venv/bin/pip install scapy psutil netifaces rich; then
    echo "[-] Failed to install required packages"
    exit 1
  fi
fi

# Usage check and dispatch
MODE="$1"
TARGET="$2"
shift 2

case "$MODE" in
  recon)
    ./venv/bin/python core/recon.py "$@"
    ;;
  cloak)
    if [ -z "$TARGET" ]; then
      echo "Usage: $0 cloak <port>"
      exit 1
    fi
    ./venv/bin/python core/cloak.py "$TARGET"
    ;;
  hijack)
    ./venv/bin/python core/hijack.py "$@"
    ;;
  proxy)
    if [ "$#" -ne 2 ]; then
      echo "Usage: $0 proxy <listen_port> <remote_target:remote_port>"
      exit 1
    fi
    LISTEN_PORT="$1"
    REMOTE_INFO="$2"
    REMOTE_HOST=$(echo "$REMOTE_INFO" | cut -d':' -f1)
    REMOTE_PORT=$(echo "$REMOTE_INFO" | cut -d':' -f2)
    ./venv/bin/python core/proxy.py "$LISTEN_PORT" "$REMOTE_HOST" "$REMOTE_PORT"
    ;;
  decoy)
    ./venv/bin/python core/decoy.py "$TARGET"
    ;;
  *)
    echo "Usage: $0 [recon|cloak|hijack|proxy|decoy] <target> [options]"
    exit 1
    ;;
esac
