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
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm, EditNoteForm
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

################ ROUTES FOR USERS ##############

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
def show_user_page(username):
    """
        Display user details
        If user_id in session is not in the url, redirect to home page
     """

    if session.get("user_id") != username: #"guard fn" do it first
        flash("You must be logged in to view!")
        return redirect("/")

    form = CSRFProtectForm()

    user = User.query.filter_by(username=username).one_or_none()

    # a mild optimization to create db.Relationship and say notes = user.notes
    notes = Note.query.filter_by(owner=username).order_by("id").all()

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

@app.post("/users/<username>/delete")
def delete_user(username):
    """Deletes current user, by deleting their notes first!"""

    if session.get("user_id") != username:
        raise Unauthorized()

    form = CSRFProtectForm()

    if form.validate_on_submit():
        Note.query.filter_by(owner=username).delete()
        db.session.commit() #unnecessary!

        user = User.query.filter_by(username=username).one_or_none() #prefer one() here
        #one_or_none() is relevant and useful only if u DO SOMETHING with None when it is None
        db.session.delete(user) #altho error for .delete(None) anyway!
        db.session.commit()

        return redirect("/")

    else:
        raise Unauthorized()


############## Routes for Notes ######################


@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def new_note(username):
    """
    On GET: displays a form to submit a new note
    On POST: on validated submission, adds note and redirects to user's page
    """

    if session.get("user_id") != username:
        raise Unauthorized()

    form = AddNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        owner = username

        note = Note(title=title, content=content, owner=owner)

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{username}")
    else:
        return render_template("add_note_form.html", form=form, username=username)


@app.route('/notes/<int:note_id>/update', methods=["GET", "POST"]) #TODO:check int: elsewhere
def edit_note(note_id):
    """
    On GET: displays a form to edit an existing note
    On POST: on validated submission, edits note and redirects to user's page
    """

    note = Note.query.get_or_404(note_id)#SQLAlchemy doing friendly forcing here
    username = note.owner

    if session.get("user_id") != username:
        raise Unauthorized()

    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note.title = title
        note.content = content

        db.session.commit()


        return redirect(f'/users/{note.owner}')

    else:
        return render_template("edit_note_form.html", form=form, username=username)


@app.post('/notes/<note_id>/delete')
def delete_note(note_id):
    """
    Deletes a note from the database. Redirects to the user's page
    """

    note = Note.query.get_or_404(note_id)
    username = note.owner #This is where name "owner" complicates
    #what if this read user = note.owner ??

    if session.get("user_id") != username:
        raise Unauthorized()

    form = CSRFProtectForm()

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()
        return redirect(f"/users/{note.owner}")
    else:
        raise Unauthorized()
