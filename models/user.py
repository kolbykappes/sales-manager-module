from mongoengine import Document, StringField, DateTimeField, BooleanField
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

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
