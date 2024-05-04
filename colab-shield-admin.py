from flask import Flask, render_template
from flask_login import LoginManager, login_required
from models import User
import uuid

app = Flask(__name__)
app.secret_key = "secret"  # FIXME: Move to env or config

flask_login = LoginManager(app)
flask_login.login_view = "login"  # type: ignore


@flask_login.user_loader
def load_user(user_id: str) -> User:
    # FIXME: implement actual user loading from db
    return User(id=uuid.uuid4())


@app.route("/")
@login_required
def index():
    """Home page"""
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    return render_template("login.html")
