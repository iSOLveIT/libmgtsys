from datetime import datetime as dt
from secrets import compare_digest

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils.types import PasswordType, ChoiceType, Password

# from project.modules import db
from .. import db, login_manager
from ..db_helper import PkModel
# from ..tracking.meta import Book
# from sqlalchemy_utils import force_auto_coercion
#
#
# force_auto_coercion()


class User(UserMixin, PkModel):
    """Model for the users table"""

    GENDER = [('', ''), ('M', 'Male'), ('F', 'Female')]

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sid = db.Column(db.String(30), unique=True, nullable=False, info={'label': 'User ID'})
    name = db.Column(db.String(300), nullable=False, info={'label': 'Name'})
    _password = db.Column(PasswordType(max_length=300, schemes=['pbkdf2_sha512']),
                          nullable=False, default=f"SWESCO_{id}", info={'label': 'Password'})
    gender = db.Column(ChoiceType(choices=GENDER), nullable=False, info={'label': 'Gender'})
    date_registered = db.Column(db.DateTime, nullable=False, default=dt.now())
    last_seen = db.Column(db.DateTime, nullable=False, default=dt.now())
    login_at = db.Column(db.DateTime, nullable=False, default=dt.now())
    has_activated = db.Column(db.Boolean(), nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    # books_recorded = db.relationship('Books', backref='recorded_by', lazy=True)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))

    def __repr__(self):
        return f"<User-id: {self.id}, User-sid: {self.sid}>"

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        # the default hashing method is pbkdf2_sha512
        self._password = plaintext

    def check_password(self, password):
        check = compare_digest(self._password, Password(value=password))
        return check

    def is_admin(self):
        r = self.role
        return any([r.purpose == "ADMIN" and r.permission_level is True])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# login_manager.login_view = "auth.login"


class Class(PkModel):
    """Model for information about various classes"""

    CLASS_RANGE = [('', ''), ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('f', 'F'), ('g', 'G'), ('h', 'H'),
                   ('i', 'I'), ('j', 'J'), ('k', 'K'), ('l', 'L'), ('m', 'M'), ('n', 'N'), ('o', 'O'), ('p', 'P'),
                   ('q', 'Q'), ('r', 'R'), ('s', 'S'), ('t', 'T'), ('u', 'U'), ('v', 'V'), ('w', 'W'), ('x', 'X'),
                   ('y', 'Y'), ('z', 'Z')]
    TRACK = [('', ''), ('GD', 'Gold'), ('GN', 'Green')]
    COURSES = [('', ''), ('GA', 'General Arts'), ('BU', 'Business'), ('SC', 'Science'),
               ('AG', 'Agriculture'), ('VA', 'Visual Arts'), ('HE', 'Home Economics')]

    __tablename__ = "class"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    programme = db.Column(ChoiceType(COURSES), nullable=False, info={'label': 'Programme'})
    current_class = db.Column(ChoiceType(CLASS_RANGE), nullable=False, info={'label': 'Class'})
    track = db.Column(ChoiceType(TRACK), nullable=False, info={'label': 'Track'})
    year_group = db.Column(db.String(4), nullable=False, info={'label': 'Admission Year'})
    class_tag = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref='class', lazy=True)

    def __repr__(self):
        return f"<Class-id: {self.id}>"


class Staff(PkModel):
    """Model for information about staff"""

    __tablename__ = "staff"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department = db.Column(db.String(100), unique=True, nullable=False, info={'label': 'Department'})
    users = db.relationship('User', backref='staff', lazy=True)

    def __repr__(self):
        return f"<Staff-id: {self.id}>"


class Role(PkModel):
    """Model for role based access control assigned to users"""

    ACCESS = [('student', 'STUDENT'), ('teacher', 'TEACHER'),
              ('admin', 'ADMIN')]

    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purpose = db.Column(ChoiceType(ACCESS), unique=True, nullable=False, info={'label': 'Account Type'})
    permission_level = db.Column(db.Boolean, nullable=False, default=False)
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f"<Role-id: {self.id}>"
