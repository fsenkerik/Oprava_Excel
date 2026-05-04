import os
import uuid
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, current_app,
)
from werkzeug.utils import secure_filename
from .models import db, Exercise, Submission
from .exercises import EXERCISE_CONFIGS
from .grader import grade_submission, grade_label

student_bp = Blueprint('student', __name__)

ALLOWED_EXTENSIONS = {'xlsx'}


def _allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _render_upload(error_msg=None, **form_values):
    """Zobrazí formulář, zachová vyplněné hodnoty při chybě."""
    exercises = Exercise.query.filter_by(is_active=True).all()
    if error_msg:
        flash(error_msg, 'danger')
    return render_template('student/upload.html', exercises=exercises, **form_values)


@student_bp.route('/', methods=['GET'])
def index():
    exercises = Exercise.query.filter_by(is_active=True).all()
    return render_template('student/upload.html', exercises=exercises)


@student_bp.route('/upload', methods=['POST'])
def upload():
    student_name = request.form.get('student_name', '').strip()
    student_class = request.form.get('student_class', '').strip()
    exercise_id = request.form.get('exercise_id', '').strip()

    form_values = dict(
        prefill_name=student_name,
        prefill_class=student_class,
        prefill_exercise=exercise_id,
    )

    if not student_name or not student_class or not exercise_id:
        return _render_upload('Vyplňte prosím všechna pole.', **form_values)

    exercise = Exercise.query.get(exercise_id)
    if not exercise or not exercise.is_active:
        return _render_upload('Zvolené cvičení není dostupné.', **form_values)

    file = request.files.get('excel_file')
    if not file or file.filename == '':
        return _render_upload('Vyberte prosím soubor.', **form_values)

    if not _allowed(file.filename):
        return _render_upload('Nahrávejte pouze soubory ve formátu .xlsx (Excel).', **form_values)

    tmp_filename = f"{uuid.uuid4()}.xlsx"
    tmp_path = os.path.join(current_app.config['UPLOAD_TEMP_DIR'], tmp_filename)

    try:
        file.save(tmp_path)

        ex_config = EXERCISE_CONFIGS.get(exercise.code)
        if not ex_config:
            return _render_upload('Konfigurace cvičení nebyla nalezena.', **form_values)

        key_path = os.path.join(
            current_app.config['ANSWER_KEYS_DIR'],
            ex_config['answer_key_file'],
        )
        if not os.path.exists(key_path):
            current_app.logger.error(f"Klíč nenalezen: {key_path}")
            return _render_upload('Soubor s odpověďmi nebyl nalezen na serveru.', **form_values)

        result = grade_submission(tmp_path, ex_config, key_path)

    except Exception as e:
        current_app.logger.error(f"Chyba při opravování: {e}")
        return _render_upload(
            'Soubor se nepodařilo zpracovat. Zkontrolujte, zda nahráváte správný soubor.',
            **form_values,
        )
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    submission = Submission(
        exercise_id=exercise.id,
        student_name=student_name,
        student_class=student_class,
        original_filename=secure_filename(file.filename),
        total_score=result['total_score'],
        max_score=result['max_score'],
        grade=result['grade'],
        task_scores=result['task_scores'],
        task_details=result['task_details'],
    )
    db.session.add(submission)
    db.session.commit()

    return redirect(url_for('student.result', submission_id=submission.id))


@student_bp.route('/result/<submission_id>')
def result(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    exercise = submission.exercise
    ex_config = EXERCISE_CONFIGS.get(exercise.code, {})
    tasks_meta = {t['id']: t['name'] for t in ex_config.get('tasks', [])}
    return render_template(
        'student/result.html',
        submission=submission,
        exercise=exercise,
        tasks_meta=tasks_meta,
        grade_label=grade_label(submission.grade),
    )
