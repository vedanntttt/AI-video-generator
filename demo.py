"""
Demo script to test the AI Video Generator functionality
Creates a simple 2-scene video to verify everything works
"""
import os
import sys
import time
from modules.tts_module import TTSGenerator
from modules.image_module import ImageGenerator
from modules.video_module import VideoGenerator
import config
import utils

def run_demo():
    """Run a simple demo to test functionality"""
    print("🎬 AI Video Generator Demo")
    print("=" * 40)
    
    # Create directories
    utils.create_directories()
    
    # Demo script
    demo_script = [
        "A magical unicorn dances in a colorful rainbow forest.",
        "The unicorn finds a sparkling crystal that grants wishes."
    ]
    
    print(f"Creating demo video with {len(demo_script)} scenes...")
    
    try:
        # Initialize generators
        print("\n1. Initializing modules...")
        tts_generator = TTSGenerator(use_elevenlabs=False)  # Use Edge TTS for demo
        image_generator = ImageGenerator()
        video_generator = VideoGenerator()
        
        scene_files = []
        
        # Process each scene
        for i, line in enumerate(demo_script):
            scene_num = i + 1
            print(f"\n2.{scene_num} Processing scene {scene_num}: {line}")
            
            # Generate image (placeholder)
            print(f"   - Generating image...")
            image_path = image_generator.generate_image(line, scene_num)
            
            # Generate audio
            print(f"   - Generating voice...")
            audio_path = tts_generator.generate_speech(line, scene_num)
            
            # Create scene video (text is already in the image)
            print(f"   - Creating video scene...")
            scene_path = video_generator.create_scene(image_path, audio_path, scene_num)
            scene_files.append(scene_path)
            
            print(f"   ✅ Scene {scene_num} complete")
        
        # Combine scenes
        print(f"\n3. Combining scenes into final video...")
        final_video = video_generator.concatenate_scenes(scene_files)
        
        print(f"\n🎉 Demo complete!")
        print(f"📁 Video saved to: {final_video}")
        
        # Check file size
        if os.path.exists(final_video):
            file_size = os.path.getsize(final_video) / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.2f} MB")
            
            # Get video info
            video_info = video_generator.get_video_info(final_video)
            if video_info:
                print(f"⏱️  Duration: {video_info.get('duration', 'Unknown'):.1f} seconds")
                print(f"📺 Resolution: {video_info.get('size', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_demo():
    """Clean up demo files"""
    print("\n🧹 Cleaning up demo files...")
    utils.cleanup_temp_files()
    print("✅ Cleanup complete")

if __name__ == "__main__":
    print("Starting demo in 3 seconds... (Ctrl+C to cancel)")
    try:
        time.sleep(3)
        success = run_demo()
        
        if success:
            print("\n" + "=" * 40)
            print("✅ Demo successful! The AI Video Generator is working.")
            print("🚀 You can now run the full app with: streamlit run app.py")
            
            # Ask if user wants to clean up
            try:
                response = input("\nClean up demo files? (y/n): ").lower().strip()
                if response in ['y', 'yes']:
                    cleanup_demo()
            except KeyboardInterrupt:
                print("\nSkipping cleanup.")
        else:
            print("\n❌ Demo failed. Please check the error messages above.")
            
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user.")
        sys.exit(1)
