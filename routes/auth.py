from flask import Blueprint, jsonify, request, session
from models import User, db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def user_json(user):
    return {'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role,
            'course': user.course, 'department': user.department, 'year': user.year,
            'cgpa': user.cgpa, 'annual_income': user.annual_income,
            'category': user.category, 'interests': user.interests}


@auth_bp.post('/register')
def register():
    data = request.get_json(silent=True) or request.form
    name, email, password = data.get('name'), data.get('email'), data.get('password')
    if not all([name, email, password]):
        return jsonify(message='Name, email and password are required'), 400
    email = email.strip().lower()
    if User.query.filter_by(email=email).first():
        return jsonify(message='Email already registered'), 409
    if len(password) < 8:
        return jsonify(message='Password must contain at least 8 characters'), 400
    user = User(name=name.strip(), email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    session['user_id'] = user.id
    return jsonify(message='Account created', user=user_json(user)), 201


@auth_bp.post('/login')
def login():
    data = request.get_json(silent=True) or request.form
    user = User.query.filter_by(email=(data.get('email') or '').strip().lower()).first()
    if not user or not user.check_password(data.get('password') or ''):
        return jsonify(message='Invalid credentials'), 401
    session['user_id'] = user.id
    return jsonify(message='Login successful', user=user_json(user))


@auth_bp.post('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify(message='Logged out')


@auth_bp.get('/me')
def me():
    user = current_user()
    if not user:
        return jsonify(message='Authentication required'), 401
    return jsonify(user=user_json(user))


@auth_bp.put('/profile')
def update_profile():
    user = current_user()
    if not user:
        return jsonify(message='Authentication required'), 401
    data = request.get_json(silent=True) or {}
    for field in ('name', 'course', 'department', 'year', 'category', 'interests'):
        if field in data:
            setattr(user, field, str(data[field]).strip())
    for field in ('cgpa', 'annual_income'):
        if field in data and data[field] not in ('', None):
            try:
                setattr(user, field, float(data[field]))
            except (TypeError, ValueError):
                return jsonify(message=f'Invalid {field}'), 400
    db.session.commit()
    return jsonify(message='Profile updated', user=user_json(user))


def current_user():
    return User.query.get(session.get('user_id')) if session.get('user_id') else None
