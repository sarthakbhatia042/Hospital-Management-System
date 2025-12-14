#!/bin/bash

echo "🏥 HealFlow Hospital Management System - Quick Start Script"
echo "=========================================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if database exists
if [ ! -f "instance/hospital.db" ]; then
    echo "🗄️  Database not found. Seeding database..."
    python seed_data.py
else
    echo "✅ Database already exists"
fi

echo ""
echo "🚀 Starting HealFlow..."
echo ""
echo "📱 Access the application at:"
echo "   Local:   http://127.0.0.1:5000"
echo "   Network: http://$(ipconfig getifaddr en0 2>/dev/null || hostname -I | awk '{print $1}'):5000"
echo ""
echo "👤 Default login:"
echo "   Admin: admin / admin123"
echo "   Doctor: dr.smith / doctor123"
echo "   Patient: john.doe / patient123"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================================="
echo ""

python app.py
