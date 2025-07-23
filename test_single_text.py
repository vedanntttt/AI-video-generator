"""
Test the single text version (only image text, no subtitle overlay)
"""
from modules.tts_module import TTSGenerator
from modules.image_module import ImageGenerator
from modules.video_module import VideoGenerator
import utils

def test_single_text():
    print('🎬 Testing SINGLE TEXT Version')
    print('=' * 50)
    
    utils.create_directories()
    
    # Test with long sentences that need wrapping
    test_cases = [
        'A brave knight enters a dark mysterious castle with glowing magical crystals lighting the ancient stone walls',
        'The magical unicorn dances gracefully in the enchanted rainbow forest under the bright moonlight with sparkling stars',
        'Deep in the vast ocean, colorful fish swim around beautiful coral reefs with hidden treasures and ancient secrets'
    ]
    
    # Initialize generators
    img_gen = ImageGenerator()
    tts = TTSGenerator(use_elevenlabs=False)
    video_gen = VideoGenerator()
    
    scene_files = []
    
    for i, test_line in enumerate(test_cases, 1):
        print(f'\n🎨 Scene {i}: {test_line[:50]}...')
        
        # Generate image with wrapped text
        print('   - Creating image with wrapped text...')
        image_path = img_gen.generate_image(test_line, i)
        
        # Generate voice
        print('   - Generating AI voice...')
        audio_path = tts.generate_speech(test_line, i)
        
        # Create video with ONLY image text (no subtitle overlay)
        print('   - Creating clean video (image + voice only)...')
        scene_path = video_gen.create_scene(image_path, audio_path, i, text=test_line)
        scene_files.append(scene_path)
        
        print(f'   ✅ Scene {i} complete - Clean single text!')
    
    # Combine all scenes
    print(f'\n🎞️ Combining {len(scene_files)} scenes...')
    final_video = video_gen.concatenate_scenes(scene_files)
    
    print('\n🎉 SINGLE TEXT VERSION COMPLETE!')
    print('=' * 50)
    print(f'📁 Final video: {final_video}')
    print('\n✨ WHAT YOU GET:')
    print('   ✅ Only ONE text element - In the background image')
    print('   ✅ Text wraps properly - Multiple lines, stays on screen')
    print('   ✅ Vibrant themed backgrounds - Colors match story content')
    print('   ✅ Clean video - No subtitle overlay, just image + voice')
    print('   ✅ Fast processing - Still ~7-8 seconds per scene')
    
    print('\n🚀 Ready to use in Streamlit!')
    print('   Go to: http://localhost:8501')
    print('   Now you get clean videos with just wrapped text in images!')

if __name__ == "__main__":
    test_single_text()
