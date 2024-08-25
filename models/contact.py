from mongoengine import Document, StringField, ReferenceField
from .user import User
from .company import Company

class Contact(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)
    title = StringField()
    zoom_id = StringField(required=True, unique=True)
    user = ReferenceField(User, required=True)
    company = ReferenceField(Company, required=True)

    meta = {'collection': 'contacts'}
