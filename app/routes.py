# -*- coding: utf-8 -*-

from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, CreateTestForm, CreateQuetionForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Test, Question, Answer
from flask_login import login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    tests = Test.query.all()
    return render_template('index.html', title='Home', tests=tests)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, Вы теперь новый пользователь!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/create-test', methods=['GET', 'POST'])
@login_required
def create_test():
    form = CreateTestForm()
    if form.validate_on_submit():
        test = Test(name=form.name.data)
        db.session.add(test)
        db.session.commit()
        flash(f'Создан новый опрос "{form.name.data}"!')
        return redirect(url_for('index'))
    return render_template('create-test.html', title='Создание нового опроса', form=form)


@app.route('/edit-test')
@login_required
def edit_test():
    test_id = request.args.get('test_id')
    questions = Question.query.filter_by(test_id=test_id)
    return render_template('edit-test.html', title='Редактирование опроса', questions=questions, test_id=test_id)


@app.route('/create-question', methods=['GET', 'POST'])
@login_required
def create_question():
    form = CreateQuetionForm()
    test_id = request.args.get('test_id')
    if form.validate_on_submit():
        question = Question(content=form.content.data, test_id=test_id)
        db.session.add(question)
        db.session.commit()

        answers = {'1': None, '2': None, '3': None, '4': None}
        for answer_number in answers:
            is_ready = True if answer_number == form.ready.data else False
            content = getattr(form, f'answer{answer_number}').data
            if content:
                answers[answer_number] = Answer(content=content, question_id=question.id, is_ready=is_ready)
                db.session.add(answers[answer_number])
        db.session.commit()
        flash(f'Создан новый вопрос "{form.content.data}"!')
        return redirect(url_for('edit_test', test_id=test_id))
    return render_template('create-question.html', title='Создание нового вопроса', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
