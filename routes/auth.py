from flask import Blueprint, jsonify, request, session
from models import User, db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.post('/register')
def register():
    data = request.get_json(silent=True) or request.form
    name, email, password = data.get('name'), data.get('email'), data.get('password')
    if not all([name, email, password]):
        return jsonify(message='Name, email and password are required'), 400
    if User.query.filter_by(email=email.strip().lower()).first():
        return jsonify(message='Email already registered'), 409
    user = User(name=name.strip(), email=email.strip().lower())
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    session['user_id'] = user.id
    return jsonify(message='Account created', user={'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role}), 201


@auth_bp.post('/login')
def login():
    data = request.get_json(silent=True) or request.form
    user = User.query.filter_by(email=(data.get('email') or '').strip().lower()).first()
    if not user or not user.check_password(data.get('password') or ''):
        return jsonify(message='Invalid credentials'), 401
    session['user_id'] = user.id
    return jsonify(message='Login successful', user={'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role})


@auth_bp.post('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify(message='Logged out')


@auth_bp.get('/me')
def me():
    user = User.query.get(session.get('user_id')) if session.get('user_id') else None
    if not user:
        return jsonify(message='Authentication required'), 401
    return jsonify(user={'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role, 'course': user.course, 'department': user.department, 'year': user.year, 'cgpa': user.cgpa, 'annual_income': user.annual_income, 'category': user.category, 'interests': user.interests})


def current_user():
    return User.query.get(session.get('user_id')) if session.get('user_id') else None
