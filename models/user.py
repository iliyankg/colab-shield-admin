from flask_login import UserMixin
from pydantic import BaseModel, FieldSerializationInfo, Field, UUID4, EmailStr, field_serializer
from uuid import uuid4


class User(UserMixin, BaseModel):
    """User model for authentication and context.

    TODO: Add extra info like email, name, projects and their relevant details.
    """
    id: UUID4 = Field(default_factory=uuid4, alias="id")
    email: EmailStr = Field(alias="email")

    @staticmethod
    def create_user(email: str) -> 'User':  # forward declaration
        """Create a new user with the given email."""
        return User(id=uuid4(), email=email)

    @field_serializer("id", when_used="always")
    def serializer_uuid_to_str(self, v: UUID4, _info: FieldSerializationInfo) -> str:
        """Serialize UUID to string so it can be written to the DB."""
        return str(v)
