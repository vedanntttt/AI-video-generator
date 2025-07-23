"""
Demo of the FREE Bing Image Creator integration
"""
import streamlit as st
from modules.image_module import ImageGenerator
import utils

def main():
    st.title("🆓 FREE AI Video Generator with Bing Image Creator")
    st.markdown("### Using DALL-E 3 completely FREE - No API keys needed!")
    
    # Create directories
    utils.create_directories()
    
    # Initialize image generator
    img_gen = ImageGenerator()
    
    st.markdown("---")
    st.subheader("🎨 Test FREE AI Image Generation")
    
    # Test input
    test_text = st.text_input(
        "Enter a scene description:",
        value="A brave knight enters a dark mysterious castle with glowing crystals",
        help="Describe the scene you want to visualize"
    )
    
    scene_number = st.number_input("Scene number:", min_value=1, max_value=10, value=1)
    
    if st.button("🎨 Generate FREE AI Image Instructions"):
        if test_text:
            st.markdown("### 🚀 Processing...")
            
            # This will show the Bing Image Creator instructions
            image_path = img_gen.generate_image(test_text, scene_number)
            
            st.success(f"✅ Instructions generated for scene {scene_number}!")
            
            # Show what happens next
            st.markdown("### 🎬 Next Steps:")
            st.markdown("""
            1. **Follow the Bing Image Creator instructions above**
            2. **Upload your AI-generated image using the file uploader**
            3. **The system will automatically add centered text overlay**
            4. **Use the image in your video generation**
            
            **🆓 Benefits:**
            - ✅ **Completely FREE** - Uses Bing Image Creator (DALL-E 3)
            - ✅ **No API keys needed** - Just visit bing.com/images/create
            - ✅ **High quality** - DALL-E 3 powered images
            - ✅ **Animated style** - Optimized prompts for cartoon/animated look
            - ✅ **Centered text** - Professional text overlay automatically added
            - ✅ **HD resolution** - 1280x720 crisp quality
            """)
            
            st.markdown("---")
            st.info("💡 **Tip:** You can generate multiple images and choose the best one!")
        else:
            st.warning("Please enter a scene description!")
    
    st.markdown("---")
    st.markdown("### 📊 Usage Statistics")
    st.metric("Free Images Generated", img_gen.bing_usage_count)
    st.success("🆓 All images are completely FREE using Bing Image Creator!")
    
    st.markdown("---")
    st.markdown("### 🎬 Full Video Generation")
    st.markdown("""
    **Ready to create full videos?**
    
    Run the main app: `streamlit run app.py`
    
    **Features:**
    - 🆓 **FREE AI images** with Bing Image Creator
    - 🎙️ **AI voices** with Edge TTS (free) or ElevenLabs
    - 🎬 **HD video generation** with perfect text centering
    - ⚡ **Fast processing** - ~15-20 seconds per scene
    - 📱 **Easy to use** - Just paste your script and go!
    """)

if __name__ == "__main__":
    main()
