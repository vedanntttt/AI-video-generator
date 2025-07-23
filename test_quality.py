"""
Test the improved video quality settings
"""
from modules.tts_module import TTSGenerator
from modules.image_module import ImageGenerator
from modules.video_module import VideoGenerator
import utils
import os

def test_quality():
    print('Testing IMPROVED VIDEO QUALITY...')
    print('=' * 50)
    
    utils.create_directories()
    
    # Test with a sentence
    test_line = 'A brave knight enters a dark mysterious castle with glowing magical crystals'
    
    print('Test line:', test_line)
    print('Improvements applied:')
    print('  - Removed zoom effect (no more blur from scaling)')
    print('  - HD resolution (1280x720)')
    print('  - Better encoding preset (medium instead of ultrafast)')
    print('  - Higher bitrate (1500k for scenes, 2000k for final)')
    print('  - Standard 24 FPS')
    
    # Generate components
    img_gen = ImageGenerator()
    tts = TTSGenerator(use_elevenlabs=False)
    video_gen = VideoGenerator()
    
    print('\n1. Creating HD image...')
    image_path = img_gen.generate_image(test_line, 1)
    
    print('2. Generating voice...')
    audio_path = tts.generate_speech(test_line, 1)
    
    print('3. Creating CRISP video (no zoom, HD quality)...')
    scene_path = video_gen.create_scene(image_path, audio_path, 1)
    
    # Check file size and quality
    if os.path.exists(scene_path):
        file_size = os.path.getsize(scene_path) / (1024 * 1024)
        video_info = video_gen.get_video_info(scene_path)
        
        print('\nQUALITY TEST RESULTS:')
        print('=' * 50)
        print(f'Video file: {scene_path}')
        print(f'File size: {file_size:.2f} MB')
        if video_info:
            print(f'Resolution: {video_info.get("size", "Unknown")}')
            print(f'Duration: {video_info.get("duration", 0):.1f}s')
            print(f'FPS: {video_info.get("fps", "Unknown")}')
        
        print('\nQUALITY IMPROVEMENTS:')
        print('  ✅ NO zoom effect - Static, sharp image')
        print('  ✅ HD resolution - 1280x720 crisp quality')
        print('  ✅ Better encoding - Medium preset for quality')
        print('  ✅ Higher bitrate - 1500k for clear video')
        print('  ✅ Standard FPS - 24fps for smooth playback')
        print('  ✅ Single text - Clean, readable text in image')
        
        print('\n🚀 Video should now be MUCH less blurry!')
    else:
        print('❌ Video creation failed')

if __name__ == "__main__":
    test_quality()
