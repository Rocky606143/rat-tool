# Remote Support Tool

A consent-based remote support agent for authorized IT administration and lab environments.

> **Important:** Use this project only on systems you own or are explicitly authorized to manage. It is not intended for covert access, persistence, credential theft, or unauthorized monitoring.

## Highlights

- 🔐 TLS-encrypted client/server communication
- 🎫 Shared-token authentication
- ✅ Allowlisted, read-only diagnostic commands
- 🧾 Local audit logging for server and agent activity
- ⚙️ Simple setup using a shell script
- 🐍 Lightweight Python implementation

## Project Layout

| File | Purpose |
| --- | --- |
| `server.py` | Runs the support server and handles connected agents |
| `agent.py` | Runs on an authorized managed device |
| `common.py` | Shared serialization and logging helpers |
| `setup.sh` | Creates the local support directories and test certificates |

## Requirements

- Python 3.9+
- OpenSSL
- Linux/macOS shell environment for `setup.sh`
- A network connection between the authorized server and agent

## Quick Start

### 1. Prepare the environment

```bash
chmod +x setup.sh
./setup.sh
```

The setup script creates `~/remote_support/`, its log directory, and local TLS certificates.

### 2. Start the server

In one terminal:

```bash
export REMOTE_TOKEN="replace-with-a-long-random-token"
python server.py
```

### 3. Start the agent

In a second terminal, on the authorized device:

```bash
export REMOTE_TOKEN="replace-with-the-same-token"
export REMOTE_HOST="127.0.0.1"
python agent.py
```

Set `REMOTE_HOST` to the server's address when the server and agent run on different machines. Do not expose the service to the public internet without adding suitable network controls and authentication.

## Configuration

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `REMOTE_TOKEN` | Yes | — | Shared authentication token |
| `REMOTE_HOST` | Agent only | `127.0.0.1` | Server hostname or IP address |
| `REMOTE_PORT` | No | `9000` | Listening/connection port |

Use a long, unique token and provide it through a secure secret-management method in real deployments. Never commit secrets to Git.

## Allowed Diagnostics

The agent currently restricts execution to these predefined commands:

- `hostname`
- `whoami`
- `uptime`
- `uname -a`
- `ls`
- `pwd`

Do not expand the allowlist to arbitrary shell input. Any additional command should be narrowly defined, validated, documented, and protected by an explicit approval workflow.

## Logs

Runtime logs are stored under:

- `~/remote_support/logs/server.log`
- `~/remote_support/logs/agent.log`

Protect these logs because they may contain hostnames, usernames, timestamps, and operational details.

## Security and Consent

This repository is intended for authorized support, testing, and educational use only. Before running an agent:

1. Obtain clear consent from the device owner or administrator.
2. Explain what information can be collected and which actions are available.
3. Provide a visible way to stop the agent.
4. Restrict network access to trusted hosts and networks.
5. Rotate tokens and certificates when access changes.
6. Review and retain audit logs according to your organization's policy.

The current setup uses self-signed certificates and environment-based token authentication. It is **not production-ready**. Before production use, add certificate validation or mTLS, stronger identity and authorization, secure secret storage, rate limiting, approval prompts, and comprehensive tests.

## Development Checklist

- [ ] Test only in an isolated lab or explicitly authorized environment
- [ ] Verify certificate validation and hostname checking
- [ ] Add an operator authentication and approval flow
- [ ] Add agent-side consent and stop controls
- [ ] Add automated tests and dependency pinning
- [ ] Review logs for sensitive data
- [ ] Run static analysis and security scanning

## License

No license has been declared yet. Add a license before distributing or accepting contributions.
