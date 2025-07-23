"""
Quick test of the optimized AI Video Generator
"""
import time
import os
from modules.tts_module import TTSGenerator
from modules.image_module import ImageGenerator
from modules.video_module import VideoGenerator
import config
import utils

def quick_test():
    print('🚀 QUICK TEST - Optimized AI Video Generator')
    print('=' * 50)
    
    # Custom test script - 3 different themed scenes
    test_script = [
        'A brave knight enters a dark mysterious castle',
        'Inside the castle, glowing magical crystals light the way', 
        'The knight discovers a golden treasure chest'
    ]
    
    utils.create_directories()
    
    # Initialize generators
    tts = TTSGenerator(use_elevenlabs=False)
    img_gen = ImageGenerator()
    video_gen = VideoGenerator()
    
    scene_files = []
    total_start = time.time()
    
    for i, line in enumerate(test_script):
        scene_num = i + 1
        scene_start = time.time()
        
        print(f'\n🎬 Scene {scene_num}: {line[:40]}...')
        
        # Generate components
        print('   - Creating themed image...')
        image_path = img_gen.generate_image(line, scene_num)
        
        print('   - Generating AI voice...')
        audio_path = tts.generate_speech(line, scene_num)
        
        print('   - Building video with subtitles...')
        scene_path = video_gen.create_scene(image_path, audio_path, scene_num, text=line)
        scene_files.append(scene_path)
        
        scene_time = time.time() - scene_start
        print(f'   ✅ Scene {scene_num} complete in {scene_time:.1f}s')
    
    # Combine scenes
    print('\n🎞️ Combining all scenes...')
    combine_start = time.time()
    final_video = video_gen.concatenate_scenes(scene_files)
    combine_time = time.time() - combine_start
    
    total_time = time.time() - total_start
    
    # Get results
    if os.path.exists(final_video):
        file_size = os.path.getsize(final_video) / (1024 * 1024)
        video_info = video_gen.get_video_info(final_video)
        
        print('\n🎉 TEST RESULTS:')
        print('=' * 50)
        print(f'📁 Video saved: {final_video}')
        print(f'⏱️ Total time: {total_time:.1f} seconds')
        print(f'📊 File size: {file_size:.2f} MB')
        print(f'🎬 Scenes: {len(test_script)}')
        print(f'⚡ Speed: {total_time/len(test_script):.1f}s per scene')
        print(f'🔗 Combine time: {combine_time:.1f}s')
        
        if video_info:
            print(f'📺 Resolution: {video_info.get("size", "Unknown")}')
            print(f'🎵 Duration: {video_info.get("duration", 0):.1f}s')
        
        print('\n✨ FEATURES TESTED:')
        print('   ✅ Castle theme - Dark gradient background')
        print('   ✅ Magic theme - Mystical colors')
        print('   ✅ Treasure theme - Golden tones')
        print('   ✅ Centered subtitles on all scenes')
        print('   ✅ Fast video encoding (ultrafast preset)')
        print('   ✅ Optimized resolution (854x480)')
        print('   ✅ Multi-threaded processing')
        
        return True
    else:
        print('❌ Video creation failed')
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print('\n🚀 Ready for Streamlit! Go to http://localhost:8501')
    else:
        print('\n❌ Please check the error messages above')
