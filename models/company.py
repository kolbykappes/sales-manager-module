from mongoengine import Document, StringField, ReferenceField
from .user import User
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

class Company(Document):
    """
    Company document model for MongoDB.
    """
    name = StringField(required=True)
    website = StringField()
    primary_industry = StringField()
    primary_sub_industry = StringField()
    zoom_id = StringField(required=True, unique=True)
    user = ReferenceField(User, required=True)

    meta = {'collection': 'companies'}

class CompanyCreate(BaseModel):
    """
    Pydantic model for company creation.
    """
    name: str
    website: str | None = None
    primary_industry: str | None = None
    primary_sub_industry: str | None = None
    zoom_id: str
    user: str  # This will be the user_id

class CompanyResponse(BaseModel):
    """
    Pydantic model for company response.
    """
    id: str
    name: str
    website: str | None
    primary_industry: str | None
    primary_sub_industry: str | None
    zoom_id: str
    user: str  # This will be the user_id

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    @classmethod
    def from_mongo(cls, company: Company) -> 'CompanyResponse':
        """
        Create a CompanyResponse instance from a Company document.
        
        Args:
            company (Company): The Company document to convert.
        
        Returns:
            CompanyResponse: The created CompanyResponse instance.
        """
        return cls(
            id=str(company.id),
            name=company.name,
            website=company.website,
            primary_industry=company.primary_industry,
            primary_sub_industry=company.primary_sub_industry,
            zoom_id=company.zoom_id,
            user=str(company.user.id)
        )

class CompanyUpdate(BaseModel):
    """
    Pydantic model for company update.
    """
    name: str | None = None
    website: str | None = None
    primary_industry: str | None = None
    primary_sub_industry: str | None = None
    zoom_id: str | None = None
