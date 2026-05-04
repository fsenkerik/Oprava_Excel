import os
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .models import db, Teacher
from config import config

csrf = CSRFProtect()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Teacher, int(user_id))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    cfg = config[config_name]()
    app.config.from_object(cfg)
    app.config['SQLALCHEMY_DATABASE_URI'] = cfg.SQLALCHEMY_DATABASE_URI
    app.config['UPLOAD_TEMP_DIR'] = cfg.UPLOAD_TEMP_DIR
    app.config['ANSWER_KEYS_DIR'] = cfg.ANSWER_KEYS_DIR

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Pro přístup se prosím přihlaste.'
    login_manager.login_message_category = 'warning'

    from .student import student_bp
    from .auth import auth_bp
    from .teacher import teacher_bp

    app.register_blueprint(student_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(teacher_bp)

    with app.app_context():
        # Ensure data directories exist before DB connection
        data_dir = os.path.dirname(app.config['UPLOAD_TEMP_DIR'])
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(app.config['UPLOAD_TEMP_DIR'], exist_ok=True)
        db.create_all()
        _seed_exercises()
        _seed_teacher()

    @app.route('/health')
    def health():
        return 'ok', 200

    return app


def _seed_teacher():
    from werkzeug.security import generate_password_hash
    username = os.environ.get('TEACHER_USERNAME', '').strip()
    password = os.environ.get('TEACHER_PASSWORD', '').strip()
    if not username or not password:
        return
    teacher = Teacher.query.filter_by(username=username).first()
    if not teacher:
        teacher = Teacher(username=username, password_hash=generate_password_hash(password))
        db.session.add(teacher)
        db.session.commit()


def _seed_exercises():
    from .exercises import EXERCISE_CONFIGS
    from .models import Exercise

    for code, cfg in EXERCISE_CONFIGS.items():
        if not Exercise.query.filter_by(code=code).first():
            ex = Exercise(
                code=code,
                name=cfg['name'],
                max_points=sum(t['max_points'] for t in cfg['tasks']),
            )
            db.session.add(ex)
    db.session.commit()
