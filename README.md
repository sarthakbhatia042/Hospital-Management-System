# HealFlow Hospital Management System 🏥

A comprehensive hospital management system built with Flask, featuring role-based dashboards for Admins, Doctors, and Patients. Designed with Indian healthcare context in mind, with localized names, addresses, and pricing in INR.

## Features

### Admin Dashboard
- View and manage doctors, patients, and appointments
- Department management
- Real-time statistics and analytics
- Search functionality

### Doctor Dashboard
- View upcoming appointments
- Manage patient records and treatment history
- Set availability schedule
- View assigned patients

### Patient Dashboard
- Book appointments with doctors
- View medical history
- Browse departments
- Health checkup packages
- Lab test booking

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download
```bash
cd HealFlow
```

### Step 2: Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Seed the Database (Optional but Recommended)
```bash
python seed_data.py
```

This will create:
- 8 Departments (Cardiology, Orthopedics, Pediatrics, Neurology, Dermatology, Oncology, Gynecology, Ophthalmology)
- 10 Doctors with names and credentials
- 12 Patients with names and addresses across major cities
- Sample appointments with realistic consultation fees in INR (₹1,000 - ₹2,000)

### Step 5: Run the Application
```bash
python app.py
```

The application will be available at:
- **Local**: http://127.0.0.1:5000
- **Network**: http://[YOUR_IP]:5000 (accessible from other devices on the same network)

## Default Login Credentials

### Admin
- **Username**: `admin`
- **Password**: `admin123`

### Doctors (Password: `doctor123` for all)
- **dr.sharma** - Dr. Raghav Sharma (Cardiology) - ₹1,500
- **dr.verma** - Dr. Priya Verma (Orthopedics) - ₹1,200
- **dr.gupta** - Dr. Ananya Gupta (Pediatrics) - ₹1,000
- **dr.singh** - Dr. Manav Singh (Neurology) - ₹1,800
- **dr.reddy** - Dr. Kavya Reddy (Dermatology) - ₹1,100
- **dr.patel** - Dr. Sarthak Patel (Oncology) - ₹2,000
- **dr.nair** - Dr. Meera Nair (Gynecology) - ₹1,300
- **dr.kumar** - Dr. Keshav Kumar (Ophthalmology) - ₹1,150
- **dr.iyer** - Dr. Aditi Iyer (Cardiology) - ₹1,400
- **dr.mehta** - Dr. Priyanshu Mehta (Orthopedics) - ₹1,250

### Patients (Password: `patient123` for all)
- **parth.joshi** - Parth Joshi (Mumbai, Maharashtra)
- **sneha.desai** - Sneha Desai (Kolkata, West Bengal)
- **dev.malhotra** - Dev Malhotra (Chennai, Tamil Nadu)
- **isha.kapoor** - Isha Kapoor (Delhi)
- **deep.agarwal** - Deep Agarwal (Bangalore, Karnataka)
- **riya.shah** - Riya Shah (Ahmedabad, Gujarat)
- **tanmaya.rao** - Tanmaya Rao (Hyderabad, Telangana)
- **ananya.bose** - Ananya Bose (Pune, Maharashtra)
- **abhishek.jain** - Abhishek Jain (Jaipur, Rajasthan)
- **diya.menon** - Diya Menon (Kochi, Kerala)
- **yatharth.bajaj** - Yatharth Bajaj (Chandigarh)
- **aayushi.chopra** - Aayushi Chopra (Lucknow, UP)

## Accessing from Other Devices

### On the Same Network (LAN)
1. Find your computer's IP address:
   - **macOS/Linux**: `ifconfig` or `ip addr`
   - **Windows**: `ipconfig`
2. Start the app: `python app.py`
3. On another device, open browser and go to: `http://[YOUR_IP]:5000`

Example: `http://192.168.1.100:5000`

### From the Internet (Production Deployment)

For production deployment, consider these options:

#### Option 1: Cloud Platforms
- **Heroku**: Free tier available
- **PythonAnywhere**: Free tier with Python support
- **Railway**: Modern deployment platform
- **Render**: Free tier available

#### Option 2: VPS (Virtual Private Server)
- DigitalOcean
- AWS EC2
- Google Cloud Platform
- Azure

#### Option 3: Using ngrok (Quick Testing)
```bash
# Install ngrok from https://ngrok.com
ngrok http 5000
```
This creates a public URL that anyone can access.

## Mobile Access

The application is **fully responsive** and works on:
- 📱 Smartphones (iOS & Android)
- 💻 Tablets
- 🖥️ Desktop computers
- Any device with a web browser

## Project Structure

```
HealFlow/
├── app.py                 # Main application file
├── models.py              # Database models
├── forms.py               # WTForms definitions
├── seed_data.py           # Database seeding script
├── requirements.txt       # Python dependencies
├── instance/
│   └── hospital.db       # SQLite database
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── images/
│       └── bg.png        # Background watermark
└── templates/
    ├── base.html         # Base template
    ├── login.html
    ├── register.html
    ├── admin/            # Admin templates
    ├── doctor/           # Doctor templates
    └── patient/          # Patient templates
```

## Security Notes

⚠️ **Important for Production**:
1. Change `SECRET_KEY` in `app.py` to a strong random value
2. Set `debug=False` in production
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Use PostgreSQL or MySQL instead of SQLite
5. Enable HTTPS
6. Change default passwords

## Troubleshooting

### Port 5000 already in use
```bash
# Find the process using port 5000
lsof -i :5000

# Kill the process (replace PID)
kill -9 <PID>
```

### Email validation error
```bash
pip install email-validator
```

### Database errors
```bash
# Reset the database
rm instance/hospital.db
python seed_data.py
```
