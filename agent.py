import os
import ssl
import socket
import subprocess
import json
import time
from pathlib import Path

from common import TOKEN, recv_json, send_json, ensure_dirs

HOST = os.environ.get("REMOTE_HOST", "127.0.0.1")
PORT = int(os.environ.get("REMOTE_PORT", "9000"))

def log_event(msg):
    ensure_dirs()
    path = Path.home() / "remote_support" / "logs" / "agent.log"
    with path.open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")

def allowed_command(cmd):
    allowed = {
        "hostname",
        "whoami",
        "uptime",
        "uname -a",
        "ls",
        "pwd",
    }
    return cmd in allowed if cmd else False

def run_command(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=20
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        return {"exit_code": 1, "stdout": "", "stderr": str(e)}

def main():
    log_event("agent starting")
    while True:
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((HOST, PORT), timeout=10) as raw:
                with context.wrap_socket(raw, server_hostname=HOST) as sock:
                    hello = {
                        "type": "hello",
                        "token": TOKEN,
                        "hostname": socket.gethostname(),
                    }
                    send_json(sock, hello)
                    log_event(f"connected to {HOST}:{PORT}")

                    while True:
                        msg = recv_json(sock)
                        if not msg:
                            break

                        if msg.get("type") == "command":
                            cmd = msg.get("cmd")
                            if not allowed_command(cmd):
                                send_json(sock, {
                                    "type": "error",
                                    "message": "Command not allowed",
                                    "cmd": cmd
                                })
                                log_event(f"blocked command: {cmd}")
                                continue

                            response = run_command(cmd)
                            send_json(sock, {
                                "type": "result",
                                "cmd": cmd,
                                "result": response,
                            })
                            log_event(f"executed: {cmd}")

                        elif msg.get("type") == "ping":
                            send_json(sock, {"type": "pong"})
                        elif msg.get("type") == "bye":
                            return

                        time.sleep(0.2)

        except Exception as e:
            log_event(f"connection error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
