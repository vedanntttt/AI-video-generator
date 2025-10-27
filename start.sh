#!/bin/bash

# AI Video Generator Startup Script
echo "🎬 Starting AI Video Generator..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📋 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
python -c "import utils; utils.create_directories()"

# Start the application
echo "🚀 Starting Streamlit application..."
echo "📱 Open your browser and go to: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the application"
echo ""

streamlit run app.py --server.port 8501 --server.address 0.0.0.0