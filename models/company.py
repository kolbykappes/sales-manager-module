from mongoengine import Document, StringField, ReferenceField
from .user import User

class Company(Document):
    name = StringField(required=True)
    website = StringField()
    primary_industry = StringField()
    primary_sub_industry = StringField()
    zoom_id = StringField(required=True, unique=True)
    user = ReferenceField(User, required=True)

    meta = {'collection': 'companies'}
