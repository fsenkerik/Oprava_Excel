import os
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
import openpyxl

GRADE_THRESHOLDS = [
    (90, 1),
    (75, 2),
    (60, 3),
    (40, 4),
    (0, 5),
]

GRADE_LABELS = {
    1: "Výborný",
    2: "Chvalitebný",
    3: "Dobrý",
    4: "Dostatečný",
    5: "Nedostatečný",
}


def compute_grade(score: int, max_score: int) -> int:
    if max_score == 0:
        return 5
    pct = (score / max_score) * 100
    for threshold, grade in GRADE_THRESHOLDS:
        if pct >= threshold:
            return grade
    return 5


def grade_label(grade: int) -> str:
    return GRADE_LABELS.get(grade, "")


def _round2(value) -> Decimal:
    try:
        return Decimal(str(float(value))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except (InvalidOperation, TypeError, ValueError):
        return None


def _normalize_text(value) -> str:
    if value is None:
        return ''
    return str(value).strip().lower()


def _answers_match(student_val, key_val, comparison: str) -> bool:
    if student_val is None or student_val == '':
        return False
    if key_val is None or key_val == '':
        return False

    if comparison == 'text':
        return _normalize_text(student_val) == _normalize_text(key_val)

    if comparison == 'numeric':
        s = _round2(student_val)
        k = _round2(key_val)
        if s is None or k is None:
            return False
        return s == k

    # mixed: try numeric first, fall back to text
    s = _round2(student_val)
    k = _round2(key_val)
    if s is not None and k is not None:
        return s == k
    return _normalize_text(student_val) == _normalize_text(key_val)


def _read_column(ws, col_letter: str, row_start: int, row_end: int) -> list:
    col_idx = openpyxl.utils.column_index_from_string(col_letter)
    return [ws.cell(row=r, column=col_idx).value for r in range(row_start, row_end + 1)]


def grade_submission(uploaded_path: str, exercise_config: dict, key_path: str) -> dict:
    # Open as file objects so handles are released on close (needed on Windows)
    with open(uploaded_path, 'rb') as f:
        student_wb = openpyxl.load_workbook(f, data_only=True)
    with open(key_path, 'rb') as f:
        key_wb = openpyxl.load_workbook(f, data_only=True)

    task_scores = {}
    task_details = {}
    total_score = 0
    max_score = 0

    for task in exercise_config["tasks"]:
        tid = task["id"]
        sheet_name = task["sheet"]
        max_pts = task["max_points"]
        comparison = task["comparison"]

        if sheet_name not in student_wb.sheetnames:
            task_scores[tid] = 0
            task_details[tid] = []
            max_score += max_pts
            continue

        student_ws = student_wb[sheet_name]
        key_ws = key_wb[task["key_sheet"]]

        student_answers = _read_column(
            student_ws,
            task["answer_col"],
            task["answer_row_start"],
            task["answer_row_end"],
        )
        key_answers = _read_column(
            key_ws,
            task["key_col"],
            task["key_row_start"],
            task["key_row_end"],
        )

        n = len(key_answers)
        correct_count = 0
        details = []

        for i, (sv, kv) in enumerate(zip(student_answers, key_answers)):
            correct = _answers_match(sv, kv, comparison)
            if correct:
                correct_count += 1
            details.append({
                "question": i + 1,
                "student": str(sv) if sv is not None else "",
                "correct": correct,
            })

        # 1 point per correct answer (matches Excel scoring for this exercise set)
        task_score = correct_count
        task_scores[tid] = task_score
        task_details[tid] = details
        total_score += task_score
        max_score += max_pts

    grade = compute_grade(total_score, max_score)

    return {
        "total_score": total_score,
        "max_score": max_score,
        "grade": grade,
        "grade_label": grade_label(grade),
        "task_scores": task_scores,
        "task_details": task_details,
    }
