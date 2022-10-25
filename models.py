
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ Site User """

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True
    )

    password = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(
        cls,
        username,
        password,
        email,
        first_name,
        last_name
    ):
        """
        Registers new user using Bcrypt.
        Function always returns User instances of newly created user.
        """

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    @classmethod
    def authenticate(cls, username, password):
        """
        Logs in user using Bcrypt.
        Function returns the user object if login successful,
            if not, function returns False
        """

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

class Note(db.Model):
    """Note on web app"""

    __tablename__ = "notes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.String,
        nullable=False
    )

    owner = db.Column(
        db.String,
        db.ForeignKey("users.username"),
        nullable=False
    )
