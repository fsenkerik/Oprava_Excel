import uuid
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


def gen_uuid():
    return str(uuid.uuid4())


class Teacher(UserMixin, db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    max_points = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    submissions = db.relationship('Submission', backref='exercise', lazy=True)


class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    student_name = db.Column(db.String(200), nullable=False)
    student_class = db.Column(db.String(50), nullable=False)

    submitted_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    original_filename = db.Column(db.String(255))

    total_score = db.Column(db.Integer, nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    task_scores = db.Column(db.JSON, nullable=False)
    task_details = db.Column(db.JSON, nullable=True)

    is_archived = db.Column(db.Boolean, default=False)
    archive_label = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
