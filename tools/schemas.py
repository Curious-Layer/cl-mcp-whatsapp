from pydantic import BaseModel, Field

class SendWhatsAppMessageInput(BaseModel):
    access_token: str
    phone_number_id: str
    to: str
    message: str


class SendWhatsAppTemplateInput(BaseModel):
    access_token: str
    phone_number_id: str
    to: str
    template_name: str
    language_code: str = Field(default="en_US")
