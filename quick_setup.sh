#!/bin/bash

echo "🎬 AI Video Generator - Quick Setup"
echo "=================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found. Installing..."
    
    # Try to install FFmpeg based on the system
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y ffmpeg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "❌ Please install Homebrew first: https://brew.sh/"
            exit 1
        fi
    else
        echo "❌ Please install FFmpeg manually: https://ffmpeg.org/download.html"
        exit 1
    fi
else
    echo "✅ FFmpeg found: $(ffmpeg -version | head -1)"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📋 Installing Python packages..."
pip install streamlit moviepy requests edge-tts elevenlabs Pillow numpy python-dotenv ffmpeg-python setuptools

# Create basic requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    cat > requirements.txt << EOF
streamlit>=1.28.0
moviepy>=1.0.3
requests>=2.31.0
edge-tts>=6.1.0
elevenlabs>=0.2.0
Pillow>=10.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
ffmpeg-python>=0.2.0
setuptools>=80.0.0
EOF
fi

# Create .env.example if it doesn't exist
if [ ! -f ".env.example" ]; then
    cat > .env.example << EOF
# ElevenLabs API Key (Optional - for premium voice generation)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# OpenAI API Key (Optional - for future features)
OPENAI_API_KEY=your_openai_api_key_here
EOF
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "To start the AI Video Generator:"
echo "1. Make sure all project files are in this directory"
echo "2. Run: source venv/bin/activate"
echo "3. Run: streamlit run app.py"
echo "4. Open: http://localhost:8501"
echo ""
echo "📁 Required files in this directory:"
echo "   - app.py (main application)"
echo "   - config.py (configuration)"
echo "   - utils.py (utilities)"
echo "   - demo_scripts.py (demo scripts)"
echo "   - modules/ (folder with TTS, image, video modules)"
echo ""
echo "🚀 Ready to create AI videos!"