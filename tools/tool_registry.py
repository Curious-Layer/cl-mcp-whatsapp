from tools.schemas import (
    SendWhatsAppMessageInput,
    SendWhatsAppTemplateInput
)
from tools.handlers import (
    send_whatsapp_message,
    send_whatsapp_template
)

TOOLS = {
    "send_whatsapp_message": {
        "schema": SendWhatsAppMessageInput,
        "handler": send_whatsapp_message,
        "description": "Send WhatsApp text message"
    },
    "send_whatsapp_template": {
        "schema": SendWhatsAppTemplateInput,
        "handler": send_whatsapp_template,
        "description": "Send WhatsApp template message"
    }
}
