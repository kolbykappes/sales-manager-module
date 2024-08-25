from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime, timezone
from .user import User
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
import uuid

class Campaign(Document):
    """
    Campaign document model for MongoDB.
    """
    campaign_id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_name = StringField(required=True, max_length=200)
    campaign_context = StringField(required=True)
    campaign_template_body = StringField(required=True)
    campaign_template_title = StringField(required=True, max_length=200)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    user = ReferenceField(User, required=True)

    meta = {'collection': 'campaigns'}

class CampaignCreate(BaseModel):
    """
    Pydantic model for campaign creation.
    """
    campaign_name: str = Field(..., max_length=200)
    campaign_context: str
    campaign_template_body: str
    campaign_template_title: str = Field(..., max_length=200)
    user: str  # This will be the user_id

class CampaignResponse(BaseModel):
    """
    Pydantic model for campaign response.
    """
    campaign_id: str
    campaign_name: str
    campaign_context: str
    campaign_template_body: str
    campaign_template_title: str
    created_at: datetime
    updated_at: datetime
    user: str  # This will be the user_id

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

    @classmethod
    def from_mongo(cls, campaign: Campaign) -> 'CampaignResponse':
        """
        Create a CampaignResponse instance from a Campaign document.
        
        Args:
            campaign (Campaign): The Campaign document to convert.
        
        Returns:
            CampaignResponse: The created CampaignResponse instance.
        """
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

class CampaignUpdate(BaseModel):
    """
    Pydantic model for campaign update.
    """
    campaign_name: str | None = Field(None, max_length=200)
    campaign_context: str | None = None
    campaign_template_body: str | None = None
    campaign_template_title: str | None = Field(None, max_length=200)
