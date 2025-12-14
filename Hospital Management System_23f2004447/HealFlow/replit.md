# Hospital Management System

## Overview
A comprehensive web-based Hospital Management System built with Flask, SQLite, and Bootstrap that manages patients, doctors, appointments, and treatments across three user roles: Admin, Doctor, and Patient.

## Project Status
**Current Version:** 1.0  
**Last Updated:** November 7, 2025  
**Status:** Fully functional with all core features implemented

## Tech Stack
- **Backend:** Flask 3.1.2, Python 3.11
- **Database:** SQLite (programmatically created)
- **ORM:** Flask-SQLAlchemy 3.1.1
- **Authentication:** Flask-Login 0.6.3
- **Forms:** Flask-WTF 1.2.2, WTForms
- **Frontend:** Jinja2, Bootstrap 5.3, HTML5, CSS3
- **Validation:** Email-validator, HTML5 validation

## Key Features

### Admin Features
- Pre-existing admin account (username: admin, password: admin123)
- Dashboard with statistics (total doctors, patients, appointments)
- Department management (add departments/specializations)
- Doctor management (add, edit, delete doctors)
- Patient management (search, view, delete patients)
- View all appointments with filtering
- Search functionality for doctors by name/specialization
- Search functionality for patients by name/ID/contact

### Doctor Features
- Dashboard showing upcoming appointments for the week
- View assigned patients list
- Mark appointments as Completed or Cancelled
- Add availability for the next 7 days
- Enter treatment details (diagnosis, prescription, notes)
- View patient history with previous diagnoses

### Patient Features
- Self-registration and login system
- Dashboard showing available departments and doctors
- Search doctors by specialization and name
- View doctor profiles with availability for 7 days
- Book appointments with conflict prevention (no double-booking)
- Cancel appointments
- View appointment history with status
- View medical history with diagnosis and prescriptions
- Edit profile information

## Database Schema

### Tables
1. **users** - User authentication and role management
2. **departments** - Medical specializations/departments
3. **doctors** - Doctor profiles and information
4. **patients** - Patient profiles and information
5. **doctor_availability** - Doctor availability slots
6. **appointments** - Appointment bookings and status
7. **treatments** - Treatment records with diagnosis/prescriptions

## Project Structure
```
.
├── app.py                          # Main Flask application with all routes
├── models.py                       # SQLAlchemy database models
├── forms.py                        # Flask-WTF forms for validation
├── hospital.db                     # SQLite database (auto-created)
├── templates/
│   ├── base.html                   # Base template with navigation
│   ├── login.html                  # Login page
│   ├── register.html               # Patient registration
│   ├── admin/                      # Admin templates
│   │   ├── dashboard.html
│   │   ├── departments.html
│   │   ├── add_department.html
│   │   ├── doctors.html
│   │   ├── add_doctor.html
│   │   ├── edit_doctor.html
│   │   ├── patients.html
│   │   └── appointments.html
│   ├── doctor/                     # Doctor templates
│   │   ├── dashboard.html
│   │   ├── appointments.html
│   │   ├── complete_appointment.html
│   │   ├── patient_history.html
│   │   └── availability.html
│   └── patient/                    # Patient templates
│       ├── dashboard.html
│       ├── profile.html
│       ├── doctors.html
│       ├── book_appointment.html
│       ├── appointments.html
│       └── history.html
└── static/
    └── css/
        └── style.css               # Custom CSS styling
```

## Default Credentials
- **Admin:**
  - Username: `admin`
  - Password: `admin123`
  <!-- - Note: For security, credentials are NOT logged to console. Change password after first login. -->

- **Sample Doctors** (run `python seed_data.py` to create):
  - Username: `dr.smith`, `dr.johnson`, `dr.williams`
  - Password: `doctor123`

- **Sample Patients** (run `python seed_data.py` to create):
  - Username: `john.doe`, `jane.smith`
  - Password: `patient123`

## Running the Application
The application runs automatically on port 5000. Access it through the webview.

## Core Functionality Implemented

✅ Role-based authentication (Admin, Doctor, Patient)  
✅ Admin dashboard with statistics  
✅ Department/specialization management  
✅ Doctor CRUD operations  
✅ Patient CRUD operations  
✅ Search functionality for doctors and patients  
✅ Doctor availability management (7-day window)  
✅ Appointment booking with conflict prevention  
✅ Appointment status updates (Booked → Completed/Cancelled)  
✅ Treatment entry with diagnosis and prescriptions  
✅ Patient medical history tracking  
✅ Responsive Bootstrap UI  
✅ Form validation (frontend HTML5 + backend WTForms)  
✅ SQLite database created programmatically  

## Security Features
- Password hashing using Werkzeug
- Flask-Login session management
- Role-based access control decorators
- CSRF protection via Flask-WTF
- Input validation and sanitization

## Notes
- Database is automatically created on first run
- Admin account is created programmatically at startup
- All forms include both frontend (HTML5) and backend validation
- Appointment conflict prevention ensures no double-booking
- Patient medical history is viewable by both patients and their doctors
