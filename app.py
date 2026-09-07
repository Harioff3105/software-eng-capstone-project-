from flask import Flask
from config import Config
from models import db
from routes.auth import auth_bp
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
        db.create_all()

    @app.get('/health')
    def health():
        return {'ok': True, 'service': 'scholarai-flask'}

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
