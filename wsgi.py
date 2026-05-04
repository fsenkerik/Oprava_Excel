import os
import click
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.models import db, Teacher
from werkzeug.security import generate_password_hash

app = create_app(os.environ.get('FLASK_ENV', 'production'))


@app.cli.command('init-teacher')
@click.option('--username', default=lambda: os.environ.get('TEACHER_USERNAME', 'ucitel'))
@click.option('--password', default=lambda: os.environ.get('TEACHER_PASSWORD', ''))
def init_teacher(username, password):
    """Vytvoří nebo aktualizuje učitelský účet."""
    if not password:
        password = click.prompt('Heslo', hide_input=True, confirmation_prompt=True)
    with app.app_context():
        teacher = Teacher.query.filter_by(username=username).first()
        if teacher:
            teacher.password_hash = generate_password_hash(password)
            click.echo(f'Heslo pro "{username}" bylo aktualizováno.')
        else:
            teacher = Teacher(username=username, password_hash=generate_password_hash(password))
            db.session.add(teacher)
            click.echo(f'Učitelský účet "{username}" byl vytvořen.')
        db.session.commit()


if __name__ == '__main__':
    app.run()
