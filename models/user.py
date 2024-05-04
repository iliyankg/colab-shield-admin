from flask_login import UserMixin
from pydantic import BaseModel, UUID4


class User(UserMixin, BaseModel):
    """User model for authentication and context.
    
    TODO: Add extra info like email, name, projects and their relevant details.
    """
    id: UUID4
