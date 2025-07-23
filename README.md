# 🎬 AI Animated Video Generator from Script

Transform your text scripts into animated videos with AI-generated images and voices!

## Features

- **Multi-line Script Processing**: Each line becomes a scene with image + voice
- **AI Voice Generation**: ElevenLabs API (primary) + Edge TTS (fallback)
- **Image Generation**: Bing Image Creator integration with manual/automated options
- **Video Creation**: Combines images and audio into professional video scenes
- **Easy-to-Use Interface**: Streamlit web app with progress tracking
- **Free Tier Friendly**: Uses free APIs and services

## Quick Start

### 1. Installation

```bash
# Clone or download the project
cd ai-video-generator

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration (Optional)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your ElevenLabs API key (optional)
# Get free API key from: https://elevenlabs.io/
ELEVENLABS_API_KEY=your_api_key_here
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Basic Workflow

1. **Enter Your Script**: Write your story, one line per scene
   ```
   Once upon a time in a magical forest, there lived a brave knight.
   The knight discovered a mysterious glowing treasure chest.
   Inside the chest was a magical sword that could grant wishes.
   ```

2. **Configure Settings**: 
   - Add ElevenLabs API key (optional, for better voice quality)
   - Choose voice provider (Auto or Edge TTS only)
   - Set minimum scene duration

3. **Generate Video**: Click "Generate Video" and wait for processing

4. **Download**: Preview and download your completed video

### Image Generation Options

The app supports multiple approaches for image generation:

1. **Automated Placeholder**: Creates text-based placeholder images
2. **Manual Bing Creator**: Provides prompts for manual image generation
3. **File Upload**: Upload your own images for each scene

### Voice Generation

- **ElevenLabs** (Primary): High-quality AI voices (10,000 free characters/month)
- **Edge TTS** (Fallback): Free Microsoft text-to-speech service

## Project Structure

```
ai-video-generator/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── modules/
│   ├── tts_module.py     # Text-to-speech functionality
│   ├── image_module.py   # Image generation handling
│   └── video_module.py   # Video creation and editing
├── temp/                 # Temporary files (auto-created)
│   ├── images/          # Generated/uploaded images
│   ├── audio/           # Generated audio files
│   └── scenes/          # Individual scene videos
└── output/              # Final video outputs
```

## Requirements

- Python 3.8+
- FFmpeg (for video processing)
- Internet connection (for AI services)

### Installing FFmpeg

**Windows:**
```bash
# Using chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## API Keys and Limits

### ElevenLabs (Optional)
- **Free Tier**: 10,000 characters/month
- **Sign up**: https://elevenlabs.io/
- **Usage**: High-quality AI voices

### Edge TTS (Default)
- **Free**: Unlimited usage
- **Quality**: Good quality, multiple voices
- **No API key required**

## Tips for Best Results

1. **Script Writing**:
   - Keep lines concise and descriptive
   - Each line should describe a clear scene
   - Aim for 10-20 words per line for optimal pacing

2. **Image Generation**:
   - Use descriptive, visual language
   - Include style keywords (animated, cartoon, colorful)
   - For manual generation, use Bing Image Creator with provided prompts

3. **Voice Settings**:
   - Start with Edge TTS (free and reliable)
   - Use ElevenLabs for higher quality when available
   - Monitor character usage in the sidebar

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Install FFmpeg and ensure it's in your PATH
2. **ElevenLabs API errors**: Check your API key and character limits
3. **Video generation fails**: Ensure all image and audio files are present
4. **Slow processing**: Processing time depends on script length and system performance

### Getting Help

- Check the Streamlit sidebar for real-time status updates
- Use the "Clear Temp Files" button to reset if needed
- Ensure all dependencies are properly installed

## License

This project is for educational and personal use. Please respect the terms of service of all integrated APIs and services.
