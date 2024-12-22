from main import app, db
from main import Faculty, Department, Lecturer
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        db.create_all()

        if Faculty.query.first():
            return

        ft = Faculty(name='Faculty of Technology')
        fb = Faculty(name='Faculty of Business')
        fa = Faculty(name='Faculty of Arts and Design')
        db.session.add_all([ft, fb, fa])
        db.session.commit()

        cs_d = Department(name='Computer Science', faculty=ft)
        is_d = Department(name='Information Systems', faculty=ft)
        ce_d = Department(name='Computer Engineering', faculty=ft)
        ba_d = Department(name='Business Administration', faculty=fb)
        dm_d = Department(name='Digital Marketing', faculty=fb)
        ad_d = Department(name='Art and Design', faculty=fa)

        db.session.add_all([cs_d, is_d, ce_d, ba_d, dm_d, ad_d])
        db.session.commit()
        
        lecturers = [
            Lecturer(
                nik='20240301',
                name='Dr. John Smith, Ph.D.',
                password=generate_password_hash('campus2024'),
                department=cs_d
            ),
            Lecturer(
                nik='20240302',
                name='Prof. Sarah Johnson, Ph.D.',
                password=generate_password_hash('campus2024'),
                department=cs_d
            ),
            Lecturer(
                nik='20240303',
                name='Dr. Michael Chen, M.Sc.',
                password=generate_password_hash('campus2024'),
                department=is_d
            ),
            Lecturer(
                nik='20240304',
                name='Dr. Emily Brown, Ph.D.',
                password=generate_password_hash('campus2024'),
                department=is_d
            ),
            Lecturer(
                nik='20240305',
                name='Prof. David Wilson, Ph.D.',
                password=generate_password_hash('campus2024'),
                department=ce_d
            ),
            Lecturer(
                nik='20240306',
                name='Dr. Jessica Lee, MBA.',
                password=generate_password_hash('campus2024'),
                department=ba_d
            ),
            Lecturer(
                nik='20240307',
                name='Dr. Robert Taylor, Ph.D.',
                password=generate_password_hash('campus2024'),
                department=dm_d
            ),
            Lecturer(
                nik='20240308',
                name='Dr. Lisa Anderson, Ph.D.',
                password=generate_password_hash('campus2024'),
                department=cs_d
            ),
            Lecturer(
                nik='20240309',
                name='Prof. Thomas Moore, M.Sc.',
                password=generate_password_hash('campus2024'),
                department=is_d
            ),
            Lecturer(
                nik='20240310',
                name='Dr. Rachel Martinez, M.F.A.',
                password=generate_password_hash('campus2024'),
                department=ad_d
            )
        ]
        db.session.add_all(lecturers)
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")