from main import app, db
from main import Faculty, Department, Lecturer
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        db.create_all()

        if Faculty.query.first():
            return

        # Deklarasi fakultas yang baru
        fik = Faculty(name='Fakultas Ilmu Komputer')
        fes = Faculty(name='Fakultas Ekonomi dan Sosial')
        fst = Faculty(name='Fakultas Sains dan Teknologi')
        db.session.add_all([fik, fes, fst])
        db.session.commit()

        # Penyesuaian departemen dengan fakultas yang sesuai
        d3_ti_d = Department(name='D3 Teknik Informatika', faculty=fik)
        d3_mi_d = Department(name='D3 Manajemen Informatika', faculty=fik)
        s1_informatika_d = Department(name='S1 Informatika', faculty=fik)
        s1_si_d = Department(name='S1 Sistem Informasi', faculty=fik)
        s1_ti_d = Department(name='S1 Teknologi Informasi', faculty=fik)
        s1_tk_d = Department(name='S1 Teknik Komputer', faculty=fik)

        # Fakultas Ekonomi dan Sosial (FES) - Departemen yang baru ditambahkan
        s1_akuntansi_d = Department(name='S1 Akuntansi', faculty=fes)
        s1_ekonomi_d = Department(name='S1 Ekonomi', faculty=fes)
        s1_hubungan_internasional_d = Department(name='S1 Hubungan Internasional', faculty=fes)
        s1_ilmu_komunikasi_d = Department(name='S1 Ilmu Komunikasi', faculty=fes)
        s1_ilmu_pemerintahan_d = Department(name='S1 Ilmu Pemerintahan', faculty=fes)
        s1_kewirausahaan_d = Department(name='S1 Kewirausahaan', faculty=fes)

        # Fakultas Sains dan Teknologi (FST) - Departemen yang baru ditambahkan
        s1_arsitektur_d = Department(name='S1 Arsitektur', faculty=fst)
        s1_perencanaan_wilayah_kota_d = Department(name='S1 Perencanaan Wilayah dan Kota', faculty=fst)
        s1_geografi_d = Department(name='S1 Geografi', faculty=fst)

        bio_d = Department(name='S1 Biologi', faculty=fst)
        kimia_d = Department(name='S1 Kimia', faculty=fst)
        fisika_d = Department(name='S1 Fisika', faculty=fst)

        db.session.add_all([d3_ti_d, d3_mi_d, s1_informatika_d, s1_si_d, s1_ti_d, s1_tk_d, 
                            s1_akuntansi_d, s1_ekonomi_d, s1_hubungan_internasional_d, 
                            s1_ilmu_komunikasi_d, s1_ilmu_pemerintahan_d, s1_kewirausahaan_d, 
                            s1_arsitektur_d, s1_perencanaan_wilayah_kota_d, s1_geografi_d,
                            bio_d, kimia_d, fisika_d])
        db.session.commit()

        # Penyesuaian daftar dosen
        lecturers = [
            Lecturer(
                nik='20240101',
                name='Dr. Muhammad Nur Ashif, M.Kom.',
                password=generate_password_hash('amikom2024'),
                department=d3_ti_d
            ),
            Lecturer(
                nik='20240102',
                name='Dr. Sri Wahyuni, M.Kom.',
                password=generate_password_hash('amikom2024'),
                department=s1_si_d
            ),
            Lecturer(
                nik='20240103',
                name='Dr. Agus Setiawan, M.M.',
                password=generate_password_hash('amikom2024'),
                department=d3_mi_d
            ),
            Lecturer(
                nik='20240104',
                name='Dr. Dian Fitriani, S.I.Kom.',
                password=generate_password_hash('amikom2024'),
                department=s1_ilmu_komunikasi_d
            ),
            Lecturer(
                nik='20240105',
                name='Dr. Bambang Pratama, M.Sn.',
                password=generate_password_hash('amikom2024'),
                department=s1_arsitektur_d
            ),
            Lecturer(
                nik='20240106',
                name='Dr. Anna Rahmawati, M.Film.',
                password=generate_password_hash('amikom2024'),
                department=s1_perencanaan_wilayah_kota_d
            ),
            Lecturer(
                nik='20240107',
                name='M. Nuraminudin, M.Kom.',
                password=generate_password_hash('amikom2024'),
                department=d3_ti_d
            ),
            Lecturer(
                nik='20240108',
                name='Anggit Ferdita Nugraha, S.T., M.Eng.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            ),
            Lecturer(
                nik='20240109',
                name='Banu Santoso, S.T., M.Eng.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            ),
            Lecturer(
                nik='20240110',
                name='Dony Ariyus, M.Kom.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            ),
            Lecturer(
                nik='20240111',
                name='Jeki Kuswanto, M.Kom.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            ),
            Lecturer(
                nik='20240112',
                name='Joko Dwi Santoso, M.Kom.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            ),
            Lecturer(
                nik='20240113',
                name='Melwin Syafrizal, S.Kom., M.Eng.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            ),
            Lecturer(
                nik='20240114',
                name='Muhammad Koprawi, S.Kom., M.Eng.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            ),
            Lecturer(
                nik='20240115',
                name='Rina Pramitasari, S.Si., M.Cs.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            ),
            Lecturer(
                nik='20240116',
                name='Senie Destya, M.Kom.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            ),
            Lecturer(
                nik='20240117',
                name='Wahid Miftahul Ashari, S.Kom., M.T.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            ),
            Lecturer(
                nik='20240118',
                name='Wahyu Sukestyastama Putra, S.T., M.Eng.',
                password=generate_password_hash('amikom2024'),
                department=s1_tk_d
            )
        ]
        db.session.add_all(lecturers)
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Database berhasil diinisialisasi sesuai dengan data Universitas Amikom Yogyakarta!")
