from flask_wtf import FlaskForm
from redis import Redis
from wtforms import EmailField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email


class EmailInRedis(object):
    """Check if email exists in Redis"""
    _db: Redis  # TODO: This should be a more generic abstraction so we can replace Redis with any other DB

    def __init__(self, rc: Redis):
        """
        Initialize the validator with the Redis connection.
        Args:
            rc (Redis): Redis connection
            invert (bool, optional): Invert the check. Defaults to False.
        """
        self._db = rc

    def __call__(self, form, field):
        if not self._email_in_db(field.data):
            raise ValidationError("Account does not exist")

    def _email_in_db(self, email: str) -> bool:
        """Check if email exists in the DB"""
        return bool(self._db.get(email))


class EmailNotInRedis(EmailInRedis):
    """Check if email does not exist in Redis"""

    def __call__(self, form, field):
        if self._email_in_db(field.data):
            raise ValidationError("Account already exists")


class LoginForm(FlaskForm):
    """Form for logging in"""
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Login")

    def __init__(self, rc: Redis, *args, **kwargs):
        """Initialize the form with the Redis connection"""
        super().__init__(*args, **kwargs)
        # TODO: Not sure this is the best way to do this but... hey it works for now.
        # TODO: Look into a redis ORM similar to SQLAlchemy
        # which seems to be what others are using to handle this kind of validation.
        self.email.validators = [
            v for v in self.email.validators] + [EmailInRedis(rc)]


class CreateAccountForm(FlaskForm):
    """Form for creating an account"""
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Create Account")

    def __init__(self, rc: Redis, *args, **kwargs):
        """Initialize the form with the Redis connection"""
        super().__init__(*args, **kwargs)
        self.email.validators = [
            v for v in self.email.validators] + [EmailNotInRedis(rc)]
