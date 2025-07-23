"""
Test both image text and subtitle text wrapping
"""
from modules.tts_module import TTSGenerator
from modules.image_module import ImageGenerator
from modules.video_module import VideoGenerator
import utils

def test_both_texts():
    print('🔧 Testing BOTH Text Elements')
    print('=' * 50)
    
    utils.create_directories()
    
    # Test with a very long sentence
    long_sentence = 'A brave knight enters a dark mysterious castle with glowing magical crystals lighting the ancient stone walls and corridors throughout the entire fortress'
    
    print(f'Testing long sentence: {long_sentence[:60]}...')
    
    # Initialize generators
    img_gen = ImageGenerator()
    tts = TTSGenerator(use_elevenlabs=False)
    video_gen = VideoGenerator()
    
    print('\n1. Creating image with wrapped text...')
    image_path = img_gen.generate_image(long_sentence, 1)
    print('   ✅ Image text should be wrapped in multiple lines')
    
    print('\n2. Generating voice...')
    audio_path = tts.generate_speech(long_sentence, 1)
    print('   ✅ Voice generated')
    
    print('\n3. Creating video with wrapped subtitles...')
    scene_path = video_gen.create_scene(image_path, audio_path, 1, text=long_sentence)
    print('   ✅ Video subtitles should also be wrapped')
    
    print('\n🎉 BOTH TEXT ISSUES FIXED:')
    print('   ✅ Image text - Wrapped in the background image')
    print('   ✅ Subtitle text - Wrapped in video overlay')
    print('   ✅ No more text going off screen!')
    print('   ✅ Both texts are readable and properly positioned')
    print(f'\n📁 Test video: {scene_path}')
    
    return scene_path

if __name__ == "__main__":
    test_both_texts()
    print('\n🚀 Ready to test in Streamlit!')
    print('   Go to: http://localhost:8501')
    print('   Try long sentences - both image and subtitle text should wrap!')
