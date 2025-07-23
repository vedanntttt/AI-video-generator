# 🛠️ Setup Guide - AI Animated Video Generator

This guide will help you set up the AI Animated Video Generator on your system.

## Prerequisites

- **Python 3.8 or higher**
- **FFmpeg** (for video processing)
- **Internet connection** (for AI services)

## Step-by-Step Installation

### 1. Check Python Version

```bash
python --version
# Should show Python 3.8 or higher
```

### 2. Install FFmpeg

FFmpeg is required for video processing. Choose your operating system:

#### Windows
```bash
# Option 1: Using Chocolatey (recommended)
choco install ffmpeg

# Option 2: Manual installation
# Download from https://ffmpeg.org/download.html
# Extract and add to PATH
```

#### macOS
```bash
# Using Homebrew
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### 3. Install Python Dependencies

```bash
# Navigate to project directory
cd ai-video-generator

# Install requirements
pip install -r requirements.txt
```

### 4. Test Installation

```bash
# Run the installation test
python test_installation.py
```

This will check:
- ✅ All Python packages are installed
- ✅ Directories can be created
- ✅ Modules can be initialized
- ✅ FFmpeg is available

### 5. Run Demo (Optional)

```bash
# Test with a simple 2-scene demo
python demo.py
```

This creates a short demo video to verify everything works.

### 6. Configure API Keys (Optional)

For better voice quality, you can add an ElevenLabs API key:

```bash
# Copy the environment template
cp .env.example .env

# Edit .env file and add your API key
ELEVENLABS_API_KEY=your_api_key_here
```

**Get ElevenLabs API Key:**
1. Go to https://elevenlabs.io/
2. Sign up for free account
3. Get API key from your profile
4. Free tier: 10,000 characters/month

### 7. Launch the App

```bash
# Start the Streamlit app
streamlit run app.py

# Or use the convenience scripts:
# Windows: run.bat
# Linux/Mac: ./run.sh
```

The app will open in your browser at `http://localhost:8501`

## Troubleshooting

### Common Issues

#### "FFmpeg not found"
- **Solution**: Install FFmpeg and ensure it's in your system PATH
- **Test**: Run `ffmpeg -version` in terminal

#### "Module not found" errors
- **Solution**: Reinstall requirements
```bash
pip install --upgrade -r requirements.txt
```

#### "Permission denied" on Linux/Mac
- **Solution**: Make run script executable
```bash
chmod +x run.sh
```

#### ElevenLabs API errors
- **Solution**: Check your API key and character limits
- **Alternative**: Use Edge TTS (no API key required)

#### Slow video generation
- **Cause**: Normal for first run (downloading models)
- **Solution**: Subsequent runs will be faster

#### "No module named 'modules'"
- **Solution**: Run from the project root directory
```bash
cd ai-video-generator
python app.py  # or streamlit run app.py
```

### Performance Tips

1. **First Run**: May be slow due to model downloads
2. **Image Generation**: Manual Bing Creator gives best results
3. **Voice Quality**: ElevenLabs > Edge TTS (but uses API quota)
4. **Video Length**: Longer scripts take more time to process

### System Requirements

**Minimum:**
- 4GB RAM
- 2GB free disk space
- Internet connection

**Recommended:**
- 8GB RAM
- 5GB free disk space
- Fast internet connection

## Getting Help

### Check Status
- Use the Streamlit sidebar for real-time status
- Monitor the console for detailed logs

### Reset Everything
```bash
# Clear all temporary files
python -c "import utils; utils.cleanup_temp_files()"

# Or use the app's "Clear Temp Files" button
```

### Logs and Debugging
- Check the terminal/console for error messages
- Temporary files are stored in the `temp/` directory
- Final videos are saved in the `output/` directory

### Support Resources
- **FFmpeg Issues**: https://ffmpeg.org/documentation.html
- **Streamlit Issues**: https://docs.streamlit.io/
- **ElevenLabs API**: https://docs.elevenlabs.io/

## Next Steps

Once everything is working:

1. **Try the example scripts** in the app
2. **Write your own stories** (keep lines descriptive)
3. **Experiment with different voices** and settings
4. **Use manual image generation** for best visual results
5. **Share your creations** with friends and family!

Happy video creating! 🎬✨
