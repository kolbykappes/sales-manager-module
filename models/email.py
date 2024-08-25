from mongoengine import Document, DictField, StringField, IntField, FloatField, DateTimeField
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import Dict

class Email(Document):
    company = DictField(required=True)
    contact = DictField(required=True)
    subject = StringField(required=True)
    body = StringField(required=True)
    ai_model = StringField(required=True)
    tokens_sent = IntField(required=True)
    tokens_returned = IntField(required=True)
    generation_time = FloatField(required=True)
    full_prompt = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    campaign_id = StringField(required=True)

    meta = {'collection': 'emails'}

class EmailCreate(BaseModel):
    company: Dict[str, str]
    contact: Dict[str, str]
    subject: str
    body: str
    ai_model: str
    tokens_sent: int
    tokens_returned: int
    generation_time: float
    full_prompt: str
    campaign_id: str

class EmailResponse(BaseModel):
    id: str
    company: Dict[str, str]
    contact: Dict[str, str]
    subject: str
    body: str
    ai_model: str
    tokens_sent: int
    tokens_returned: int
    generation_time: float
    full_prompt: str
    created_at: datetime
    campaign_id: str

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

    @classmethod
    def from_mongo(cls, email: Email):
        return cls(
            id=str(email.id),
            company=email.company,
            contact=email.contact,
            subject=email.subject,
            body=email.body,
            ai_model=email.ai_model,
            tokens_sent=email.tokens_sent,
            tokens_returned=email.tokens_returned,
            generation_time=email.generation_time,
            full_prompt=email.full_prompt,
            created_at=email.created_at,
            campaign_id=email.campaign_id
        )

class EmailUpdate(BaseModel):
    subject: str | None = None
    body: str | None = None
    ai_model: str | None = None
    campaign_id: str | None = None
