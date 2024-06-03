from typing import Optional

from redis import Redis
from redis.commands.json.path import Path
from flask import Flask, current_user, request, url_for, redirect, jsonify, render_template
from flask_login import LoginManager, login_required, login_user
from pydantic import ValidationError
from models import User, FileInfo
from protocol import CreateAccountRequest
from backend import BackendConn


app = Flask(__name__)
app.secret_key = "secret"  # FIXME: Move to env or config

flask_login = LoginManager(app)
flask_login.login_view = "login"  # type: ignore

# TODO: Move following to config
rc = Redis(host='redis', port=6379, db=0)
backend_conn = BackendConn(url='http://localhost:1338')  # type: ignore


@flask_login.user_loader
def load_user(user_id: str) -> Optional[User]:
    user = rc.json().get(user_id)
    if user is None:
        return None  # TODO: logging

    try:
        return User.model_validate(user)
    except ValidationError as e:
        return None  # TODO: logging


@app.route("/api/register", methods=["POST"])
def api_register():
    """API endpoint for registration"""
    # Validate request
    try:
        create_account_request = CreateAccountRequest.model_validate(
            request.json)
    except ValidationError as e:
        return {"error": str(e)}, 400

    # Check if user already exists
    user = rc.get(create_account_request.email)
    if user:
        return {"error": "User already exists"}, 409

    # Create user
    try:
        user = User.create_user(create_account_request.email)
    except Exception as e:
        return {"error": str(e)}, 500

    # Save user
    with rc.pipeline() as pipe:
        pipe.set(user.email, str(user.id))
        pipe.json().set(str(user.id), Path.root_path(), user.model_dump())
        pipe.execute()

    # Return response
    return jsonify({"status": "success", "user_id": str(user.id)})


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    email = request.form.get('email')  # TODO: Add validation
    if not email:
        # TODO: Add error and logging
        return render_template("login.html")

    user_id = rc.get(email)
    if not user_id:
        # TODO: Add errror and loggin
        return render_template("login.html")

    user = rc.json().get(str(user_id))
    if not user:
        # TODO: Add errror and loggin
        return render_template("login.html")

    try:
        user = User.model_validate(user)
    except ValidationError as e:
        # TODO: Add errror and loggin
        return render_template("login.html")

    login_user(user, remember=True)
    return redirect(url_for('index'))


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
