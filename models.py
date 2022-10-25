
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
        primary_key=True,
        nullable=False,
        unique=True
    )

    password = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(50), nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    # register class method
    @classmethod
    def register(cls, username, password):
        """
        Registers new user using Bcrypt.
        Function always returns User instances of newly created user.
        """

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username, password=hashed)

    @classmethod
    def authenticate(cls, username, password):
        """
        Logs in user using Bcrypt.
        Function returns the user object if login successful,
            if not, function returns None
        """

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False
