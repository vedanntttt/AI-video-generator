"""
Configuration file for AI Animated Video Generator
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ElevenLabs API Configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_FREE_CHAR_LIMIT = 10000

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DALLE_MODEL = "dall-e-3"
DALLE_SIZE = "1792x1024"  # HD landscape format
DALLE_QUALITY = "standard"  # standard or hd
DALLE_STYLE = "vivid"  # vivid or natural

# File paths and directories
TEMP_DIR = "temp"
IMAGES_DIR = os.path.join(TEMP_DIR, "images")
AUDIO_DIR = os.path.join(TEMP_DIR, "audio")
SCENES_DIR = os.path.join(TEMP_DIR, "scenes")
OUTPUT_DIR = "output"

# Video settings (optimized for quality)
DEFAULT_SCENE_DURATION = 3  # seconds per scene minimum
VIDEO_FPS = 24  # Standard FPS for smooth video
VIDEO_RESOLUTION = (1280, 720)  # HD resolution for crisp quality

# Audio settings
AUDIO_SAMPLE_RATE = 22050
AUDIO_CHANNELS = 1

# Image settings (optimized for quality)
IMAGE_SIZE = (1280, 720)  # HD resolution to match video
IMAGE_STYLE_PROMPT = "animated style, cartoon, colorful, high quality"

# Supported file formats
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.m4a']
