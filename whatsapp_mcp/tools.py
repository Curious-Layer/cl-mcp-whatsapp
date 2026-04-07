import json
import logging
from typing import Optional

from fastmcp import FastMCP
from pydantic import Field

from whatsapp_mcp import service

logger = logging.getLogger("whatsapp-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool(
        name="health_check",
        description="Check server readiness and configured authentication mode.",
    )
    def health_check() -> str:
        try:
            return json.dumps(
                {
                    "status": "ok",
                    "server": "CL WhatsApp MCP Server",
                }
            )
        except Exception as e:
            logger.error(f"Failed health_check: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="test_connection",
        description="Test connection to WhatsApp Cloud API and verify phone number ID.",
    )
    def test_connection_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        phone_number_id: str = Field(
            description="Sender's WhatsApp Business Account phone number ID"
        ),
    ) -> str:
        try:
            result = service.test_connection(
                api_key=api_key, phone_number_id=phone_number_id
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"test_connection failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="send_text_message",
        description="Send a text message via WhatsApp Cloud API.",
    )
    def send_text_message_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        phone_number_id: str = Field(
            description="Sender's WhatsApp Business Account phone number ID"
        ),
        recipient_phone: str = Field(
            description="Recipient's phone number with country code, eg. 912345678900"
        ),
        message_text: str = Field(description="Text message content"),
    ) -> str:
        try:
            result = service.send_text_message(
                api_key=api_key,
                phone_number_id=phone_number_id,
                recipient_phone=recipient_phone,
                message_text=message_text,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"send_text_message failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="send_template_message",
        description="Send a template message via WhatsApp Cloud API.",
    )
    def send_template_message_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        phone_number_id: str = Field(
            description="Sender's WhatsApp Business Account phone number ID"
        ),
        recipient_phone: str = Field(
            description="Recipient's phone number with country code, eg. 912345678900"
        ),
        template_name: str = Field(description="Name of the approved template"),
        template_language_code: str = Field(
            default="en_US", description="Template language code (e.g., en_US, es_ES)"
        ),
        parameters: Optional[list] = Field(
            default=None,
            description="List of parameter values to populate template variables",
        ),
    ) -> str:
        try:
            result = service.send_template_message(
                api_key=api_key,
                phone_number_id=phone_number_id,
                recipient_phone=recipient_phone,
                template_name=template_name,
                template_language_code=template_language_code,
                parameters=parameters,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"send_template_message failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="send_media_message",
        description="Send a media message (image, video, audio, document) via WhatsApp Cloud API.",
    )
    def send_media_message_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        phone_number_id: str = Field(
            description="Sender's WhatsApp Business Account phone number ID"
        ),
        recipient_phone: str = Field(
            description="Recipient's phone number with country code, eg. 912345678900"
        ),
        media_type: str = Field(
            description="Type of media: image, video, audio, or document"
        ),
        media_url: str = Field(description="URL of the media file"),
        caption: Optional[str] = Field(
            default=None, description="Caption for image or video (optional)"
        ),
    ) -> str:
        try:
            result = service.send_media_message(
                api_key=api_key,
                phone_number_id=phone_number_id,
                recipient_phone=recipient_phone,
                media_type=media_type,
                media_url=media_url,
                caption=caption,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"send_media_message failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="get_message_attachment",
        description="Retrieve media URL for a message attachment from WhatsApp Cloud API.",
    )
    def get_message_attachment_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        media_id: str = Field(description="ID of the media attachment"),
    ) -> str:
        try:
            result = service.get_message_attachment(api_key=api_key, media_id=media_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"get_message_attachment failed: {e}")
            return json.dumps({"error": str(e)})
