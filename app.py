from pathlib import Path
from flask import Flask, render_template
from config import Config
from models import db
from routes.auth import auth_bp, current_user
from routes.scholarships import scholarships_bp
from routes.eligibility import eligibility_bp
from routes.applications import applications_bp
from routes.reports import reports_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(scholarships_bp)
    app.register_blueprint(eligibility_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(reports_bp)
    with app.app_context():
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
        db.create_all()

    @app.get('/')
    def index():
        return render_template('index.html')

    @app.get('/admin')
    def admin_dashboard():
        user = current_user()
        if not user or user.role != 'admin':
            return render_template('index.html')
        return render_template('admin.html')

    @app.get('/health')
    def health():
        return {'ok': True, 'service': 'scholarai-flask'}

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
