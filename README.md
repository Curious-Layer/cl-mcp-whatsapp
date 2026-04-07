Send and manage WhatsApp messages via the WhatsApp Cloud API.

A Model Context Protocol (MCP) server that exposes the WhatsApp Cloud API for sending messages, managing media, and handling message workflows.

---

## Overview

The WhatsApp MCP Server provides stateless, multi-user messaging capabilities:

- **Text messaging** - Send plain text messages to WhatsApp contacts
- **Template messages** - Send pre-approved message templates for bulk messaging
- **Media sharing** - Send images, videos, audio, and documents
- **Connection testing** - Verify API credentials and phone number configuration
- **Media retrieval** - Fetch attachment URLs from received messages

Perfect for:

- Building WhatsApp bot integrations
- Automated customer notifications
- Bulk messaging campaigns with templates
- Media-rich customer communications
- AI agent-powered WhatsApp workflows

---

## Tools

<details>
<summary><code>health_check</code> — Server readiness verification</summary>

Returns the current health status of the MCP server.

**Inputs:**

None

**Output:**

```json
{
  "status": "ok",
  "server": "CL WhatsApp MCP Server"
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/health_check
```

</details>

<details>
<summary><code>send_text_message</code> — Send a text message</summary>

Send a plain text message to a WhatsApp contact using the 24-hour customer service window or an active conversation thread.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `recipient_phone` (string, required) — Recipient's phone number with country code (e.g., `917823846641`)
- `message_text` (string, required) — Text content of the message

**Output:**

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "917823846641", "wa_id": "917823846641"}],
  "messages": [{"id": "wamid.xyz...", "message_status": "accepted"}]
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/send_text_message \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "recipient_phone": "917823846641",
    "message_text": "Hello from WhatsApp API!"
  }'
```

</details>

<details>
<summary><code>send_template_message</code> — Send a pre-approved template</summary>

Send a template message that has been pre-approved by WhatsApp. Templates have no delivery restrictions and work for cold outreach.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `recipient_phone` (string, required) — Recipient's phone number with country code
- `template_name` (string, required) — Name of the approved template (e.g., `hello_world`)
- `template_language_code` (string, optional, default: `en_US`) — Template language code (e.g., `en_US`, `es_ES`)
- `parameters` (array, optional) — List of parameter values to populate template variables

**Output:**

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "917823846641", "wa_id": "917823846641"}],
  "messages": [{"id": "wamid.xyz...", "message_status": "accepted"}]
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/send_template_message \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "recipient_phone": "917823846641",
    "template_name": "hello_world",
    "template_language_code": "en_US"
  }'
```

</details>

<details>
<summary><code>send_media_message</code> — Send image, video, audio, or document</summary>

Send media files to a WhatsApp contact using direct URLs (within 24-hour window or active thread).

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `recipient_phone` (string, required) — Recipient's phone number with country code
- `media_type` (string, required) — Type of media: `image`, `video`, `audio`, or `document`
- `media_url` (string, required) — Public URL of the media file
- `caption` (string, optional) — Caption text (image and video only)

**Output:**

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "917823846641", "wa_id": "917823846641"}],
  "messages": [{"id": "wamid.xyz...", "message_status": "accepted"}]
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/send_media_message \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "recipient_phone": "917823846641",
    "media_type": "image",
    "media_url": "https://example.com/image.jpg",
    "caption": "Check this out!"
  }'
```

</details>

<details>
<summary><code>test_connection</code> — Verify API credentials and phone number</summary>

Test your WhatsApp Cloud API connection and phone number configuration. Retrieves phone number details and quality rating.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID

**Output:**

```json
{
  "id": "1077755395418019",
  "display_phone_number": "+1 (555) 555-1234",
  "quality_rating": "GREEN"
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/test_connection \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019"
  }'
```

</details>

<details>
<summary><code>get_message_attachment</code> — Retrieve media URL</summary>

Fetch the download URL for media attachments from received messages (images, videos, documents, audio).

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `media_id` (string, required) — ID of the media attachment

**Output:**

```json
{
  "id": "media_id",
  "url": "https://media.graph.facebook.com/...",
  "media_product_type": "MESSAGES"
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/get_message_attachment \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "media_id": "12345"
  }'
