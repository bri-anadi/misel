from main import app, db
from main import Faculty, Department, Lecturer
from werkzeug.security import generate_password_hash
import sys
from sqlalchemy.exc import SQLAlchemyError

def init_db():
    try:
        with app.app_context():

            db.create_all()

            if Faculty.query.first():
                print("Database already initialized!")
                return

            print("Creating faculties...")
            fik = Faculty(name='Fakultas Ilmu Komputer')
            fes = Faculty(name='Fakultas Ekonomi dan Sosial')
            fst = Faculty(name='Fakultas Sains dan Teknologi')

            try:
                db.session.add_all([fik, fes, fst])
                db.session.commit()
                print("✓ Faculties created successfully")
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"Error creating faculties: {str(e)}")
                sys.exit(1)

            # Create departments
            print("Creating departments...")
            departments = [
                # FIK Departments
                Department(name='D3 Teknik Informatika', faculty=fik),
                Department(name='D3 Manajemen Informatika', faculty=fik),
                Department(name='S1 Informatika', faculty=fik),
                Department(name='S1 Sistem Informasi', faculty=fik),
                Department(name='S1 Teknologi Informasi', faculty=fik),
                Department(name='S1 Teknik Komputer', faculty=fik),

                # FES Departments
                Department(name='S1 Akuntansi', faculty=fes),
                Department(name='S1 Ekonomi', faculty=fes),
                Department(name='S1 Hubungan Internasional', faculty=fes),
                Department(name='S1 Ilmu Komunikasi', faculty=fes),
                Department(name='S1 Ilmu Pemerintahan', faculty=fes),
                Department(name='S1 Kewirausahaan', faculty=fes),

                # FST Departments
                Department(name='S1 Arsitektur', faculty=fst),
                Department(name='S1 Perencanaan Wilayah dan Kota', faculty=fst),
                Department(name='S1 Geografi', faculty=fst),
            ]

            try:
                db.session.add_all(departments)
                db.session.commit()
                print("✓ Departments created successfully")
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"Error creating departments: {str(e)}")
                sys.exit(1)

            # Create reference dictionary for departments
            dept_dict = {dept.name: dept for dept in Department.query.all()}

            # Create lecturers
            print("Creating lecturers...")
            lecturers = [
                {
                    'nik': '20240101',
                    'name': 'Dr. Muhammad Nur Ashif, M.Kom.',
                    'dept': 'D3 Teknik Informatika'
                },
                {
                    'nik': '20240102',
                    'name': 'Dr. Sri Wahyuni, M.Kom.',
                    'dept': 'S1 Sistem Informasi'
                },
                {
                    'nik': '20240103',
                    'name': 'Dr. Agus Setiawan, M.M.',
                    'dept': 'D3 Manajemen Informatika'
                },
                {
                    'nik': '20240104',
                    'name': 'Dr. Dian Fitriani, S.I.Kom.',
                    'dept': 'S1 Ilmu Komunikasi'
                },
                {
                    'nik': '20240105',
                    'name': 'Dr. Bambang Pratama, M.Sn.',
                    'dept': 'S1 Arsitektur'
                },
                {
                    'nik': '20240106',
                    'name': 'Dr. Anna Rahmawati, M.Film.',
                    'dept': 'S1 Perencanaan Wilayah dan Kota'
                },
                {
                    'nik': '20240107',
                    'name': 'M. Nuraminudin, M.Kom.',
                    'dept': 'D3 Teknik Informatika'
                },
            ] + [
                {
                    'nik': f'2024011{i}',
                    'name': name,
                    'dept': 'S1 Teknik Komputer'
                } for i, name in enumerate([
                    'Anggit Ferdita Nugraha, S.T., M.Eng.',
                    'Banu Santoso, S.T., M.Eng.',
                    'Dony Ariyus, M.Kom.',
                    'Jeki Kuswanto, M.Kom.',
                    'Joko Dwi Santoso, M.Kom.',
                    'Melwin Syafrizal, S.Kom., M.Eng.',
                    'Muhammad Koprawi, S.Kom., M.Eng.',
                    'Rina Pramitasari, S.Si., M.Cs.',
                    'Senie Destya, M.Kom.',
                    'Wahid Miftahul Ashari, S.Kom., M.T.',
                    'Wahyu Sukestyastama Putra, S.T., M.Eng.'
                ], start=8)
            ]

            lecturer_objects = []
            for lecturer in lecturers:
                lecturer_objects.append(Lecturer(
                    nik=lecturer['nik'],
                    name=lecturer['name'],
                    password=generate_password_hash('amikom2024'),
                    department=dept_dict[lecturer['dept']]
                ))

            try:
                db.session.add_all(lecturer_objects)
                db.session.commit()
                print("✓ Lecturers created successfully")
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"Error creating lecturers: {str(e)}")
                sys.exit(1)

            print("\n✓ Database initialization completed successfully!")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    init_db()