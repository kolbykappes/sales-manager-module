from mongoengine import Document, StringField, ReferenceField
from .user import User
from .company import Company
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

class Contact(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)
    title = StringField()
    zoom_id = StringField(required=True, unique=True)
    user = ReferenceField(User, required=True)
    company = ReferenceField(Company, required=True)

    meta = {'collection': 'contacts'}

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    title: str | None = None
    zoom_id: str
    user: str  # This will be the user_id
    company: str  # This will be the company_id

class ContactResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    title: str | None
    zoom_id: str
    user: str  # This will be the user_id
    company: str  # This will be the company_id

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    @classmethod
    def from_mongo(cls, contact: Contact):
        return cls(
            id=str(contact.id),
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            title=contact.title,
            zoom_id=contact.zoom_id,
            user=str(contact.user.id),
            company=str(contact.company.id)
        )

class ContactUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    title: str | None = None
    zoom_id: str | None = None
    company: str | None = None  # This will be the company_id
