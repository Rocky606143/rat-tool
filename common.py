import os
import socket
import ssl
import json
import time
from pathlib import Path

TOKEN = os.environ.get("REMOTE_TOKEN", "change-me-strong-token")

def send_json(sock, payload):
    data = json.dumps(payload).encode()
    sock.sendall(f"{len(data):<8}".encode() + data)

def recv_json(sock):
    header = sock.recv(8)
    if not header:
        return None
    try:
        length = int(header.decode("ascii", errors="ignore").strip())
    except ValueError:
        return None
    chunks = []
    remaining = length
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            break
        chunks.append(chunk)
        remaining -= len(chunk)
    if remaining != 0:
        return None
    try:
        return json.loads(b"".join(chunks).decode())
    except Exception:
        return None

def ensure_dirs():
    log_dir = Path.home() / "remote_support" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
