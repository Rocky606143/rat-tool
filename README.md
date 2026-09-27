# Remote Support Tool (RAT)

A consent-based remote support agent for IT/admin management.

## Features

- **Secure**: TLS encrypted communication
- **Token Authentication**: Shared secret token validation
- **Command Allowlist**: Only safe commands can be executed (hostname, whoami, uptime, uname, ls, pwd)
- **Audit Logging**: All actions logged locally
- **Easy Setup**: One-liner setup script

## Quick Start

### 1. Setup (one time)

```bash
chmod +x setup.sh
./setup.sh
```

This creates:
- `~/remote_support/logs/` directory
- SSL certificates in `~/remote_support/`

### 2. Run Server (Terminal 1)

```bash
REMOTE_TOKEN="super-secure-token" python server.py
```

You should see:
```
Listening on 0.0.0.0:9000
```

### 3. Run Agent (Terminal 2)

```bash
REMOTE_TOKEN="super-secure-token" REMOTE_HOST="127.0.0.1" python agent.py
```

Agent will connect and wait for commands.

## Usage

### Send Command from Server

Add this to `server.py` or create an interactive CLI:

```python
from server import send_command

# Send command to a connected client
result = send_command("hostname-of-device", "whoami")
print(result)
```

## Configuration

Environment variables:

- `REMOTE_TOKEN` - Shared authentication token (required)
- `REMOTE_HOST` - Server IP/hostname (agent only, default: 127.0.0.1)
- `REMOTE_PORT` - Port to use (default: 9000)

## Logs

Logs are stored in:
- `~/remote_support/logs/server.log` - Server events
- `~/remote_support/logs/agent.log` - Agent events

## Allowed Commands

Currently allowed:
- `hostname` - Get device hostname
- `whoami` - Get current user
- `uptime` - Get system uptime
- `uname -a` - Get system info
- `ls` - List files
- `pwd` - Get current directory

To add more commands, edit the `allowed_command()` function in `agent.py`.

## Security Notes

⚠️ **For Testing Only**:
- Uses self-signed certificates
- No mTLS validation
- Token stored in environment variable

**For Production**:
- Use proper PKI certificates
- Enable mTLS validation
- Use JWT or OAuth tokens
- Implement command approval workflow
- Add user consent prompts on managed devices
- Restrict to specific admin users

## Files

- `common.py` - Shared utilities (JSON serialization, logging)
- `server.py` - Central control server
- `agent.py` - Client agent installed on managed devices
- `setup.sh` - One-time setup script
