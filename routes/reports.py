import csv
import io
from flask import Blueprint, jsonify, request, Response
from models import User, Scholarship, Application, Document, db
from routes.auth import current_user

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')


def admin():
    user = current_user()
    return user if user and user.role == 'admin' else None


@reports_bp.get('/summary')
def summary():
    if not admin(): return jsonify(message='Admin only'), 403
    return jsonify({
        'students': User.query.filter_by(role='student').count(),
        'scholarships': Scholarship.query.filter_by(active=True).count(),
        'applications': Application.query.count(),
        'documents': Document.query.count(),
        'eligible': Application.query.filter_by(eligibility_result='Eligible').count(),
        'not_eligible': Application.query.filter_by(eligibility_result='Not Eligible').count(),
        'approved': Application.query.filter_by(status='Approved').count(),
        'rejected': Application.query.filter_by(status='Rejected').count(),
        'pending': Application.query.filter(Application.status.in_(['Submitted','Under Review','AI Verified','Documents Verified'])).count(),
    })


@reports_bp.get('/applications-by-status')
def applications_by_status():
    if not admin(): return jsonify(message='Admin only'), 403
    rows = db.session.query(Application.status, db.func.count(Application.id)).group_by(Application.status).all()
    return jsonify([{'status': status, 'count': count} for status, count in rows])


@reports_bp.get('/applications-by-scholarship')
def applications_by_scholarship():
    if not admin(): return jsonify(message='Admin only'), 403
    rows = db.session.query(Scholarship.title, db.func.count(Application.id)).outerjoin(Application).group_by(Scholarship.id).order_by(db.func.count(Application.id).desc()).all()
    return jsonify([{'scholarship': title, 'count': count} for title, count in rows])


@reports_bp.get('/applications')
def all_applications():
    if not admin(): return jsonify(message='Admin only'), 403
    rows = Application.query.order_by(Application.submitted_at.desc()).all()
    return jsonify([{'id': a.id, 'student': a.student.name, 'email': a.student.email, 'scholarship': a.scholarship.title,
                     'status': a.status, 'eligibility_result': a.eligibility_result, 'eligibility_score': a.eligibility_score,
                     'submitted_at': a.submitted_at.isoformat(), 'remarks': a.remarks} for a in rows])


@reports_bp.get('/applications.csv')
def export_applications():
    if not admin(): return jsonify(message='Admin only'), 403
    output = io.StringIO(); writer = csv.writer(output)
    writer.writerow(['Application ID','Student','Email','Scholarship','Status','Eligibility','Score','Submitted At','Remarks'])
    for a in Application.query.order_by(Application.submitted_at.desc()).all():
        writer.writerow([a.id,a.student.name,a.student.email,a.scholarship.title,a.status,a.eligibility_result,a.eligibility_score,a.submitted_at.isoformat(),a.remarks or ''])
    return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition':'attachment; filename=scholarship_applications.csv'})
