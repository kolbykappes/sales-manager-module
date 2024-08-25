from mongoengine import Document, StringField, DateTimeField
import uuid

class User(Document):
    user_id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    username = StringField(required=True, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    last_login = DateTimeField()

    meta = {'collection': 'users'}
