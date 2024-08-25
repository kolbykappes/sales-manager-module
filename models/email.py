from mongoengine import Document, DictField, StringField, IntField, FloatField, DateTimeField
from datetime import datetime

class Email(Document):
    company = DictField(required=True)
    contact = DictField(required=True)
    subject = StringField(required=True)
    body = StringField(required=True)
    ai_model = StringField(required=True)
    tokens_sent = IntField(required=True)
    tokens_returned = IntField(required=True)
    generation_time = FloatField(required=True)
    campaign_id = IntField(required=True)
    full_prompt = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'emails'}
