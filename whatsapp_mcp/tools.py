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
        name="send_marketing_template_message",
        description="Send a marketing template message via WhatsApp Cloud API with optional policy and activity sharing controls.",
    )
    def send_marketing_template_message_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        phone_number_id: str = Field(
            description="Sender's WhatsApp Business Account phone number ID"
        ),
        recipient_phone: str = Field(
            description="Recipient's phone number with country code, eg. 912345678900"
        ),
        template_name: str = Field(
            description="Name of the approved marketing template"
        ),
        template_language_code: str = Field(
            default="en_US", description="Template language code (e.g., en_US, es_ES)"
        ),
        components: Optional[list] = Field(
            default=None,
            description="Array of template components containing the parameters of the message",
        ),
        product_policy: Optional[str] = Field(
            default=None,
            description="Optional product policy setting: CLOUD_API_FALLBACK or STRICT",
        ),
        message_activity_sharing: Optional[bool] = Field(
            default=None,
            description="Optional flag to control message activity sharing",
        ),
    ) -> str:
        try:
            result = service.send_marketing_template_message(
                api_key=api_key,
                phone_number_id=phone_number_id,
                recipient_phone=recipient_phone,
                template_name=template_name,
                template_language_code=template_language_code,
                components=components,
                product_policy=product_policy,
                message_activity_sharing=message_activity_sharing,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"send_marketing_template_message failed: {e}")
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

    @mcp.tool(
        name="get_message_history_events",
        description="Retrieve paginated message delivery status events from WhatsApp Cloud API.",
    )
    def get_message_history_events_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        message_history_id: str = Field(
            description="WhatsApp Business Message History ID"
        ),
        status_filter: Optional[str] = Field(
            default=None,
            description="Filter by delivery status (ACCEPTED, DELIVERED, ERROR, READ, SENT)",
        ),
        fields: Optional[str] = Field(
            default=None,
            description="Comma-separated list of fields (id, delivery_status, error_description, occurrence_timestamp, status_timestamp, application)",
        ),
        limit: int = Field(
            default=25,
            description="Maximum number of events per page (1-100)",
        ),
        after: Optional[str] = Field(
            default=None,
            description="Cursor for pagination to get next page",
        ),
        before: Optional[str] = Field(
            default=None,
            description="Cursor for pagination to get previous page",
        ),
    ) -> str:
        try:
            result = service.get_message_history_events(
                api_key=api_key,
                message_history_id=message_history_id,
                status_filter=status_filter,
                fields=fields,
                limit=limit,
                after=after,
                before=before,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"get_message_history_events failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="configure_conversational_automation",
        description="Configure conversational automation settings for WhatsApp Business Account phone number (welcome messages, prompts, bot commands).",
    )
    def configure_conversational_automation_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        phone_number_id: str = Field(
            description="Sender's WhatsApp Business Account phone number ID"
        ),
        enable_welcome_message: Optional[bool] = Field(
            default=None,
            description="Whether to enable welcome messages for new conversations",
        ),
        prompts: Optional[list] = Field(
            default=None,
            description="List of conversation prompts (ice breakers) to guide customer interactions",
        ),
        commands: Optional[list] = Field(
            default=None,
            description="List of bot commands. Each command should have 'command_name' and 'command_description' keys",
        ),
    ) -> str:
        try:
            result = service.configure_conversational_automation(
                api_key=api_key,
                phone_number_id=phone_number_id,
                enable_welcome_message=enable_welcome_message,
                prompts=prompts,
                commands=commands,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"configure_conversational_automation failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="get_bot_details",
        description="Retrieve WhatsApp Business Bot configuration details (id, prompts, commands, welcome message settings).",
    )
    def get_bot_details_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        bot_id: str = Field(description="WhatsApp Business Bot ID"),
        fields: Optional[str] = Field(
            default=None,
            description="Comma-separated list of fields to include (id, prompts, commands, enable_welcome_message)",
        ),
    ) -> str:
        try:
            result = service.get_bot_details(
                api_key=api_key,
                bot_id=bot_id,
                fields=fields,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"get_bot_details failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="check_call_permissions",
        description="Check whether you have permission to call a WhatsApp user and retrieve available actions.",
    )
    def check_call_permissions_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        phone_number_id: str = Field(
            description="Your WhatsApp Business Account phone number ID"
        ),
        user_wa_id: str = Field(
            description="The WhatsApp ID of the user to check call permissions for"
        ),
    ) -> str:
        try:
            result = service.get_call_permissions(
                api_key=api_key,
                phone_number_id=phone_number_id,
                user_wa_id=user_wa_id,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"check_call_permissions failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="manage_call",
        description="Manage WhatsApp calls - initiate, accept, reject, or terminate calls.",
    )
    def manage_call_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        phone_number_id: str = Field(
            description="Your WhatsApp Business Account phone number ID"
        ),
        action: str = Field(
            description="Call action: connect (initiate), pre_accept, accept, reject, or terminate"
        ),
        to: Optional[str] = Field(
            default=None,
            description="The WhatsApp number being called (required for connect/pre_accept/accept/reject)",
        ),
        call_id: Optional[str] = Field(
            default=None,
            description="The WhatsApp call ID (required for terminate action)",
        ),
        session: Optional[dict] = Field(
            default=None,
            description="Session description protocol (SDP) - dict with 'sdp_type' (offer/answer) and 'sdp' string",
        ),
        biz_opaque_callback_data: Optional[str] = Field(
            default=None,
            description="Arbitrary string for tracking purposes (max 512 characters)",
        ),
    ) -> str:
        try:
            result = service.manage_call(
                api_key=api_key,
                phone_number_id=phone_number_id,
                action=action,
                to=to,
                call_id=call_id,
                session=session,
                biz_opaque_callback_data=biz_opaque_callback_data,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"manage_call failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="get_qr_code",
        description="Retrieve details for a WhatsApp Message QR code including image URL for marketing.",
    )
    def get_qr_code_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        phone_number_id: str = Field(
            description="Your WhatsApp Business Account phone number ID"
        ),
        qr_code_id: str = Field(
            description="The unique 14-character identifier of the QR code"
        ),
        fields: Optional[str] = Field(
            default=None,
            description="Comma-separated fields (code, prefilled_message, deep_link_url, creation_time, qr_image_url.format(SVG|PNG))",
        ),
    ) -> str:
        try:
            result = service.get_qr_code(
                api_key=api_key,
                phone_number_id=phone_number_id,
                qr_code_id=qr_code_id,
                fields=fields,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"get_qr_code failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="delete_qr_code",
        description="Permanently delete a WhatsApp Message QR code. This action cannot be undone.",
    )
    def delete_qr_code_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        phone_number_id: str = Field(
            description="Your WhatsApp Business Account phone number ID"
        ),
        qr_code_id: str = Field(
            description="The unique 14-character identifier of the QR code to delete"
        ),
    ) -> str:
        try:
            result = service.delete_qr_code(
                api_key=api_key,
                phone_number_id=phone_number_id,
                qr_code_id=qr_code_id,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"delete_qr_code failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="get_whatsapp_business_profile",
        description="Retrieve WhatsApp Business Profile details including business information and configuration.",
    )
    def get_whatsapp_business_profile_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        business_profile_id: str = Field(
            description="Your WhatsApp Business Profile ID"
        ),
        fields: Optional[str] = Field(
            default=None,
            description="Comma-separated fields (id, account_name, description, email, about, address, vertical, websites, profile_picture_url, messaging_product)",
        ),
    ) -> str:
        try:
            result = service.get_whatsapp_business_profile(
                api_key=api_key,
                business_profile_id=business_profile_id,
                fields=fields,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"get_whatsapp_business_profile failed: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="update_whatsapp_business_profile",
        description="Update WhatsApp Business Profile information such as business name, description, contact details, and website URLs.",
    )
    def update_whatsapp_business_profile_tool(
        api_key: str = Field(description="WhatsApp Cloud API access token"),
        business_profile_id: str = Field(
            description="Your WhatsApp Business Profile ID"
        ),
        account_name: Optional[str] = Field(
            default=None,
            description="Name of the business account",
        ),
        description: Optional[str] = Field(
            default=None,
            description="Business description text",
        ),
        email: Optional[str] = Field(
            default=None,
            description="Contact email address",
        ),
        about: Optional[str] = Field(
            default=None,
            description="About section text",
        ),
        address: Optional[str] = Field(
            default=None,
            description="Physical address of the business",
        ),
        vertical: Optional[str] = Field(
            default=None,
            description="Industry vertical: UNDEFINED, OTHER, AUTO, BEAUTY, APPAREL, EDU, ENTERTAIN, EVENT_PLAN, FINANCE, GROCERY, GOVT, HOTEL, HEALTH, NONPROFIT, PROF_SERVICES, RETAIL, TRAVEL, RESTAURANT, NOT_A_BIZ",
        ),
        websites: Optional[list] = Field(
            default=None,
            description="List of website URLs associated with the business",
        ),
        profile_picture_handle: Optional[str] = Field(
            default=None,
            description="Handle of the profile picture from Resumable Upload API",
        ),
    ) -> str:
        try:
            result = service.update_whatsapp_business_profile(
                api_key=api_key,
                business_profile_id=business_profile_id,
                account_name=account_name,
                description=description,
                email=email,
                about=about,
                address=address,
                vertical=vertical,
                websites=websites,
                profile_picture_handle=profile_picture_handle,
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"update_whatsapp_business_profile failed: {e}")
            return json.dumps({"error": str(e)})
