from mongoengine import Document, IntField, StringField, DateTimeField, ReferenceField
from datetime import datetime
from .user import User
from pydantic import BaseModel, Field
from typing import Optional

class Campaign(Document):
    campaign_id = IntField(required=True, unique=True)
    campaign_name = StringField(required=True, max_length=200)
    campaign_context = StringField(required=True)
    campaign_template_body = StringField(required=True)
    campaign_template_title = StringField(required=True, max_length=200)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User, required=True)

    meta = {'collection': 'campaigns'}

class CampaignCreate(BaseModel):
    campaign_id: int
    campaign_name: str = Field(..., max_length=200)
    campaign_context: str
    campaign_template_body: str
    campaign_template_title: str = Field(..., max_length=200)
    user: str  # This will be the user_id

class CampaignResponse(BaseModel):
    campaign_id: int
    campaign_name: str
    campaign_context: str
    campaign_template_body: str
    campaign_template_title: str
    created_at: datetime
    updated_at: datetime
    user: str  # This will be the user_id

    class Config:
        orm_mode = True
