from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

user_test = db.Table('user_test',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('test_id', db.Integer, db.ForeignKey('test.id'))
)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.String(128), index=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String(128), index=True)
    tags = db.relationship('Test', secondary=user_test, backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    questions = db.relationship('Question', backref='test', lazy='dynamic')

    def __repr__(self):
        return '<Test {}>'.format(self.name)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __repr__(self):
        return '<Question {}>'.format(self.content)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    is_ready = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Answer {}>'.format(self.content)
