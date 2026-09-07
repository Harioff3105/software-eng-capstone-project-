from datetime import date
from flask import Blueprint, jsonify, request
from models import Scholarship, db
from routes.auth import current_user

scholarships_bp = Blueprint('scholarships', __name__, url_prefix='/api/scholarships')


def serialize(s):
    return {'id': s.id, 'title': s.title, 'provider': s.provider, 'description': s.description, 'amount': s.amount, 'deadline': s.deadline.isoformat() if s.deadline else None, 'min_cgpa': s.min_cgpa, 'max_income': s.max_income, 'eligible_category': s.eligible_category, 'eligible_courses': s.eligible_courses, 'tags': s.tags, 'active': s.active}


@scholarships_bp.get('')
def list_scholarships():
    q = (request.args.get('q') or '').strip()
    query = Scholarship.query.filter_by(active=True)
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(Scholarship.title.ilike(like), Scholarship.provider.ilike(like), Scholarship.tags.ilike(like)))
    return jsonify([serialize(s) for s in query.order_by(Scholarship.deadline.asc()).all()])


@scholarships_bp.post('')
def create_scholarship():
    user = current_user()
    if not user or user.role != 'admin':
        return jsonify(message='Admin only'), 403
    data = request.get_json(silent=True) or {}
    scholarship = Scholarship(title=data.get('title',''), provider=data.get('provider',''), description=data.get('description',''), amount=data.get('amount'), min_cgpa=data.get('min_cgpa'), max_income=data.get('max_income'), eligible_category=data.get('eligible_category'), eligible_courses=data.get('eligible_courses'), tags=data.get('tags'))
    if data.get('deadline'):
        scholarship.deadline = date.fromisoformat(data['deadline'])
    if not scholarship.title or not scholarship.provider or not scholarship.description:
        return jsonify(message='Title, provider and description are required'), 400
    db.session.add(scholarship)
    db.session.commit()
    return jsonify(scholarship=serialize(scholarship)), 201
