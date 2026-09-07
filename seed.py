import os
from datetime import date, timedelta
from app import app
from models import db, User, Scholarship


SCHOLARSHIPS = [
    {'title':'National Merit Technology Scholarship','provider':'National Education Foundation','description':'Merit support for undergraduate students pursuing technology and computing disciplines.','amount':50000,'min_cgpa':7.5,'max_income':800000,'eligible_courses':'B.Tech, B.E., B.Sc','eligible_category':'All','tags':'technology, merit, engineering'},
    {'title':'Women in Computing Scholarship','provider':'Digital Futures Trust','description':'Financial assistance for students building careers in computing, software and data disciplines.','amount':75000,'min_cgpa':7.0,'max_income':1000000,'eligible_courses':'B.Tech IT, B.Tech CSE, B.Sc CS','eligible_category':'Women','tags':'women, computing, software'},
    {'title':'Future Data Science Fellowship','provider':'Data Innovation Council','description':'Scholarship for students interested in data science, artificial intelligence and analytics.','amount':60000,'min_cgpa':7.5,'max_income':900000,'eligible_courses':'B.Tech, B.Sc, MCA','eligible_category':'All','tags':'data science, AI, analytics'},
    {'title':'STEM Excellence Grant','provider':'STEM Scholars India','description':'Academic grant supporting high-performing students in science, technology, engineering and mathematics.','amount':40000,'min_cgpa':8.0,'max_income':700000,'eligible_courses':'B.Tech, B.E., B.Sc','eligible_category':'All','tags':'STEM, excellence, engineering'},
    {'title':'Inclusive Education Support Scholarship','provider':'Student Opportunity Foundation','description':'Need-aware educational assistance designed to widen access to higher education.','amount':35000,'min_cgpa':6.5,'max_income':500000,'eligible_courses':'Any undergraduate programme','eligible_category':'SC, ST, OBC, EWS','tags':'need based, inclusion, education'},
]

with app.app_context():
    db.create_all()
    for item in SCHOLARSHIPS:
        if not Scholarship.query.filter_by(title=item['title']).first():
            db.session.add(Scholarship(deadline=date.today()+timedelta(days=60), **item))
    admin_email=os.getenv('ADMIN_EMAIL','admin@scholarai.local').strip().lower()
    admin_password=os.getenv('ADMIN_PASSWORD','ChangeMe123!')
    admin=User.query.filter_by(email=admin_email).first()
    if not admin:
        admin=User(name='ScholarAI Administrator',email=admin_email,role='admin')
        admin.set_password(admin_password); db.session.add(admin)
    db.session.commit()
    print('Seed complete.')
    print(f'Admin email: {admin_email}')
    print('Admin password is controlled by ADMIN_PASSWORD (default is for local demo only).')
