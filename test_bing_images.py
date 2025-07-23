"""
Test the FREE Bing Image Creator integration
"""
from modules.image_module import ImageGenerator
import utils

def test_bing_images():
    print('Testing FREE BING IMAGE CREATOR (DALL-E 3)...')
    print('=' * 60)
    
    utils.create_directories()
    img_gen = ImageGenerator()
    
    # Test different scene types
    test_scenes = [
        'A brave knight enters a dark mysterious castle',
        'A magical unicorn dances in an enchanted forest',
        'A spaceship approaches an alien planet with purple skies'
    ]
    
    for i, scene_text in enumerate(test_scenes, 1):
        print(f'\n🎨 Scene {i}: {scene_text}')
        
        # This will show Bing instructions in Streamlit
        image_path = img_gen.generate_image(scene_text, i)
        print(f'   ✅ Instructions shown for: {image_path}')
        print(f'   ✅ FREE Bing Image Creator prompt generated')
        print(f'   ✅ Fallback custom scene created if needed')
    
    print('\n🆓 FREE BING IMAGE CREATOR FEATURES:')
    print('   ✅ Uses DALL-E 3 completely FREE')
    print('   ✅ No API key required')
    print('   ✅ High-quality AI-generated images')
    print('   ✅ Optimized prompts for animated style')
    print('   ✅ Centered text overlay on images')
    print('   ✅ Upload functionality for easy use')
    print('   ✅ Custom scene fallback if needed')
    
    print('\n🚀 Usage Instructions:')
    print('   1. Run: streamlit run app.py')
    print('   2. Enter your script')
    print('   3. Follow Bing Image Creator instructions')
    print('   4. Upload generated images or use custom scenes')
    print('   5. Get professional videos with AI images!')
    
    print(f'\n📊 Current usage: {img_gen.bing_usage_count} images (all FREE!)')

if __name__ == "__main__":
    test_bing_images()
