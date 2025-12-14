from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Doctor, Patient, Department, Appointment, Treatment, DoctorAvailability, LabBooking
from forms import (LoginForm, PatientRegistrationForm, PatientProfileForm, 
                   DoctorForm, DepartmentForm, AppointmentForm, TreatmentForm, DoctorAvailabilityForm)
from datetime import datetime, date, timedelta, time
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-please-change')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'doctor':
            flash('Access denied. Doctor privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def patient_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'patient':
            flash('Access denied. Patient privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif current_user.role == 'patient':
            return redirect(url_for('patient_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        current_hospital_user = User.query.filter_by(username=form.username.data).first()
        if current_hospital_user and current_hospital_user.check_password(form.password.data) and current_hospital_user.active:
            login_user(current_hospital_user)
            flash(f'Welcome back, {current_hospital_user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password, or account is deactivated.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Username or email already exists. Please choose different credentials.', 'danger')
            return render_template('register.html', form=form)
        
        user = User(username=form.username.data, email=form.email.data, role='patient')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        
        patient = Patient(
            user_id=user.id,
            full_name=form.full_name.data,
            phone=form.phone.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            address=form.address.data,
            blood_group=form.blood_group.data
        )
        db.session.add(patient)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    upcoming_appointments = Appointment.query.filter(
        Appointment.appointment_date >= date.today(),
        Appointment.status == 'Booked'
    ).count()
    
    recent_consultations = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    medical_specialists = Doctor.query.limit(5).all()
    registered_patients = Patient.query.limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_doctors=total_doctors,
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         upcoming_appointments=upcoming_appointments,
                         recent_appointments=recent_consultations,
                         doctors=medical_specialists,
                         patients=registered_patients)

@app.route('/admin/departments')
@login_required
@admin_required
def admin_departments():
    departments = Department.query.all()
    return render_template('admin/departments.html', departments=departments)

@app.route('/admin/department/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        existing_dept = Department.query.filter_by(name=form.name.data).first()
        if existing_dept:
            flash('Department already exists.', 'danger')
            return render_template('admin/add_department.html', form=form)
        
        department = Department(name=form.name.data, description=form.description.data)
        db.session.add(department)
        db.session.commit()
        flash('Department added successfully!', 'success')
        return redirect(url_for('admin_departments'))
    
    return render_template('admin/add_department.html', form=form)

@app.route('/admin/doctors')
@login_required
@admin_required
def admin_doctors():
    search = request.args.get('search', '')
    if search:
        doctors = Doctor.query.filter(
            (Doctor.full_name.ilike(f'%{search}%')) |
            (Department.name.ilike(f'%{search}%'))
        ).join(Department).all()
    else:
        doctors = Doctor.query.all()
    
    return render_template('admin/doctors.html', doctors=doctors, search=search)

@app.route('/admin/doctor/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_doctor():
    form = DoctorForm()
    form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
    
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return render_template('admin/add_doctor.html', form=form)
        
        user = User(username=form.username.data, email=form.email.data, role='doctor')
        user.set_password(form.password.data if form.password.data else 'doctor123')
        db.session.add(user)
        db.session.flush()
        
        doctor = Doctor(
            user_id=user.id,
            full_name=form.full_name.data,
            department_id=form.department_id.data,
            phone=form.phone.data,
            qualification=form.qualification.data,
            experience_years=form.experience_years.data,
            consultation_fee=form.consultation_fee.data
        )
        db.session.add(doctor)
        db.session.commit()
        
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('admin_doctors'))
    
    return render_template('admin/add_doctor.html', form=form)

@app.route('/admin/doctor/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    form = DoctorForm(obj=doctor)
    form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
    
    if form.validate_on_submit():
        doctor.full_name = form.full_name.data
        doctor.department_id = form.department_id.data
        doctor.phone = form.phone.data
        doctor.qualification = form.qualification.data
        doctor.experience_years = form.experience_years.data
        doctor.consultation_fee = form.consultation_fee.data
        
        doctor.user.email = form.email.data
        if form.password.data:
            doctor.user.set_password(form.password.data)
        
        db.session.commit()
        flash('Doctor updated successfully!', 'success')
        return redirect(url_for('admin_doctors'))
    
    form.username.data = doctor.user.username
    form.email.data = doctor.user.email
    return render_template('admin/edit_doctor.html', form=form, doctor=doctor)

@app.route('/admin/doctor/delete/<int:doctor_id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    user = doctor.user
    db.session.delete(doctor)
    db.session.delete(user)
    db.session.commit()
    flash('Doctor deleted successfully!', 'success')
    return redirect(url_for('admin_doctors'))

@app.route('/admin/patients')
@login_required
@admin_required
def admin_patients():
    search = request.args.get('search', '')
    if search:
        patients = Patient.query.filter(
            (Patient.full_name.ilike(f'%{search}%')) |
            (Patient.phone.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        ).join(User).all()
    else:
        patients = Patient.query.all()
    
    return render_template('admin/patients.html', patients=patients, search=search)

@app.route('/admin/patient/delete/<int:patient_id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    user = patient.user
    db.session.delete(patient)
    db.session.delete(user)
    db.session.commit()
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('admin_patients'))

@app.route('/admin/appointments')
@login_required
@admin_required
def admin_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments)

@app.route('/doctor/dashboard')
@login_required
@doctor_required
def doctor_dashboard():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    today = date.today()
    next_week = today + timedelta(days=7)
    
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date >= today,
        Appointment.status == 'Booked'
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
    
    assigned_patients = db.session.query(Patient).join(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).distinct().all()
    
    patients_count = len(assigned_patients)
    
    availabilities = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor.id,
        DoctorAvailability.date >= today,
        DoctorAvailability.date <= next_week
    ).order_by(DoctorAvailability.date).all()
    
    return render_template('doctor/dashboard.html', 
                         doctor=doctor,
                         upcoming_appointments=upcoming_appointments,
                         assigned_patients=assigned_patients,
                         patients_count=patients_count,
                         availabilities=availabilities)

@app.route('/doctor/appointments')
@login_required
@doctor_required
def doctor_appointments():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(
        Appointment.appointment_date.desc(), Appointment.appointment_time.desc()
    ).all()
    return render_template('doctor/appointments.html', appointments=appointments)

@app.route('/doctor/appointment/<int:appointment_id>/complete', methods=['GET', 'POST'])
@login_required
@doctor_required
def doctor_complete_appointment(appointment_id):
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.doctor_id != doctor.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('doctor_appointments'))
    
    form = TreatmentForm()
    if form.validate_on_submit():
        treatment = Treatment(
            appointment_id=appointment.id,
            diagnosis=form.diagnosis.data,
            prescription=form.prescription.data,
            notes=form.notes.data
        )
        appointment.status = 'Completed'
        db.session.add(treatment)
        db.session.commit()
        flash('Appointment marked as completed and treatment recorded!', 'success')
        return redirect(url_for('doctor_appointments'))
    
    return render_template('doctor/complete_appointment.html', form=form, appointment=appointment)

@app.route('/doctor/appointment/<int:appointment_id>/cancel', methods=['POST'])
@login_required
@doctor_required
def doctor_cancel_appointment(appointment_id):
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.doctor_id != doctor.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('doctor_appointments'))
    
    appointment.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled successfully!', 'success')
    return redirect(url_for('doctor_appointments'))

@app.route('/doctor/patient/<int:patient_id>/history')
@login_required
@doctor_required
def doctor_patient_history(patient_id):
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    patient = Patient.query.get_or_404(patient_id)
    
    appointments = Appointment.query.filter_by(
        patient_id=patient_id,
        doctor_id=doctor.id,
        status='Completed'
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('doctor/patient_history.html', patient=patient, appointments=appointments)

@app.route('/doctor/availability', methods=['GET', 'POST'])
@login_required
@doctor_required
def doctor_availability():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    form = DoctorAvailabilityForm()
    
    if form.validate_on_submit():
        availability = DoctorAvailability(
            doctor_id=doctor.id,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
        db.session.add(availability)
        db.session.commit()
        flash('Availability added successfully!', 'success')
        return redirect(url_for('doctor_availability'))
    
    today = date.today()
    next_week = today + timedelta(days=7)
    availabilities = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor.id,
        DoctorAvailability.date >= today,
        DoctorAvailability.date <= next_week
    ).order_by(DoctorAvailability.date).all()
    
    return render_template('doctor/availability.html', form=form, availabilities=availabilities)

@app.route('/patient/dashboard')
@login_required
@patient_required
def patient_dashboard():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    departments = Department.query.all()
    
    today = date.today()
    next_week = today + timedelta(days=7)
    
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date >= today,
        Appointment.status == 'Booked'
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
    
    # Get history for dashboard
    history = Appointment.query.filter_by(
        patient_id=patient.id,
        status='Completed'
    ).order_by(Appointment.appointment_date.desc()).limit(5).all()
    
    doctors_available = Doctor.query.join(DoctorAvailability).filter(
        DoctorAvailability.date >= today,
        DoctorAvailability.date <= next_week
    ).distinct().all()

    # Mock Data for New Features
    health_packages = [
        {'name': 'Full Body Checkup', 'price': 2999, 'features': ['Blood Test', 'X-Ray', 'ECG', 'Consultation'], 'icon': 'bi-person-check'},
        {'name': 'Heart Health', 'price': 4999, 'features': ['Lipid Profile', 'ECG', 'Echo', 'Cardiologist Consult'], 'icon': 'bi-heart-pulse'},
        {'name': 'Diabetes Care', 'price': 1999, 'features': ['HbA1c', 'Sugar Fasting', 'Diet Plan', 'Diabetologist Consult'], 'icon': 'bi-droplet'}
    ]

    lab_tests = [
        {'name': 'CBC (Complete Blood Count)', 'price': 300},
        {'name': 'Thyroid Profile', 'price': 500},
        {'name': 'Vitamin D Test', 'price': 1000},
        {'name': 'Liver Function Test', 'price': 400}
    ]

    patient_stories = [
        {'name': 'Priya Sharma', 'condition': 'Cardiac Surgery', 'img': 'P', 'text': 'The care I received at HealFlow was exceptional. The doctors were attentive and the facilities were world-class.'},
        {'name': 'Rahul Verma', 'condition': 'Orthopedics', 'img': 'R', 'text': 'I recovered faster than expected thanks to the dedicated physiotherapy team. Highly recommended!'},
        {'name': 'Anjali Gupta', 'condition': 'Maternity', 'img': 'A', 'text': 'A wonderful experience bringing my baby into the world here. The nurses were angels.'}
    ]
    
    return render_template('patient/dashboard.html',
                         patient=patient,
                         departments=departments,
                         upcoming_appointments=upcoming_appointments,
                         history=history,
                         doctors_available=doctors_available,
                         health_packages=health_packages,
                         lab_tests=lab_tests,
                         patient_stories=patient_stories)

@app.route('/patient/profile', methods=['GET', 'POST'])
@login_required
@patient_required
def patient_profile():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    form = PatientProfileForm(obj=patient)
    
    if form.validate_on_submit():
        patient.full_name = form.full_name.data
        patient.phone = form.phone.data
        patient.date_of_birth = form.date_of_birth.data
        patient.gender = form.gender.data
        patient.address = form.address.data
        patient.blood_group = form.blood_group.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('patient_profile'))
    
    form.email.data = current_user.email
    return render_template('patient/profile.html', form=form, patient=patient)

@app.route('/patient/doctors')
@login_required
@patient_required
def patient_doctors():
    search = request.args.get('search', '')
    department_id = request.args.get('department', '')
    
    query = Doctor.query.join(Department)
    
    if search:
        query = query.filter(
            (Doctor.full_name.ilike(f'%{search}%')) |
            (Department.name.ilike(f'%{search}%'))
        )
    
    if department_id:
        query = query.filter(Doctor.department_id == int(department_id))
    
    doctors = query.all()
    departments = Department.query.all()
    
    today = date.today()
    next_week = today + timedelta(days=7)
    
    doctor_availability = {}
    for doctor in doctors:
        availabilities = DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == doctor.id,
            DoctorAvailability.date >= today,
            DoctorAvailability.date <= next_week,
            DoctorAvailability.is_available == True
        ).all()
        doctor_availability[doctor.id] = availabilities
    
    return render_template('patient/doctors.html',
                         doctors=doctors,
                         departments=departments,
                         doctor_availability=doctor_availability,
                         search=search)

@app.route('/patient/book-appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@patient_required
def patient_book_appointment(doctor_id):
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    doctor = Doctor.query.get_or_404(doctor_id)
    form = AppointmentForm()
    form.doctor_id.choices = [(doctor.id, doctor.full_name)]
    form.doctor_id.data = doctor.id
    
    if form.validate_on_submit():
        existing_appointment = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            status='Booked'
        ).first()
        
        if existing_appointment:
            flash('This time slot is already booked. Please choose a different time.', 'danger')
            return render_template('patient/book_appointment.html', form=form, doctor=doctor)
        
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            reason=form.reason.data,
            status='Booked'
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient_appointments'))
    
    today = date.today()
    next_week = today + timedelta(days=7)
    availabilities = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.date >= today,
        DoctorAvailability.date <= next_week
    ).all()
    
    return render_template('patient/book_appointment.html', form=form, doctor=doctor, availabilities=availabilities)

@app.route('/patient/appointments')
@login_required
@patient_required
def patient_appointments():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(
        Appointment.appointment_date.desc(), Appointment.appointment_time.desc()
    ).all()
    return render_template('patient/appointments.html', appointments=appointments)

@app.route('/patient/appointment/<int:appointment_id>/cancel', methods=['POST'])
@login_required
@patient_required
def patient_cancel_appointment(appointment_id):
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.patient_id != patient.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('patient_appointments'))
    
    appointment.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled successfully!', 'success')
    return redirect(url_for('patient_appointments'))

