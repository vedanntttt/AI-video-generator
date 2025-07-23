"""
Test script to verify installation and basic functionality
"""
import sys
import os
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'streamlit',
        'moviepy',
        'requests',
        'edge_tts',
        'elevenlabs',
        'PIL',
        'numpy',
        'dotenv',
        'pydub'
    ]
    
    print("Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {str(e)}")
            failed_imports.append(package)
    
    return failed_imports

def test_directories():
    """Test if directories can be created"""
    print("\nTesting directory creation...")
    
    import config
    import utils
    
    try:
        utils.create_directories()
        
        directories = [
            config.TEMP_DIR,
            config.IMAGES_DIR,
            config.AUDIO_DIR,
            config.SCENES_DIR,
            config.OUTPUT_DIR
        ]
        
        for directory in directories:
            if os.path.exists(directory):
                print(f"✅ {directory}")
            else:
                print(f"❌ {directory}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Directory creation failed: {str(e)}")
        return False

def test_basic_functionality():
    """Test basic module functionality"""
    print("\nTesting basic functionality...")
    
    try:
        # Test TTS module
        from modules.tts_module import TTSGenerator
        tts = TTSGenerator(use_elevenlabs=False)  # Use Edge TTS only for testing
        print("✅ TTS module initialized")
        
        # Test Image module
        from modules.image_module import ImageGenerator
        img_gen = ImageGenerator()
        print("✅ Image module initialized")
        
        # Test Video module
        from modules.video_module import VideoGenerator
        video_gen = VideoGenerator()
        print("✅ Video module initialized")
        
        return True
    except Exception as e:
        print(f"❌ Module initialization failed: {str(e)}")
        return False

def test_ffmpeg():
    """Test if FFmpeg is available"""
    print("\nTesting FFmpeg availability...")

    try:
        # First try imageio-ffmpeg (comes with MoviePy)
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"✅ FFmpeg available via imageio-ffmpeg: {ffmpeg_path}")
        return True
    except Exception:
        pass

    try:
        # Fallback to system FFmpeg
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg is available (system)")
            return True
        else:
            print("❌ FFmpeg not working properly")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found. Please install FFmpeg.")
        return False
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg test timed out")
        return False
    except Exception as e:
        print(f"❌ FFmpeg test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Animated Video Generator - Installation Test")
    print("=" * 50)
    
    # Test imports
    failed_imports = test_imports()
    
    # Test directories
    dirs_ok = test_directories()
    
    # Test basic functionality
    modules_ok = test_basic_functionality()
    
    # Test FFmpeg
    ffmpeg_ok = test_ffmpeg()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    if not failed_imports:
        print("✅ All packages imported successfully")
    else:
        print(f"❌ Failed imports: {', '.join(failed_imports)}")
        print("   Run: pip install -r requirements.txt")
    
    if dirs_ok:
        print("✅ Directory creation successful")
    else:
        print("❌ Directory creation failed")
    
    if modules_ok:
        print("✅ Module initialization successful")
    else:
        print("❌ Module initialization failed")
    
    if ffmpeg_ok:
        print("✅ FFmpeg is ready")
    else:
        print("❌ FFmpeg needs to be installed")
        print("   Windows: choco install ffmpeg")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
    
    # Overall result
    all_tests_passed = not failed_imports and dirs_ok and modules_ok and ffmpeg_ok
    
    if all_tests_passed:
        print("\n🎉 All tests passed! You can run the app with:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before running the app.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
