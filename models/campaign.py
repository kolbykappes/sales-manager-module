from mongoengine import Document, IntField, StringField, DateTimeField, ReferenceField
from datetime import datetime
from .user import User

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
