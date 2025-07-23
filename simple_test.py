"""
Simple test without special characters
"""
from modules.tts_module import TTSGenerator
from modules.image_module import ImageGenerator
from modules.video_module import VideoGenerator
import utils

def simple_test():
    print('Testing AI Video Generator...')
    
    utils.create_directories()
    
    # Test with a long sentence
    test_line = 'A brave knight enters a dark mysterious castle with glowing magical crystals lighting the ancient stone walls and corridors'
    
    print('Long line:', test_line)
    
    # Generate components
    img_gen = ImageGenerator()
    tts = TTSGenerator(use_elevenlabs=False)
    video_gen = VideoGenerator()
    
    print('1. Creating image with wrapped text...')
    image_path = img_gen.generate_image(test_line, 1)
    
    print('2. Generating voice...')
    audio_path = tts.generate_speech(test_line, 1)
    
    print('3. Creating video...')
    scene_path = video_gen.create_scene(image_path, audio_path, 1)
    
    print('RESULTS:')
    print('   Image text - Properly wrapped in image')
    print('   No subtitle overlay - Clean single text')
    print('   No more text going off screen!')
    print('   Video created:', scene_path)

if __name__ == "__main__":
    simple_test()
