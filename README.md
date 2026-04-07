# CL WhatsApp MCP Server

Stateless Model Context Protocol (MCP) server scaffold for WhatsApp Cloud API.

This repository now follows the Curious Layer MCP architecture standard and is intentionally minimal.
Only the `health_check` tool is implemented for now.

## Authentication Mode

This server is designed for WhatsApp Cloud API calls using a **System User access token** (not OAuth).
Tenant-facing WhatsApp tools will accept auth input per call when they are added.

## Current Tools

- `health_check`: Returns server status and configured auth mode.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
# default transport
python server.py

# streamable-http example
python server.py --transport streamable-http --host 127.0.0.1 --port 8001
```

## Project Structure

```text
cl-mcp-whatsapp/
|-- server.py
|-- requirements.txt
|-- README.md
`-- whatsapp_mcp/
    |-- __init__.py
    |-- cli.py
    |-- config.py
    |-- schemas.py
    |-- service.py
    `-- tools.py
```

## Notes

- The server exports ASGI app at `/mcp` using streamable-http.
- Additional WhatsApp API tools will be added from your API docs in the next step.