```

</details>

---

## API Parameters Reference

<details>
<summary><strong>Phone Number Format</strong></summary>

WhatsApp phone numbers must include the country code without `+` or `0` prefix:

- Correct: `917823846641` (country code 91 = India)
- Correct: `14155552671` (country code 1 = US)
- Incorrect: `+917823846641`
- Incorrect: `07823846641`

</details>

<details>
<summary><strong>Message Status Codes</strong></summary>

Returned in the `message_status` field:

| Status | Meaning |
|--------|---------|
| `accepted` | Message accepted by WhatsApp, being processed |
| `held_for_quality_assessment` | Message held for quality check before delivery (may be delayed) |
| `paused` | Message delivery paused (usually due to quality issues or rate limits) |

</details>

<details>
<summary><strong>Media Types Supported</strong></summary>

| Type | Format | Max Size |
|------|--------|----------|
| `image` | JPG, PNG | 5 MB |
| `video` | MP4, 3GP | 16 MB |
| `audio` | MP3, OGG | 16 MB |
| `document` | PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT | 100 MB |

</details>

---

## Authentication Guide

<details>
<summary><strong>WhatsApp Business Account Setup</strong></summary>

All tools require a valid **WhatsApp Cloud API access token** and **Phone Number ID**. Here's how to obtain them:

### Step 1: Create Meta Business Account

1. Go to [Meta Business Manager](https://business.facebook.com)
2. Click **Create Account** and follow the setup wizard
3. Verify your business information

### Step 2: Create WhatsApp Business Account

1. In Business Manager, navigate to **WhatsApp** in the sidebar
2. Click **Create WhatsApp Business Account** or select existing one
3. Configure your business profile (name, description, phone number)
4. Get your **WhatsApp Business Account ID** (shown in setup panel)

### Step 3: Verify Phone Number

1. In WhatsApp settings, go to **Phone Numbers**
2. Add your business phone number
3. Complete verification steps (SMS or call)
4. Copy your **Phone Number ID** (required for all API calls)

### Step 4: Create Meta Developer App

1. Go to [Meta Developer Portal](https://developers.facebook.com)
2. Click **My Apps** → **Create App**
3. Choose **Business** type
4. Add **WhatsApp** use case
5. Connect your WhatsApp Business Account

### Step 5: Generate Permanent Access Token

1. In Business Manager, go to **System Users** (Settings → System Users)
2. Click **Add** and create a new system user
3. Select the user and click **Assign Assets**
4. Assign your app and WhatsApp Business Account
5. Click **Generate Token** for the system user
6. Add these scopes:
   - `whatsapp_business_management`
   - `whatsapp_business_messaging`
7. Copy and store the token securely

**Note:** Tokens expire periodically. Regenerate as needed from system user settings.

### Step 6: Get Credentials in .env

Store these in your `.env` file:

```env
WHATSAPP_API_KEY=YOUR_SYSTEM_USER_ACCESS_TOKEN
PHONE_NUMBER_ID=YOUR_PHONE_NUMBER_ID
WHATSAPP_BUSINESS_ACCOUNT_ID=YOUR_BUSINESS_ACCOUNT_ID
```

For detailed setup, refer to [WhatsApp Cloud API Getting Started Guide](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started).

</details>

---

## Message Delivery Rules

 **Important:** WhatsApp enforces strict message delivery policies:

### **24-Hour Customer Service Window**

- You can send **non-template messages** only if:
  - The user messaged you first (within last 24 hours), OR
  - You're replying in an active conversation thread

- After 24 hours with no user response, you **cannot** send text messages
- **Solution:** Use template messages (no restriction)

### **Template Messages (Unrestricted)**

- Pre-approved templates can be sent anytime
- No 24-hour window restriction
- Ideal for bulk campaigns and cold outreach

---

## Troubleshooting

<details>
<summary><strong>Common Issues & Solutions</strong></summary>

### **Error: "Object with ID does not exist"**

- **Cause:** Wrong `phone_number_id` or not linked to your access token
- **Solution:**
  1. Verify `phone_number_id` in WhatsApp Business Manager
  2. Confirm phone number is verified
  3. Check token has `whatsapp_business_messaging` scope

### **Message Accepted but Not Delivered**

- **Cause:** Outside 24-hour customer service window
- **Solution:**
  1. Ask user to message you first OR
  2. Use a template message instead
  3. Use `send_template_message` tool (unrestricted)

### **"Invalid Access Token" Error**

- **Cause:** Token expired or invalid
- **Solution:**
  1. Regenerate token in Business Manager
  2. Verify token has required scopes
  3. Check token is not revoked

### **"Invalid Recipient Phone Number"**

- **Cause:** Phone number format incorrect
- **Solution:**
  1. Use format: Country Code + Number (no + or 0)
  2. Example: `917823846641` (not `+917823846641`)
  3. Verify number is a valid WhatsApp user

### **Media URL Not Accessible**

- **Cause:** URL expired or requires authentication
- **Solution:**
  1. Ensure URL is publicly accessible
  2. Use direct media URLs (not requiring login)
  3. Check media file size is within limits

### **Rate Limit Exceeded**

- **Cause:** Too many API calls in short timeframe
- **Solution:**
  1. Implement exponential backoff retry logic
  2. Space out API calls
  3. Check rate limits in Meta Business settings

</details>

---

## Resources

<details>
<summary><strong>External Documentation</strong></summary>

- **[WhatsApp Cloud API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)** — Official API reference
- **[Getting Started Guide](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)** — Setup and first message
- **[Message Templates](https://developers.facebook.com/docs/whatsapp/message-templates/manage-templates)** — Template management
- **[Error Codes Reference](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes)** — API error codes
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — MCP framework specification

</details>

---
