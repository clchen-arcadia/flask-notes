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
from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm
from werkzeug.exceptions import Unauthorized

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
    """
        Display user details
        If user_id in session is not in the url, redirect to home page
     """
     #TODO: create link to send to add note form. and a button to delete the entire acct! and buttons to delete each note!

    form = CSRFProtectForm()

    notes = Note.query.filter_by(owner=username).all()

    if session.get("user_id") != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.filter_by(username=username).one_or_none()
        return render_template(
            "user_page.html",
            user=user,
            form=form,
            notes=notes
        )


@app.post("/logout")
def logout_user():
    """ Clear information from session and redirect user """

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("user_id", None)
        return redirect("/")

    else:
        raise Unauthorized()


############## Routes for Notes ######################

@app.post('/users/<username>/delete')
def delete_user(username):
    """
    Deletes a user from the database
        after deleting all of their notes first!
        Function then redirects to '/'
    """


@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def new_note(username):
    """
    On GET: displays a form to submit a new note
    On POST: on validated submission, adds note and redirects to user's page
    """

@app.route('/notes/<note_id>/update', methods=["GET", "POST"])
def edit_note(note_id):
    """
    On GET: displays a form to edit an existing note
    On POST: on validated submission, edits note and redirects to user's page
    """
    #TODO: check session that user has authorization to edit this note!

@app.post('/notes/<note_id>/delete')
def delete_note(note_id):
    """
    Deletes a note from the database. Redirects to the user's page
    """
    #TODO: check session that user has authorization to delete this note!
