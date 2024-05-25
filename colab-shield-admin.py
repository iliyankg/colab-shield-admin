from flask import Flask, render_template
from flask_login import LoginManager, login_required
from models import User, FileInfo
from backend import BackendConn
import uuid

app = Flask(__name__)
app.secret_key = "secret"  # FIXME: Move to env or config

flask_login = LoginManager(app)
flask_login.login_view = "login"  # type: ignore


@flask_login.user_loader
def load_user(user_id: str) -> User:
    # FIXME: implement actual user loading from db
    return User(id=uuid.uuid4())


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    return render_template("login.html")

# @app.route("/api/login", methods=["POST"])
# def api_login():
#     """API endpoint for login"""


@app.route("/")
# @login_required
def index():
    """Home page"""
    return render_template("home.html")


@app.route("/project/<project_id>")
# @login_required
def project(project_id):
    """Project page"""
    backend_conn = BackendConn("localhost:1338")
    try:
        response = backend_conn.get_files_for_project(project_id)
        files = [FileInfo(**file.model_dump()) for file in response.files]
    except Exception as e:
        return render_template("project.html", project_id=project_id,
                               num_entries=0, error=str(e))

    return render_template("project.html", project_id=project_id,
                           num_entries=len(files), entries=files)
