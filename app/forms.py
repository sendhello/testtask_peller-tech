from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from config import Config


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Авторизация')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя уже существует. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Данный email уже зарегистирован. Пожалуйста, укажите другой адрес электронной почты.')


class CreateTestForm(FlaskForm):
    name = StringField('Название нового опроса', validators=[DataRequired()])
    submit = SubmitField('Создать')


class CreateQuetionForm(FlaskForm):
    content = StringField('Вопрос', validators=[DataRequired()], widget=TextArea())
    answer1 = StringField('Вариант 1', validators=[DataRequired()])
    answer2 = StringField('Вариант 2', validators=[DataRequired()])
    answer3 = StringField('Вариант 3')
    answer4 = StringField('Вариант 4')
    ready = RadioField(
        'Правильный ответ', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    submit = SubmitField('Добавить вопрос')
