from main import app, db
from main import Faculty, Department, Lecturer
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        db.create_all()

        if Faculty.query.first():
            return

        fti = Faculty(name='Fakultas Teknologi Informasi')
        fb = Faculty(name='Fakultas Bisnis dan Ekonomi')
        fki = Faculty(name='Fakultas Komunikasi dan Informatika')
        db.session.add_all([fti, fb, fki])
        db.session.commit()

        ti_d = Department(name='Teknik Informatika', faculty=fti)
        si_d = Department(name='Sistem Informasi', faculty=fti)
        tk_d = Department(name='Teknik Komputer', faculty=fti)

        mi_d = Department(name='Manajemen Informatika', faculty=fb)
        mt_d = Department(name='Magister Teknologi Informasi', faculty=fb)

        ilkom_d = Department(name='Ilmu Komunikasi', faculty=fki)
        dkv_d = Department(name='Desain Komunikasi Visual', faculty=fki)
        fi_d = Department(name='Film dan Televisi', faculty=fki)

        db.session.add_all([ti_d, si_d, tk_d, mi_d, mt_d, ilkom_d, dkv_d, fi_d])
        db.session.commit()

        lecturers = [
            Lecturer(
                nik='20240101',
                name='Dr. Muhammad Nur Ashif, M.Kom.',
                password=generate_password_hash('amikom2024'),
                department=ti_d
            ),
            Lecturer(
                nik='20240102',
                name='Dr. Sri Wahyuni, M.Kom.',
                password=generate_password_hash('amikom2024'),
                department=si_d
            ),
            Lecturer(
                nik='20240103',
                name='Dr. Joko Susanto, M.Kom.',
                password=generate_password_hash('amikom2024'),
                department=tk_d
            ),
            Lecturer(
                nik='20240104',
                name='Dr. Agus Setiawan, M.M.',
                password=generate_password_hash('amikom2024'),
                department=mi_d
            ),
            Lecturer(
                nik='20240105',
                name='Dr. Rina Suryani, M.T.',
                password=generate_password_hash('amikom2024'),
                department=mt_d
            ),
            Lecturer(
                nik='20240106',
                name='Dr. Dian Fitriani, S.I.Kom.',
                password=generate_password_hash('amikom2024'),
                department=ilkom_d
            ),
            Lecturer(
                nik='20240107',
                name='Dr. Bambang Pratama, M.Sn.',
                password=generate_password_hash('amikom2024'),
                department=dkv_d
            ),
            Lecturer(
                nik='20240108',
                name='Dr. Anna Rahmawati, M.Film.',
                password=generate_password_hash('amikom2024'),
                department=fi_d
            )
            ,
            Lecturer(
                nik='20240109',
                name='M. Nuraminudin, M.Kom',
                password=generate_password_hash('amikom2024'),
                department=ti_d
            )
        ]
        db.session.add_all(lecturers)
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Database berhasil diinisialisasi sesuai dengan data Universitas Amikom Yogyakarta!")
