import csv
import io
from datetime import timezone
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, Response, current_app,
)
from flask_login import login_required
from .models import db, Submission, Exercise
from .exercises import EXERCISE_CONFIGS
from .grader import grade_label

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')


@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    class_filter = request.args.get('class', '').strip()
    exercise_filter = request.args.get('exercise', '').strip()
    show_archived = request.args.get('archived', '0') == '1'
    page = request.args.get('page', 1, type=int)

    query = Submission.query.filter_by(is_archived=show_archived)

    if class_filter:
        query = query.filter(Submission.student_class.ilike(f'%{class_filter}%'))
    if exercise_filter:
        ex = Exercise.query.filter_by(code=exercise_filter).first()
        if ex:
            query = query.filter_by(exercise_id=ex.id)

    query = query.order_by(Submission.submitted_at.desc())
    pagination = query.paginate(page=page, per_page=30, error_out=False)

    exercises = Exercise.query.all()
    classes = db.session.query(Submission.student_class).distinct().order_by(Submission.student_class).all()
    classes = [c[0] for c in classes]

    return render_template(
        'teacher/dashboard.html',
        submissions=pagination.items,
        pagination=pagination,
        exercises=exercises,
        classes=classes,
        class_filter=class_filter,
        exercise_filter=exercise_filter,
        show_archived=show_archived,
        grade_label=grade_label,
    )


@teacher_bp.route('/submissions/<submission_id>')
@login_required
def detail(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    exercise = submission.exercise
    ex_config = EXERCISE_CONFIGS.get(exercise.code, {})
    tasks_meta = {t['id']: t['name'] for t in ex_config.get('tasks', [])}
    return render_template(
        'teacher/detail.html',
        submission=submission,
        exercise=exercise,
        tasks_meta=tasks_meta,
        grade_label=grade_label,
    )


@teacher_bp.route('/submissions/<submission_id>/archive', methods=['POST'])
@login_required
def archive(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    label = request.form.get('archive_label', '').strip()
    submission.is_archived = True
    submission.archive_label = label or None
    db.session.commit()
    flash(f'Odevzdání {submission.student_name} bylo archivováno.', 'success')
    return redirect(request.referrer or url_for('teacher.dashboard'))


@teacher_bp.route('/submissions/<submission_id>/unarchive', methods=['POST'])
@login_required
def unarchive(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    submission.is_archived = False
    submission.archive_label = None
    db.session.commit()
    flash(f'Odevzdání {submission.student_name} bylo obnoveno.', 'success')
    return redirect(request.referrer or url_for('teacher.dashboard'))


@teacher_bp.route('/submissions/<submission_id>/delete', methods=['POST'])
@login_required
def delete(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    name = submission.student_name
    db.session.delete(submission)
    db.session.commit()
    flash(f'Odevzdání {name} bylo smazáno.', 'success')
    return redirect(url_for('teacher.dashboard'))


@teacher_bp.route('/submissions/<submission_id>/note', methods=['POST'])
@login_required
def save_note(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    submission.notes = request.form.get('notes', '').strip() or None
    db.session.commit()
    flash('Poznámka byla uložena.', 'success')
    return redirect(url_for('teacher.detail', submission_id=submission_id))


@teacher_bp.route('/export')
@login_required
def export_csv():
    class_filter = request.args.get('class', '').strip()
    exercise_filter = request.args.get('exercise', '').strip()
    show_archived = request.args.get('archived', '0') == '1'

    query = Submission.query.filter_by(is_archived=show_archived)
    if class_filter:
        query = query.filter(Submission.student_class.ilike(f'%{class_filter}%'))
    if exercise_filter:
        ex = Exercise.query.filter_by(code=exercise_filter).first()
        if ex:
            query = query.filter_by(exercise_id=ex.id)

    submissions = query.order_by(Submission.submitted_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Jméno', 'Třída', 'Cvičení', 'Datum odevzdání', 'Body', 'Max bodů', 'Procent', 'Známka'])

    for s in submissions:
        pct = round(s.total_score / s.max_score * 100, 1) if s.max_score else 0
        submitted = s.submitted_at.strftime('%d.%m.%Y %H:%M') if s.submitted_at else ''
        writer.writerow([
            s.student_name,
            s.student_class,
            s.exercise.name,
            submitted,
            s.total_score,
            s.max_score,
            f'{pct} %',
            f'{s.grade} – {grade_label(s.grade)}',
        ])

    output.seek(0)
    return Response(
        '﻿' + output.getvalue(),  # BOM for Excel UTF-8
        mimetype='text/csv; charset=utf-8',
        headers={'Content-Disposition': 'attachment; filename=odevzdani.csv'},
    )


@teacher_bp.route('/exercises')
@login_required
def exercises():
    all_exercises = Exercise.query.all()
    return render_template('teacher/exercises.html', exercises=all_exercises)


@teacher_bp.route('/exercises/<int:exercise_id>/toggle', methods=['POST'])
@login_required
def toggle_exercise(exercise_id):
    ex = Exercise.query.get_or_404(exercise_id)
    ex.is_active = not ex.is_active
    db.session.commit()
    state = 'aktivováno' if ex.is_active else 'deaktivováno'
    flash(f'Cvičení "{ex.name}" bylo {state}.', 'success')
    return redirect(url_for('teacher.exercises'))
