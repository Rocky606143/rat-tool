import os
import ssl
import socket
import socketserver
import threading
import json
import time
from pathlib import Path

from common import TOKEN, recv_json, send_json, ensure_dirs

HOST = os.environ.get("REMOTE_HOST", "0.0.0.0")
PORT = int(os.environ.get("REMOTE_PORT", "9000"))

clients = {}
lock = threading.Lock()

def log_event(msg):
    ensure_dirs()
    path = Path.home() / "remote_support" / "logs" / "server.log"
    with path.open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")

class ThreadedTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

class RemoteHandler(socketserver.BaseRequestHandler):
    def handle(self):
        sock = self.request
        try:
            hello = recv_json(sock)
            if not hello:
                return
            if hello.get("token") != TOKEN:
                send_json(sock, {"type": "error", "message": "bad token"})
                return

            client_id = hello.get("hostname", "unknown")
            with lock:
                clients[client_id] = {"sock": sock, "hostname": client_id}

            send_json(sock, {"type": "welcome", "message": "connected"})
            log_event(f"client connected: {client_id}")

            while True:
                msg = recv_json(sock)
                if not msg:
                    break
                if msg.get("type") == "result":
                    log_event(f"result from {client_id}: {msg}")
                elif msg.get("type") == "pong":
                    log_event(f"pong from {client_id}")
        except Exception as e:
            log_event(f"handler error: {e}")
        finally:
            with lock:
                for key, val in list(clients.items()):
                    if val["sock"] is sock:
                        del clients[key]

def send_command(hostname, cmd):
    with lock:
        client = clients.get(hostname)
    if not client:
        return {"status": "not_found"}
    try:
        send_json(client["sock"], {"type": "command", "cmd": cmd})
        return {"status": "sent"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    ensure_dirs()
    server = ThreadedTCPServer((HOST, PORT), RemoteHandler)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cert_path = str(Path.home() / "remote_support" / "cert.pem")
    key_path = str(Path.home() / "remote_support" / "key.pem")
    context.load_cert_chain(cert_path, key_path)
    server.socket = context.wrap_socket(server.socket, server_side=True)

    print(f"Listening on {HOST}:{PORT}")
    log_event("server started")
    try:
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        print("Server stopped")
        log_event("server stopped")

if __name__ == "__main__":
    main()
