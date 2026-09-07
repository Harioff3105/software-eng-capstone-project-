from datetime import date
from flask import Blueprint, jsonify, request
from models import Scholarship, db
from routes.auth import current_user

scholarships_bp = Blueprint('scholarships', __name__, url_prefix='/api/scholarships')


def serialize(s):
    return {'id': s.id, 'title': s.title, 'provider': s.provider, 'description': s.description, 'amount': s.amount,
            'deadline': s.deadline.isoformat() if s.deadline else None, 'min_cgpa': s.min_cgpa, 'max_income': s.max_income,
            'eligible_category': s.eligible_category, 'eligible_courses': s.eligible_courses, 'tags': s.tags, 'active': s.active}


def admin_required():
    user = current_user()
    return user if user and user.role == 'admin' else None


def apply_fields(s, data):
    for field in ('title', 'provider', 'description', 'eligible_category', 'eligible_courses', 'tags'):
        if field in data: setattr(s, field, str(data[field]).strip())
    for field in ('amount', 'min_cgpa', 'max_income'):
        if field in data and data[field] not in ('', None): setattr(s, field, float(data[field]))
        elif field in data: setattr(s, field, None)
    if 'deadline' in data: s.deadline = date.fromisoformat(data['deadline']) if data['deadline'] else None
    if 'active' in data: s.active = bool(data['active'])


@scholarships_bp.get('')
def list_scholarships():
    q = (request.args.get('q') or '').strip()
    query = Scholarship.query.filter_by(active=True)
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(Scholarship.title.ilike(like), Scholarship.provider.ilike(like), Scholarship.tags.ilike(like)))
    return jsonify([serialize(s) for s in query.order_by(Scholarship.deadline.asc()).all()])


@scholarships_bp.get('/admin')
def admin_scholarships():
    if not admin_required(): return jsonify(message='Admin only'), 403
    return jsonify([serialize(s) for s in Scholarship.query.order_by(Scholarship.created_at.desc()).all()])


@scholarships_bp.post('')
def create_scholarship():
    if not admin_required(): return jsonify(message='Admin only'), 403
    data = request.get_json(silent=True) or {}
    if not data.get('title') or not data.get('provider') or not data.get('description'):
        return jsonify(message='Title, provider and description are required'), 400
    try:
        scholarship = Scholarship(); apply_fields(scholarship, data)
        db.session.add(scholarship); db.session.commit()
        return jsonify(scholarship=serialize(scholarship)), 201
    except (TypeError, ValueError):
        db.session.rollback(); return jsonify(message='Invalid scholarship values'), 400


@scholarships_bp.put('/<int:scholarship_id>')
def update_scholarship(scholarship_id):
    if not admin_required(): return jsonify(message='Admin only'), 403
    scholarship = Scholarship.query.get_or_404(scholarship_id)
    try:
        apply_fields(scholarship, request.get_json(silent=True) or {}); db.session.commit()
        return jsonify(scholarship=serialize(scholarship))
    except (TypeError, ValueError):
        db.session.rollback(); return jsonify(message='Invalid scholarship values'), 400


@scholarships_bp.delete('/<int:scholarship_id>')
def delete_scholarship(scholarship_id):
    if not admin_required(): return jsonify(message='Admin only'), 403
    scholarship = Scholarship.query.get_or_404(scholarship_id)
    scholarship.active = False; db.session.commit()
    return jsonify(message='Scholarship deactivated', scholarship=serialize(scholarship))
