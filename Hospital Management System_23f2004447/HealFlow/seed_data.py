from app import app
from models import db, User, Department, Doctor, Patient, DoctorAvailability, Appointment, Treatment
from datetime import date, time, timedelta, datetime

def seed_database():
    with app.app_context():
        print("Starting database seeding...")
        
        db.create_all()
        print("✓ Database tables created")
        
        departments_data = [
            {'name': 'Cardiology', 'description': 'Heart and cardiovascular system specialists'},
            {'name': 'Orthopedics', 'description': 'Bone, joint, and muscle specialists'},
            {'name': 'Pediatrics', 'description': 'Children healthcare specialists'},
            {'name': 'Neurology', 'description': 'Brain and nervous system specialists'},
            {'name': 'Dermatology', 'description': 'Skin, hair, and nail specialists'},
            {'name': 'Oncology', 'description': 'Cancer treatment and care specialists'},
            {'name': 'Gynecology', 'description': 'Women\'s health specialists'},
            {'name': 'Ophthalmology', 'description': 'Eye care specialists'}
        ]
        
        dept_creation_date = datetime(2010, 11, 10)  
        departments = []
        for dept_data in departments_data:
            dept = Department(**dept_data)
            dept.created_at = dept_creation_date
            departments.append(dept)
            db.session.add(dept)
        
        db.session.commit()
        print(f"✓ {len(departments)} Departments created")
        
        doctors_data = [
            {'username': 'dr.sharma', 'email': 'sharma@healflow.com', 'full_name': 'Dr. Raghav Sharma', 'dept_idx': 0, 'qualification': 'MD, FACC - Cardiology', 'experience': 15, 'fee': 1500, 'phone': '555-0101'},
            {'username': 'dr.verma', 'email': 'verma@healflow.com', 'full_name': 'Dr. Priya Verma', 'dept_idx': 1, 'qualification': 'MD, FAAOS - Orthopedics', 'experience': 10, 'fee': 1200, 'phone': '555-0102'},
            {'username': 'dr.gupta', 'email': 'gupta@healflow.com', 'full_name': 'Dr. Ananya Gupta', 'dept_idx': 2, 'qualification': 'MD, FAAP - Pediatrics', 'experience': 8, 'fee': 1000, 'phone': '555-0103'},
            {'username': 'dr.singh', 'email': 'singh@healflow.com', 'full_name': 'Dr. Manav Singh', 'dept_idx': 3, 'qualification': 'MD, PhD - Neurology', 'experience': 12, 'fee': 1800, 'phone': '555-0104'},
            {'username': 'dr.reddy', 'email': 'reddy@healflow.com', 'full_name': 'Dr. Kavya Reddy', 'dept_idx': 4, 'qualification': 'MD - Dermatology', 'experience': 7, 'fee': 1100, 'phone': '555-0105'},
            {'username': 'dr.patel', 'email': 'patel@healflow.com', 'full_name': 'Dr. Sarthak Patel', 'dept_idx': 5, 'qualification': 'MD, Oncologist', 'experience': 18, 'fee': 2000, 'phone': '555-0106'},
            {'username': 'dr.nair', 'email': 'nair@healflow.com', 'full_name': 'Dr. Meera Nair', 'dept_idx': 6, 'qualification': 'MD, FACOG - Gynecology', 'experience': 11, 'fee': 1300, 'phone': '555-0107'},
            {'username': 'dr.kumar', 'email': 'kumar@healflow.com', 'full_name': 'Dr. Keshav Kumar', 'dept_idx': 7, 'qualification': 'MD - Ophthalmology', 'experience': 9, 'fee': 1150, 'phone': '555-0108'},
            {'username': 'dr.iyer', 'email': 'iyer@healflow.com', 'full_name': 'Dr. Aditi Iyer', 'dept_idx': 0, 'qualification': 'MD - Cardiology', 'experience': 6, 'fee': 1400, 'phone': '555-0109'},
            {'username': 'dr.mehta', 'email': 'mehta@healflow.com', 'full_name': 'Dr. Priyanshu Mehta', 'dept_idx': 1, 'qualification': 'MD - Orthopedics', 'experience': 13, 'fee': 1250, 'phone': '555-0110'},
        ]
        
        doctors = []
        for doc_data in doctors_data:
            user = User(username=doc_data['username'], email=doc_data['email'], role='doctor')
            user.set_password('doctor123')
            db.session.add(user)
            db.session.flush()
            
            doctor = Doctor(
                user_id=user.id,
                full_name=doc_data['full_name'],
                department_id=departments[doc_data['dept_idx']].id,
                phone=doc_data['phone'],
                qualification=doc_data['qualification'],
                experience_years=doc_data['experience'],
                consultation_fee=doc_data['fee']
            )
            doctors.append(doctor)
            db.session.add(doctor)
        
        db.session.commit()
        print(f"✓ {len(doctors)} Doctors created")
        
        #Doctor's Availability
        today = date.today()
        for doctor in doctors:
            for day_offset in range(7):
                availability_date = today + timedelta(days=day_offset)
                availability = DoctorAvailability(
                    doctor_id=doctor.id,
                    date=availability_date,
                    start_time=time(9, 0),
                    end_time=time(17, 0),
                    is_available=True
                )
                db.session.add(availability)
        
        db.session.commit()
        print("✓ Doctor availability created (7 days)")
        
        # Patients
        patients_data = [
            {'username': 'parth.joshi', 'email': 'parth@gmail.com', 'full_name': 'Parth Joshi', 'phone': '555-1001', 'dob': date(1990, 5, 15), 'gender': 'Male', 'address': '123 MG Road, Mumbai, Maharashtra', 'blood': 'A+'},
            {'username': 'sneha.desai', 'email': 'sneha@yahoo.com', 'full_name': 'Sneha Desai', 'phone': '555-1002', 'dob': date(1985, 8, 20), 'gender': 'Female', 'address': '456 Park Street, Kolkata, West Bengal', 'blood': 'O+'},
            {'username': 'dev.malhotra', 'email': 'dev@gmail.com', 'full_name': 'Dev Malhotra', 'phone': '555-1003', 'dob': date(1992, 3, 10), 'gender': 'Male', 'address': '789 Anna Salai, Chennai, Tamil Nadu', 'blood': 'B+'},
            {'username': 'isha.kapoor', 'email': 'isha@gmail.com', 'full_name': 'Isha Kapoor', 'phone': '555-1004', 'dob': date(1988, 11, 5), 'gender': 'Female', 'address': '321 Connaught Place, Delhi', 'blood': 'AB+'},
            {'username': 'deep.agarwal', 'email': 'deep@yahoo.com', 'full_name': 'Deep Agarwal', 'phone': '555-1005', 'dob': date(1995, 7, 22), 'gender': 'Male', 'address': '654 MG Road, Bangalore, Karnataka', 'blood': 'A-'},
            {'username': 'riya.shah', 'email': 'riya@yahoo.com', 'full_name': 'Riya Shah', 'phone': '555-1006', 'dob': date(1991, 2, 18), 'gender': 'Female', 'address': '987 SG Highway, Ahmedabad, Gujarat', 'blood': 'O-'},
            {'username': 'tanmaya.rao', 'email': 'tanmaya@gmail.com', 'full_name': 'Tanmaya Rao', 'phone': '555-1007', 'dob': date(1987, 9, 30), 'gender': 'Male', 'address': '159 Banjara Hills, Hyderabad, Telangana', 'blood': 'B-'},
            {'username': 'ananya.bose', 'email': 'ananya@yahoo.com', 'full_name': 'Ananya Bose', 'phone': '555-1008', 'dob': date(1993, 4, 25), 'gender': 'Female', 'address': '753 Park Avenue, Pune, Maharashtra', 'blood': 'AB-'},
            {'username': 'abhishek.jain', 'email': 'abhishek@gmail.com', 'full_name': 'Abhishek Jain', 'phone': '555-1009', 'dob': date(1989, 12, 8), 'gender': 'Male', 'address': '852 MG Road, Jaipur, Rajasthan', 'blood': 'A+'},
            {'username': 'diya.menon', 'email': 'diya@yahoo.com', 'full_name': 'Diya Menon', 'phone': '555-1010', 'dob': date(1994, 6, 14), 'gender': 'Female', 'address': '951 Marine Drive, Kochi, Kerala', 'blood': 'O+'},
            {'username': 'yatharth.bajaj', 'email': 'yatharth@yahoo.com', 'full_name': 'Yatharth Bajaj', 'phone': '555-1011', 'dob': date(1986, 1, 28), 'gender': 'Male', 'address': '147 Elgin Road, Chandigarh', 'blood': 'B+'},
            {'username': 'aayushi.chopra', 'email': 'aayushi@gmail.com', 'full_name': 'Aayushi Chopra', 'phone': '555-1012', 'dob': date(1996, 10, 17), 'gender': 'Female', 'address': '258 Residency Road, Lucknow, UP', 'blood': 'AB+'},
        ]
        
        patients = []
        for pat_data in patients_data:
            user = User(username=pat_data['username'], email=pat_data['email'], role='patient')
            user.set_password('patient123')
            db.session.add(user)
            db.session.flush()
            
            patient = Patient(
                user_id=user.id,
                full_name=pat_data['full_name'],
                phone=pat_data['phone'],
                date_of_birth=pat_data['dob'],
                gender=pat_data['gender'],
                address=pat_data['address'],
                blood_group=pat_data['blood']
            )
            patients.append(patient)
            db.session.add(patient)
        
        db.session.commit()
        print(f"✓ {len(patients)} Patients created")
        
        appointments_data = [
            {'patient_idx': 0, 'doctor_idx': 0, 'days': 2, 'time': time(10, 0), 'reason': 'Chest pain and irregular heartbeat', 'status': 'Booked'},
            {'patient_idx': 1, 'doctor_idx': 1, 'days': 3, 'time': time(14, 0), 'reason': 'Knee pain after exercise', 'status': 'Booked'},
            {'patient_idx': 2, 'doctor_idx': 3, 'days': 1, 'time': time(11, 30), 'reason': 'Severe headaches', 'status': 'Booked'},
            {'patient_idx': 3, 'doctor_idx': 6, 'days': 4, 'time': time(9, 30), 'reason': 'Routine gynecological checkup', 'status': 'Booked'},
            {'patient_idx': 4, 'doctor_idx': 2, 'days': 5, 'time': time(15, 0), 'reason': 'Child vaccination', 'status': 'Booked'},
            {'patient_idx': 5, 'doctor_idx': 4, 'days': 2, 'time': time(13, 0), 'reason': 'Skin rash and irritation', 'status': 'Booked'},
            {'patient_idx': 6, 'doctor_idx': 7, 'days': 3, 'time': time(10, 30), 'reason': 'Eye checkup', 'status': 'Booked'},
            
            #previous
            {'patient_idx': 0, 'doctor_idx': 0, 'days': -10, 'time': time(10, 0), 'reason': 'Annual heart checkup', 'status': 'Completed'},
            {'patient_idx': 1, 'doctor_idx': 1, 'days': -15, 'time': time(14, 0), 'reason': 'Back pain consultation', 'status': 'Completed'},
            {'patient_idx': 7, 'doctor_idx': 5, 'days': -5, 'time': time(11, 0), 'reason': 'Cancer screening', 'status': 'Completed'},
            {'patient_idx': 8, 'doctor_idx': 8, 'days': -8, 'time': time(16, 0), 'reason': 'Heart palpitations', 'status': 'Completed'},
            
            # Cancelled
            {'patient_idx': 9, 'doctor_idx': 9, 'days': -3, 'time': time(12, 0), 'reason': 'Joint pain', 'status': 'Cancelled'},
        ]
        
        for apt_data in appointments_data:
            appointment = Appointment(
                patient_id=patients[apt_data['patient_idx']].id,
                doctor_id=doctors[apt_data['doctor_idx']].id,
                appointment_date=today + timedelta(days=apt_data['days']),
                appointment_time=apt_data['time'],
                reason=apt_data['reason'],
                status=apt_data['status']
            )
            db.session.add(appointment)
            
            if apt_data['status'] == 'Completed':
                db.session.flush()
                treatment = Treatment(
                    appointment_id=appointment.id,
                    diagnosis='Patient examined and diagnosed',
                    prescription='Prescribed medication as needed',
                    notes='Follow-up recommended in 3 months'
                )
                db.session.add(treatment)
        
        db.session.commit()
        print(f"✓ {len(appointments_data)} Sample appointments created")
        
        print("\n" + "="*60)
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nLogin Credentials:")
        print("\nAdmin:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nDoctors (Password: doctor123 for all):")
        for doc in doctors_data[:5]:
            print(f"  • {doc['username']} ({doc['full_name']})")
        print(f"  ... and {len(doctors_data) - 5} more doctors")
        print("\nPatients (Password: patient123 for all):")
        for pat in patients_data[:5]:
            print(f"  • {pat['username']} ({pat['full_name']})")
        print(f"  ... and {len(patients_data) - 5} more patients")
        print("="*60)

if __name__ == '__main__':
    seed_database()
