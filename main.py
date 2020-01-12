from app import app, db
from app.models import User, Test, Question, Answer


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Test': Test, 'Question': Question, 'Answer': Answer}