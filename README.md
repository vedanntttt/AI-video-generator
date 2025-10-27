# 🎬 AI Animated Video Generator

Transform your text scripts into stunning animated videos with AI-generated images and natural-sounding voices! This powerful tool combines multiple AI technologies to create professional-quality animated videos from simple text descriptions.

## ✨ Features

### 🎨 **FREE AI Image Generation**
- Uses Bing Image Creator (DALL-E 3) - completely free!
- Intelligent scene analysis and prompt optimization
- Animated Disney Pixar style visuals
- Custom fallback scenes with professional styling
- Multiple video quality options (480p, 720p, 1080p)

### 🎙️ **Advanced Text-to-Speech**
- **ElevenLabs API** support for premium voice quality
- **Edge TTS** as free fallback option
- Automatic voice provider switching
- Character usage tracking
- Multiple voice options

### 🎬 **Professional Video Production**
- MoviePy-powered video processing
- Automatic scene timing based on audio length
- High-quality video encoding with FFmpeg
- Individual scene downloads
- Batch processing capabilities

### 🚀 **Enhanced User Experience**
- Beautiful Streamlit web interface
- Real-time progress tracking with time estimates
- Scene preview functionality
- Advanced settings and quality controls
- Comprehensive error handling and recovery

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for video processing)

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-video-generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from https://ffmpeg.org/download.html

5. **Configure API keys (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

## 🎯 Usage

### Basic Workflow

1. **Write Your Script**
   - Enter one line per scene
   - Use descriptive, visual language
   - Keep scenes concise but detailed

2. **Configure Settings**
   - Choose video quality (480p/720p/1080p)
   - Select voice provider
   - Set scene duration

3. **Generate Video**
   - Click "Generate Video"
   - Monitor progress in real-time
   - Download individual scenes or final video

### Example Scripts

**Fantasy Adventure:**
```
A brave knight enters a mystical enchanted forest filled with glowing trees.
The knight discovers an ancient treasure chest hidden beneath magical vines.
Inside the chest lies a powerful sword that radiates golden light.
The sword grants the knight the power to protect the innocent.
The knight emerges from the forest as a legendary hero.
```

**Space Exploration:**
```
A sleek spaceship approaches a mysterious alien planet with purple skies.
The astronaut steps onto the planet's surface covered in crystal formations.
Strange alien creatures with friendly eyes greet the visitor peacefully.
The astronaut and aliens share knowledge about their different worlds.
Together they build a bridge of friendship across the galaxy.
```

## 🔧 Advanced Features

### API Keys Setup

**ElevenLabs (Optional - Premium Voices)**
1. Sign up at https://elevenlabs.io/
2. Get your API key from the dashboard
3. Add to `.env`: `ELEVENLABS_API_KEY=your_key_here`

**Benefits:**
- Higher quality, more natural voices
- Multiple voice options
- Better pronunciation and emotion

### Video Quality Settings

- **High (1080p)**: Best quality, larger files
- **Medium (720p)**: Balanced quality and size (recommended)
- **Low (480p)**: Faster processing, smaller files

### Free AI Image Generation

The application uses **Bing Image Creator** (powered by DALL-E 3) which is completely free:

1. **Automated Instructions**: The app provides optimized prompts
2. **Manual Upload**: Upload your own generated images
3. **Fallback Scenes**: Custom animated scenes if needed

## 📁 Project Structure

```
ai-video-generator/
├── app.py                 # Main Streamlit application
├── run.py                 # Application launcher
├── config.py              # Configuration settings
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── modules/
│   ├── tts_module.py     # Text-to-speech handling
│   ├── image_module.py   # AI image generation
│   └── video_module.py   # Video processing
└── temp/                 # Generated files
    ├── images/           # Generated images
    ├── audio/            # Voice audio files
    ├── scenes/           # Individual scene videos
    └── output/           # Final videos
```

## 🎨 Customization

### Adding New Voice Providers
1. Extend `TTSGenerator` class in `modules/tts_module.py`
2. Add provider selection in the UI
3. Implement voice generation method

### Custom Image Styles
1. Modify prompt templates in `modules/image_module.py`
2. Add new style options in the UI
3. Customize scene analysis logic

### Video Effects
1. Extend `VideoGenerator` class in `modules/video_module.py`
2. Add transition effects
3. Implement background music support

## 🔍 Troubleshooting

### Common Issues

**FFmpeg not found**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

**Memory issues with large scripts**
- Reduce video quality to 720p or 480p
- Process fewer scenes at once
- Increase system RAM if possible

**ElevenLabs API errors**
- Check your API key is valid
- Monitor character usage limits
- The app will automatically fallback to Edge TTS

**Image generation issues**
- Follow the manual Bing Image Creator instructions
- Upload your own images if needed
- Custom fallback scenes will be created automatically

## 📊 Performance Tips

### Optimization Strategies

1. **Video Quality**: Use 720p for best balance
2. **Script Length**: Start with 5-10 scenes for testing
3. **Batch Processing**: Enable for large scripts
4. **System Resources**: Close other applications during processing

### Processing Time Estimates

- **Simple script (5 scenes)**: 2-5 minutes
- **Medium script (10 scenes)**: 5-10 minutes
- **Large script (20+ scenes)**: 15-30 minutes

*Times vary based on system performance and API response times*

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make your changes** and test thoroughly
4. **Submit a pull request** with a clear description

### Areas for Contribution

- New AI image providers
- Additional voice options
- Video effects and transitions
- UI/UX improvements
- Performance optimizations
- Documentation updates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for the amazing web framework
- **MoviePy** for video processing capabilities
- **ElevenLabs** for high-quality text-to-speech
- **Microsoft Edge TTS** for free voice generation
- **Bing Image Creator** for free AI image generation
- **FFmpeg** for video encoding support

## 📞 Support

Having issues? Here's how to get help:

1. **Check the troubleshooting section** above
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Join our community** for discussions and tips

---

**Made with ❤️ for content creators, educators, and storytellers worldwide!**

*Transform your imagination into animated reality with the power of AI.*
