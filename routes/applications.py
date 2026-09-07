from flask import Blueprint, jsonify, request
from models import Application, Scholarship, db
from routes.auth import current_user

applications_bp = Blueprint('applications', __name__, url_prefix='/api/applications')


def serialize(a):
    return {'id': a.id, 'scholarship_id': a.scholarship_id, 'scholarship': a.scholarship.title if a.scholarship else None, 'status': a.status, 'eligibility_result': a.eligibility_result, 'eligibility_score': a.eligibility_score, 'ai_explanation': a.ai_explanation, 'remarks': a.remarks, 'submitted_at': a.submitted_at.isoformat(), 'updated_at': a.updated_at.isoformat()}


@applications_bp.post('')
def submit_application():
    user = current_user()
    if not user:
        return jsonify(message='Authentication required'), 401
    data = request.get_json(silent=True) or {}
    scholarship = Scholarship.query.get(data.get('scholarship_id'))
    if not scholarship or not scholarship.active:
        return jsonify(message='Scholarship not found'), 404
    if Application.query.filter_by(student_id=user.id, scholarship_id=scholarship.id).first():
        return jsonify(message='You have already applied for this scholarship'), 409
    application = Application(student_id=user.id, scholarship_id=scholarship.id)
    db.session.add(application)
    db.session.commit()
    return jsonify(application=serialize(application)), 201


@applications_bp.get('/me')
def my_applications():
    user = current_user()
    if not user:
        return jsonify(message='Authentication required'), 401
    return jsonify([serialize(a) for a in Application.query.filter_by(student_id=user.id).order_by(Application.submitted_at.desc()).all()])


@applications_bp.patch('/<int:application_id>/status')
def update_status(application_id):
    user = current_user()
    if not user or user.role != 'admin':
        return jsonify(message='Admin only'), 403
    application = Application.query.get_or_404(application_id)
    status = (request.get_json(silent=True) or {}).get('status')
    allowed = {'Submitted', 'Under Review', 'AI Verified', 'Documents Verified', 'Approved', 'Rejected'}
    if status not in allowed:
        return jsonify(message='Invalid application status'), 400
    application.status = status
    db.session.commit()
    return jsonify(application=serialize(application))
