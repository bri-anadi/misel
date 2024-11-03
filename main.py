# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from io import BytesIO
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from re import sub
from unicodedata import normalize
from unidecode import unidecode
import pandas as pd
import tempfile
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Models
class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    departments = db.relationship('Department', backref='faculty', lazy=True)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    lecturers = db.relationship('Lecturer', backref='department', lazy=True)

class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    schedules = db.relationship('Schedule', backref='lecturer', lazy=True)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'), nullable=False)


def slugify(text):
    """
    Convert text to URL-friendly slug format.
    Example: "Dr. Jane Smith, M.Sc." -> "dr-jane-smith-m-sc"
    """
    # Normalize unicode characters and convert to ASCII
    text = unidecode(text)

    # Convert to lowercase
    text = text.lower()

    # Replace special characters with spaces
    text = sub(r'[^\w\s-]', ' ', text)

    # Replace multiple spaces with single hyphen
    text = sub(r'\s+', '-', text.strip())

    # Remove duplicate hyphens
    text = sub(r'-+', '-', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    return text

def deslugify(slug):
    """
    Convert URL slug back to original format for database queries.
    Example: "jane-smith-m-sc" -> "Jane Smith, M.Sc."
    """
    # Replace hyphens with spaces and capitalize words
    name = sub(r'-', ' ', slug)
    return name

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'lecturer_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    faculties = Faculty.query.all()
    departments = Department.query.all()
    lecturers = Lecturer.query.all()
    return render_template('index.html', faculties=faculties, departments=departments, lecturers=lecturers)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nik = request.form['nik']
        password = request.form['password']

        lecturer = Lecturer.query.filter_by(nik=nik).first()
        if lecturer and check_password_hash(lecturer.password, password):
            session['lecturer_id'] = lecturer.id
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('lecturer_id', None)
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    lecturer = Lecturer.query.get(session['lecturer_id'])
    return render_template('dashboard.html', lecturer=lecturer)

@app.route('/schedule/<string:lecturer_slug>')
def lecturer_schedule(lecturer_slug):
    """
    Find lecturer by their URL slug.
    Try multiple matching approaches to handle edge cases.
    """
    # First try: Direct name match after deslugify
    lecturer = Lecturer.query.filter(
        Lecturer.name.ilike(lecturer_slug.replace('-', ' '))
    ).first()

    if not lecturer:
        # Second try: Match by generated slug
        lecturers = Lecturer.query.all()
        for l in lecturers:
            if slugify(l.name) == lecturer_slug:
                lecturer = l
                break

    if not lecturer:
        abort(404)

    return render_template('schedule.html', lecturer=lecturer)

# API Routes
@app.route('/api/schedule', methods=['POST'])
@login_required
def add_schedule():
    data = request.json
    new_schedule = Schedule(
        course_name=data['course_name'],
        day=data['day'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        room=data['room'],
        lecturer_id=session['lecturer_id']
    )
    db.session.add(new_schedule)
    db.session.commit()
    socketio.emit('schedule_update', {'action': 'add', 'schedule': {
        'id': new_schedule.id,
        'course_name': new_schedule.course_name,
        'day': new_schedule.day,
        'start_time': new_schedule.start_time,
        'end_time': new_schedule.end_time,
        'room': new_schedule.room
    }})
    return jsonify({'message': 'Schedule added successfully'})

@app.route('/api/schedule/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def manage_schedule(id):
    schedule = Schedule.query.get_or_404(id)
    if schedule.lecturer_id != session['lecturer_id']:
        return jsonify({'error': 'Unauthorized'}), 403

    if request.method == 'PUT':
        data = request.json
        schedule.course_name = data['course_name']
        schedule.day = data['day']
        schedule.start_time = data['start_time']
        schedule.end_time = data['end_time']
        schedule.room = data['room']
        db.session.commit()
        socketio.emit('schedule_update', {'action': 'update', 'schedule': {
            'id': schedule.id,
            'course_name': schedule.course_name,
            'day': schedule.day,
            'start_time': schedule.start_time,
            'end_time': schedule.end_time,
            'room': schedule.room
        }})
        return jsonify({'message': 'Schedule updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(schedule)
        db.session.commit()
        socketio.emit('schedule_update', {'action': 'delete', 'schedule_id': id})
        return jsonify({'message': 'Schedule deleted successfully'})

@app.route('/api/search')
def search_lecturers():
    # Get search parameters
    query = request.args.get('q', '')
    faculty_id = request.args.get('faculty', '')
    department_id = request.args.get('department', '')
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Number of items per page

    # Build the query
    lecturers = Lecturer.query

    # Apply filters
    if query:
        lecturers = lecturers.filter(Lecturer.name.ilike(f'%{query}%'))
    if faculty_id:
        lecturers = lecturers.join(Department).filter(Department.faculty_id == faculty_id)
    if department_id:
        lecturers = lecturers.filter(Lecturer.department_id == department_id)

    # Get paginated results
    paginated_lecturers = lecturers.paginate(page=page, per_page=per_page, error_out=False)

    # Prepare response
    results = {
        'items': [],
        'total': paginated_lecturers.total,
        'pages': paginated_lecturers.pages,
        'current_page': page,
        'has_next': paginated_lecturers.has_next,
        'has_prev': paginated_lecturers.has_prev,
        'per_page': per_page
    }

    # Format lecturer data
    for lecturer in paginated_lecturers.items:
        results['items'].append({
            'id': lecturer.id,
            'name': lecturer.name,
            'slug': slugify(lecturer.name),
            'department': lecturer.department.name,
            'faculty': lecturer.department.faculty.name
        })

    return jsonify(results)

@app.route('/api/schedule/export/<string:format>')
@login_required
def export_schedule(format):
    lecturer = Lecturer.query.get(session['lecturer_id'])
    schedules = Schedule.query.filter_by(lecturer_id=lecturer.id).all()

    # Convert schedules to DataFrame
    data = []
    for schedule in schedules:
        data.append({
            'Mata Kuliah': schedule.course_name,
            'Hari': schedule.day,
            'Waktu Mulai': schedule.start_time,
            'Waktu Selesai': schedule.end_time,
            'Ruang': schedule.room
        })

    df = pd.DataFrame(data)

    # Create a BytesIO object to store the file
    buffer = BytesIO()

    # Export based on format
    if format == 'xlsx':
        df.to_excel(buffer, index=False, engine='openpyxl')
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        file_ext = 'xlsx'
    else:  # csv
        df.to_csv(buffer, index=False)
        mimetype = 'text/csv'
        file_ext = 'csv'

    buffer.seek(0)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return send_file(
        buffer,
        mimetype=mimetype,
        as_attachment=True,
        download_name=f'jadwal_kuliah_{timestamp}.{file_ext}'
    )

@app.route('/api/schedule/import', methods=['POST'])
@login_required
def import_schedule():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith(('.xlsx', '.csv')):
        return jsonify({'error': 'Invalid file format. Please upload XLSX or CSV file'}), 400

    try:
        # Create temporary file to store the upload
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file.save(tmp.name)

            # Read the file based on its extension
            if file.filename.endswith('.xlsx'):
                df = pd.read_excel(tmp.name)
            else:
                df = pd.read_csv(tmp.name)

        # Delete temporary file
        os.unlink(tmp.name)

        # Validate column names
        required_columns = {'Mata Kuliah', 'Hari', 'Waktu Mulai', 'Waktu Selesai', 'Ruang'}
        if not required_columns.issubset(df.columns):
            return jsonify({'error': 'Invalid file format. Missing required columns'}), 400

        # Import schedules
        success_count = 0
        error_count = 0

        for _, row in df.iterrows():
            try:
                new_schedule = Schedule(
                    course_name=row['Mata Kuliah'],
                    day=row['Hari'],
                    start_time=str(row['Waktu Mulai']),
                    end_time=str(row['Waktu Selesai']),
                    room=str(row['Ruang']),
                    lecturer_id=session['lecturer_id']
                )
                db.session.add(new_schedule)
                success_count += 1
            except Exception as e:
                error_count += 1
                continue

        db.session.commit()

        return jsonify({
            'message': f'Import completed. Successfully imported {success_count} schedules. {error_count} errors.',
            'success_count': success_count,
            'error_count': error_count
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.template_filter('slugify')
def slugify_filter(text):
    return slugify(text)

@app.route('/set-theme', methods=['POST'])
def set_theme():
    data = request.get_json()
    session['dark_mode'] = data.get('dark_mode', False)
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True, host="0.0.0.0")