@app.route('/patient/history')
@login_required
@patient_required
def patient_history():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    completed_appointments = Appointment.query.filter_by(
        patient_id=patient.id,
        status='Completed'
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('patient/history.html', appointments=completed_appointments)

@app.template_filter('format_date')
def format_date(value):
    if value is None:
        return ''
    return value.strftime('%B %d, %Y')

@app.template_filter('format_time')
def format_time(value):
    if value is None:
        return ''
    return value.strftime('%I:%M %p')

@app.route('/patient/add-lab-test', methods=['POST'])
@login_required
@patient_required
def add_lab_test():
    test_name = request.form.get('test_name')
    price = request.form.get('price')
    
    if not test_name or not price:
        flash('Invalid test details.', 'danger')
        return redirect(url_for('patient_dashboard'))
    
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    booking = LabBooking(
        patient_id=patient.id,
        test_name=test_name,
        price=float(price)
    )
    
    db.session.add(booking)
    db.session.commit()
    
    flash(f'{test_name} added to your cart!', 'success')
    return redirect(url_for('patient_dashboard'))

@app.route('/patient/cart')
@login_required
@patient_required
def patient_cart():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    bookings = LabBooking.query.filter_by(patient_id=patient.id).order_by(LabBooking.booking_date.desc()).all()
    total_amount = sum(booking.price for booking in bookings)
    
    return render_template('patient/cart.html', bookings=bookings, total_amount=total_amount)

@app.route('/patient/remove-lab-test/<int:booking_id>', methods=['POST'])
@login_required
@patient_required
def remove_lab_test(booking_id):
    booking = LabBooking.query.get_or_404(booking_id)
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    if booking.patient_id != patient.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('patient_cart'))
    
    db.session.delete(booking)
    db.session.commit()
    
    flash('Item removed from cart.', 'success')
    return redirect(url_for('patient_cart'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@hospital.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
