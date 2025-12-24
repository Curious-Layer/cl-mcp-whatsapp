# CL-WhatsApp

Stateless MCP Server for WhatsApp integrations.

This project exposes WhatsApp tools that can be used by an AI agent,
automation workflow, or client application using the Model Context Protocol (MCP).

---

## Features

- `send_whatsapp_message`
- `send_whatsapp_template`
- Fully stateless architecture
- Mock mode enabled (no WhatsApp API key required)
- Easy to switch to real WhatsApp Cloud API later

---

## Prerequisites

Make sure the following are installed:

- Python **3.10+**
- pip (comes with Python)

Check Python version:
```bash
python --version

Project Structure
pgsql
Copy code
CL-WhatsApp/
├── server.py
├── auth.py
├── requirements.txt
├── test.py
├── .env
└── tools/
    ├── schemas.py
    ├── handlers.py
    └── tool_registry.py
How to Run (Client Instructions)
Step 1️⃣ Navigate to Project Directory
bash
Copy code
cd CL-WhatsApp
Step 2️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
Step 3️⃣ Start the MCP Server
bash
Copy code
python server.py
Expected output:

text
Copy code
CL-WhatsApp MCP Server Ready
Step 4️⃣ Test the Tools (Mock Mode)
bash
Copy code
python test.py