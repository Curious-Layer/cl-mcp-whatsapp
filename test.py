from server import call_tool

print(
    call_tool(
        "send_whatsapp_message",
        {
            "access_token": "dummy-token",
            "phone_number_id": "dummy-id",
            "to": "919999999999",
            "message": "Hello from CL-WhatsApp MCP"
        }
    )
)

print(
    call_tool(
        "send_whatsapp_template",
        {
            "access_token": "dummy-token",
            "phone_number_id": "dummy-id",
            "to": "919999999999",
            "template_name": "hello_world"
        }
    )
)
