from models import db, User, Note
from app import app

db.drop_all()
db.create_all()


user_1 = User.register(
    username = "test_username_1",
    password = "password",
    email = "test@test.com",
    first_name = "test_first_name_1",
    last_name = "test_last_name_1"
)

user_2 = User.register(
    username = "test_username_2",
    password = "password2",
    email = "test2@test2.com",
    first_name = "test_first_name_2",
    last_name = "test_last_name_2"
)

db.session.add(user_1)
db.session.add(user_2)

db.session.commit()


note_1 = Note(
    title = "note_1",
    content = "testtesttest",
    owner = "test_username_1"
)
note_2 = Note(
    title = "note_2",
    content = "hellohellohello",
    owner = "test_username_1"
)
note_3 = Note(
    title = "note_1_2",
    content = "test2test2test2",
    owner = "test_username_2"
)

db.session.add(note_1)
db.session.add(note_2)
db.session.add(note_3)

db.session.commit()
