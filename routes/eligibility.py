import json
from flask import Blueprint, jsonify, request, current_app
from models import Application, Scholarship, db
from routes.auth import current_user

eligibility_bp = Blueprint('eligibility', __name__, url_prefix='/api/eligibility')


def basic_check(user, scholarship):
    reasons = []
    passed = True
    if scholarship.min_cgpa is not None:
        if user.cgpa is None:
            passed = False; reasons.append('CGPA is required.')
        elif user.cgpa < scholarship.min_cgpa:
            passed = False; reasons.append(f'CGPA must be at least {scholarship.min_cgpa}.')
    if scholarship.max_income is not None:
        if user.annual_income is None:
            passed = False; reasons.append('Annual family income is required.')
        elif user.annual_income > scholarship.max_income:
            passed = False; reasons.append(f'Annual income must not exceed {scholarship.max_income}.')
    if scholarship.eligible_category:
        allowed = {x.strip().lower() for x in scholarship.eligible_category.split(',')}
        if not user.category or user.category.lower() not in allowed:
            passed = False; reasons.append('Category requirement is not satisfied.')
    if scholarship.eligible_courses:
        allowed = {x.strip().lower() for x in scholarship.eligible_courses.split(',')}
        if not user.course or user.course.lower() not in allowed:
            passed = False; reasons.append('Course requirement is not satisfied.')
    return passed, reasons


@eligibility_bp.post('/check/<int:scholarship_id>')
def check_eligibility(scholarship_id):
    user = current_user()
    if not user:
        return jsonify(message='Authentication required'), 401
    scholarship = Scholarship.query.get_or_404(scholarship_id)
    passed, reasons = basic_check(user, scholarship)
    result = {'eligible': passed, 'score': 1.0 if passed else 0.0, 'explanation': ' '.join(reasons) if reasons else 'The available profile information satisfies the configured eligibility criteria.'}
    if current_app.config.get('GEMINI_API_KEY'):
        try:
            from google import genai
            client = genai.Client(api_key=current_app.config['GEMINI_API_KEY'])
            prompt = f"Evaluate scholarship eligibility using only the supplied facts. Return JSON with eligible (boolean), score (0 to 1), explanation (string), missing_information (array). Student: {json.dumps({'course': user.course, 'department': user.department, 'year': user.year, 'cgpa': user.cgpa, 'annual_income': user.annual_income, 'category': user.category, 'interests': user.interests})}. Scholarship: {json.dumps({'title': scholarship.title, 'provider': scholarship.provider, 'min_cgpa': scholarship.min_cgpa, 'max_income': scholarship.max_income, 'eligible_category': scholarship.eligible_category, 'eligible_courses': scholarship.eligible_courses, 'tags': scholarship.tags})}."
            response = client.models.generate_content(model=current_app.config['GEMINI_MODEL'], contents=prompt)
            text = response.text.strip().replace('```json', '').replace('```', '').strip()
            result.update(json.loads(text))
        except Exception:
            pass
    application = Application.query.filter_by(student_id=user.id, scholarship_id=scholarship.id).first()
    if application:
        application.eligibility_result = 'Eligible' if result['eligible'] else 'Not Eligible'
        application.eligibility_score = float(result.get('score', 0))
        application.ai_explanation = result.get('explanation', '')
        application.status = 'AI Verified'
        db.session.commit()
    return jsonify(result=result)
