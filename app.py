from flask import Flask, request, jsonify, redirect, render_template, session
from sqlalchemy import null
from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


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
    # TODO: Create RegisterForm in forms.py
    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        user = User.register(username=name, password=password)
        db.session.add(user)
        db.session.commit()

        # flash messages
        return redirect("/secret")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """
        On GET request: displays the login form
        On POST request: Upon validation and authentication, redirects to
            route /secret.
            If not validated, render login form with error message.
    """
    # TODO: Create LoginForm in forms.py
    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        user = User.authenticate(name, password)

        if user:
            session["user_id"] = user.id
            return redirect("/secret")
        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.get("/secret")
def show_secret_page():
    return render_template("secret.html")
