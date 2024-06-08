import structlog
from typing import Optional
from redis import Redis
from redis.commands.json.path import Path

from flask import Flask, request, url_for, redirect, jsonify, render_template
from flask_login import LoginManager, current_user, login_required, login_user

from pydantic import ValidationError

from models import User, FileInfo
from backend import BackendConn
from forms import LoginForm, CreateAccountForm

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(),
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=False),
        structlog.dev.ConsoleRenderer()
    ]
)
logger = structlog.get_logger()


app = Flask(__name__)
app.secret_key = "secret"  # FIXME: Move to env or config

flask_login = LoginManager(app)
flask_login.login_view = "login"  # type: ignore

# TODO: Move following to config
rc = Redis(host='127.0.0.1', port=6379, db=0)
backend_conn = BackendConn(url='http://localhost:1338')  # type: ignore


@flask_login.user_loader
def load_user(user_id: str) -> Optional[User]:
    """Load user from Redis."""
    user = rc.json().get(user_id)
    if user is None:
        return None  # TODO: logging

    try:
        return User.model_validate(user)
    except ValidationError as e:
        return None  # TODO: logging


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    """Create Account page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    print("about to validate form")

    form = CreateAccountForm(request.form)
    if form.validate_on_submit():
        # Check if user already exists
        user = rc.get(form.email.data)
        if user:
            return {"error": "User already exists"}, 409

        # Create user
        try:
            user = User.create_user(form.email.data)
        except Exception as e:
            return {"error": str(e)}, 500

        # Save user
        with rc.pipeline() as pipe:
            # TODO: These keys should be namespaced
            pipe.set(user.email, str(user.id))
            pipe.json().set(str(user.id), Path.root_path(), user.model_dump())
            pipe.execute()

        return redirect(url_for('login'))
    else:
        print(form.errors)

    return render_template("create_account.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user_id = rc.get(form.email.data)
        if not user_id:
            # TODO: Add errror and loggin
            return redirect(url_for("create_account"))

        user = rc.json().get(str(user_id))
        if not user:
            # TODO: Add errror and loggin
            return render_template("login.html", form=form)

        try:
            user = User.model_validate(user)
        except ValidationError as e:
            # TODO: Add errror and loggin
            return render_template("login.html", form=form)

        login_user(user, remember=True)
        return redirect(url_for('index'))

    return render_template("login.html", form=form)


@app.route("/")
@login_required
def index():
    """Home page"""
    return render_template("home.html")


@app.route("/project/<project_id>")
@login_required
def project(project_id):
    """Project page"""
    try:
        response = backend_conn.get_files_for_project(
            current_user.get_id(), project_id)
        files = [FileInfo(**file.model_dump()) for file in response.files]
    except Exception as e:
        return render_template("project.html", project_id=project_id,
                               num_entries=0, error=str(e))

    return render_template("project.html", project_id=project_id,
                           num_entries=len(files), entries=files)
