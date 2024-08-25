from mongoengine import Document, StringField, DateTimeField, BooleanField
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict
from datetime import datetime

class User(Document):
    email = StringField(required=True, unique=True)
    user_id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    username = StringField(required=True, unique=True)
    full_name = StringField(required=True)
    password_hash = StringField(required=True)
    is_active = BooleanField(default=True)
    last_login = DateTimeField()

    meta = {'collection': 'users'}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str

class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    username: str
    full_name: str
    is_active: bool
    last_login: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )

    @classmethod
    def from_mongo(cls, user: User):
        return cls(
            user_id=str(user.user_id),
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            last_login=user.last_login
        )

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None
