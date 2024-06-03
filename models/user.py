from flask_login import UserMixin
from pydantic import BaseModel, EmailStr, UUID4
import uuid


class User(UserMixin, BaseModel):
    """User model for authentication and context.

    TODO: Add extra info like email, name, projects and their relevant details.
    """
    id: UUID4
    email: EmailStr

    @staticmethod
    def create_user(email: str) -> 'User':  # forward declaration
        """Create a new user with the given email."""
        return User(id=uuid.uuid4(), email=email)

    @staticmethod
    def build_redis_key(user_id: str) -> str:
        return f"user:{user_id}"
