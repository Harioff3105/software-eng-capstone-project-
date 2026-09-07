from flask import Blueprint, jsonify
from models import User, Scholarship, Application, Document, db
from routes.auth import current_user

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')


@reports_bp.get('/summary')
def summary():
    user = current_user()
    if not user or user.role != 'admin':
        return jsonify(message='Admin only'), 403
    total = Application.query.count()
    return jsonify({
        'students': User.query.filter_by(role='student').count(),
        'scholarships': Scholarship.query.filter_by(active=True).count(),
        'applications': total,
        'documents': Document.query.count(),
        'eligible': Application.query.filter_by(eligibility_result='Eligible').count(),
        'not_eligible': Application.query.filter_by(eligibility_result='Not Eligible').count(),
        'approved': Application.query.filter_by(status='Approved').count(),
        'rejected': Application.query.filter_by(status='Rejected').count(),
        'pending': Application.query.filter(Application.status.in_(['Submitted', 'Under Review', 'AI Verified', 'Documents Verified'])).count(),
    })


@reports_bp.get('/applications-by-status')
def applications_by_status():
    user = current_user()
    if not user or user.role != 'admin':
        return jsonify(message='Admin only'), 403
    rows = db.session.query(Application.status, db.func.count(Application.id)).group_by(Application.status).all()
    return jsonify([{'status': status, 'count': count} for status, count in rows])
