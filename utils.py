"""
Utility functions for the AI Animated Video Generator
"""
import os
import shutil
from typing import List
import config

def create_directories():
    """Create necessary directories for the application"""
    directories = [
        config.TEMP_DIR,
        config.IMAGES_DIR,
        config.AUDIO_DIR,
        config.SCENES_DIR,
        config.OUTPUT_DIR
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def cleanup_temp_files():
    """Clean up temporary files and directories"""
    if os.path.exists(config.TEMP_DIR):
        shutil.rmtree(config.TEMP_DIR)
    create_directories()

def get_scene_filename(scene_number: int, file_type: str) -> str:
    """Generate standardized filename for scene files"""
    return f"scene_{scene_number:03d}.{file_type}"

def validate_script_lines(script_lines: List[str]) -> List[str]:
    """Validate and clean script lines"""
    cleaned_lines = []
    for i, line in enumerate(script_lines):
        line = line.strip()
        if line:  # Skip empty lines
            cleaned_lines.append(line)
    return cleaned_lines

def estimate_reading_time(text: str, words_per_minute: int = 150) -> float:
    """Estimate reading time for text in seconds"""
    word_count = len(text.split())
    reading_time = (word_count / words_per_minute) * 60
    return max(reading_time, config.DEFAULT_SCENE_DURATION)  # Minimum scene duration

def format_duration(seconds: float) -> str:
    """Format duration in seconds to MM:SS format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
