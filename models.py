from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    course = db.Column(db.String(120))
    department = db.Column(db.String(120))
    year = db.Column(db.String(20))
    cgpa = db.Column(db.Float)
    annual_income = db.Column(db.Float)
    category = db.Column(db.String(80))
    interests = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    applications = db.relationship('Application', back_populates='student', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    provider = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float)
    deadline = db.Column(db.Date)
    min_cgpa = db.Column(db.Float)
    max_income = db.Column(db.Float)
    eligible_category = db.Column(db.String(200))
    eligible_courses = db.Column(db.String(500))
    tags = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    applications = db.relationship('Application', back_populates='scholarship')


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarship.id'), nullable=False)
    status = db.Column(db.String(40), default='Submitted', nullable=False)
    eligibility_result = db.Column(db.String(30))
    eligibility_score = db.Column(db.Float)
    ai_explanation = db.Column(db.Text)
    remarks = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    student = db.relationship('User', back_populates='applications')
    scholarship = db.relationship('Scholarship', back_populates='applications')
    __table_args__ = (db.UniqueConstraint('student_id', 'scholarship_id', name='uq_student_scholarship'),)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
