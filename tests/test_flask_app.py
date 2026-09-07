import os
import tempfile
import unittest

os.environ['DATABASE_URL'] = 'sqlite:///' + os.path.join(tempfile.gettempdir(), 'scholarai_test.db')
os.environ['SECRET_KEY'] = 'test-secret'

from app import create_app
from models import db, Scholarship


class ScholarAITests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:', SECRET_KEY='test-secret')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all(); db.create_all()
            db.session.add(Scholarship(title='Test Scholarship',provider='Test Provider',description='Test',amount=10000,min_cgpa=7.0,max_income=500000,eligible_category='All',eligible_courses='B.Tech',tags='test'))
            db.session.commit()

    def test_health(self):
        self.assertEqual(self.client.get('/health').status_code, 200)

    def test_register_login_profile_and_apply(self):
        r=self.client.post('/api/auth/register',json={'name':'Test Student','email':'student@test.local','password':'Password123'})
        self.assertEqual(r.status_code,201)
        self.assertEqual(self.client.put('/api/auth/profile',json={'course':'B.Tech IT','cgpa':8.2,'annual_income':300000,'category':'All'}).status_code,200)
        self.assertEqual(self.client.post('/api/applications',json={'scholarship_id':1}).status_code,201)
        self.assertEqual(self.client.post('/api/applications',json={'scholarship_id':1}).status_code,409)
        self.assertEqual(self.client.get('/api/applications/me').status_code,200)

    def test_admin_guard(self):
        self.assertEqual(self.client.get('/api/reports/summary').status_code,403)


if __name__ == '__main__':
    unittest.main()
