from flask import (
    Flask,
    request,
    jsonify,
    redirect,
    render_template,
    session,
    flash
)
from flask_debugtoolbar import DebugToolbarExtension
# from sqlalchemy import null
from models import db, connect_db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get("/")
def show_register_page():
    """ Currently just redirects to register page """

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """
        On GET request: displays register form
        On POST route: Validates register form and upon validation, redirects to
            secret. Else if not validated, shows form with error messages
    """
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.username

        # flash messages
        return redirect(f"/users/{username}")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """
        On GET request: displays the login form
        On POST request: Upon validation and authentication, redirects to
            route /users/username.
            If not validated, render login form with error message.
    """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.username
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.get("/users/<username>")
def show_secret_page(username):
    """ Display user details
        If user_id in session is not in the url, redirect to home page
     """
    form = CSRFProtectForm()

    if session.get("user_id") != username:
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:
        user = User.query.filter_by(username=username).one_or_none()
        return render_template("user_page.html", user=user, form=form)


@app.post("/logout")
def logout_user():
    """ Clear information from session and redirect user """

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("user_id", None)

    # TODO: Message of warning and taking them out
    return redirect("/")

# Questions:
#
