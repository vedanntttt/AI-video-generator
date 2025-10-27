"""
Utility functions for the AI Animated Video Generator
"""
import os
import shutil
import subprocess
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

def check_ffmpeg() -> bool:
    """Check if FFmpeg is available on the system"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_file_size(file_path: str) -> float:
    """Get file size in MB"""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)  # Convert to MB
    except OSError:
        return 0.0

def get_video_info(video_path: str) -> dict:
    """Get basic video information"""
    try:
        from moviepy.editor import VideoFileClip
        
        with VideoFileClip(video_path) as clip:
            return {
                'duration': clip.duration,
                'fps': clip.fps,
                'size': clip.size,
                'has_audio': clip.audio is not None,
                'file_size': get_file_size(video_path)
            }
    except Exception:
        return {
            'file_size': get_file_size(video_path)
        }

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for cross-platform compatibility"""
    import re
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    return sanitized

def ensure_audio_format(audio_path: str, target_format: str = "mp3") -> str:
    """Ensure audio file is in the correct format"""
    if not audio_path.endswith(f".{target_format}"):
        # Convert using FFmpeg if needed
        try:
            new_path = audio_path.rsplit('.', 1)[0] + f".{target_format}"
            subprocess.run([
                'ffmpeg', '-i', audio_path, '-y', new_path
            ], capture_output=True, check=True)
            return new_path
        except subprocess.CalledProcessError:
            return audio_path  # Return original if conversion fails
    return audio_path

def create_backup(file_path: str) -> str:
    """Create a backup of a file"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup"
        shutil.copy2(file_path, backup_path)
        return backup_path
    return ""

def count_files_in_directory(directory: str, extension: str = None) -> int:
    """Count files in a directory, optionally filtered by extension"""
    if not os.path.exists(directory):
        return 0
    
    files = os.listdir(directory)
    if extension:
        files = [f for f in files if f.endswith(extension)]
    
    return len(files)
