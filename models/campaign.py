from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime
from .user import User
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
import uuid

class Campaign(Document):
    campaign_id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_name = StringField(required=True, max_length=200)
    campaign_context = StringField(required=True)
    campaign_template_body = StringField(required=True)
    campaign_template_title = StringField(required=True, max_length=200)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User, required=True)

    meta = {'collection': 'campaigns'}

class CampaignCreate(BaseModel):
    campaign_name: str = Field(..., max_length=200)
    campaign_context: str
    campaign_template_body: str
    campaign_template_title: str = Field(..., max_length=200)
    user: str  # This will be the user_id

class CampaignResponse(BaseModel):
    campaign_id: str
    campaign_name: str
    campaign_context: str
    campaign_template_body: str
    campaign_template_title: str
    created_at: datetime
    updated_at: datetime
    user: str  # This will be the user_id

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @classmethod
    def from_mongo(cls, campaign: Campaign):
        return cls(
            campaign_id=str(campaign.campaign_id),
            campaign_name=campaign.campaign_name,
            campaign_context=campaign.campaign_context,
            campaign_template_body=campaign.campaign_template_body,
            campaign_template_title=campaign.campaign_template_title,
            created_at=campaign.created_at,
            updated_at=campaign.updated_at,
            user=str(campaign.user.id)
        )
