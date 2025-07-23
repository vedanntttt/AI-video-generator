"""
AI Animated Video Generator from Script
A Streamlit app that converts text scripts into animated videos
"""
import streamlit as st
import os
from typing import List
import config
import utils
from modules.tts_module import TTSGenerator
from modules.image_module import ImageGenerator
from modules.video_module import VideoGenerator

def main():
    st.set_page_config(
        page_title="AI Animated Video Generator",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 AI Animated Video Generator")
    st.markdown("Transform your script into an animated video with AI-generated images and voices!")
    
    # Initialize session state
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'final_video_path' not in st.session_state:
        st.session_state.final_video_path = None
    
    # Create necessary directories
    utils.create_directories()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Information about free image generation
        st.success("🆓 FREE AI Images: Using Bing Image Creator (DALL-E 3) - No API key needed!")

        # ElevenLabs API key input
        elevenlabs_key = st.text_input(
            "ElevenLabs API Key (Optional)",
            type="password",
            help="Enter your ElevenLabs API key for better voice quality. Leave empty to use Edge TTS."
        )

        if elevenlabs_key:
            os.environ["ELEVENLABS_API_KEY"] = elevenlabs_key

        # Voice selection
        voice_provider = st.selectbox(
            "Voice Provider",
            ["Auto (ElevenLabs → Edge TTS)", "Edge TTS Only"],
            help="Auto will try ElevenLabs first, then fallback to Edge TTS"
        )

        # Video settings
        st.subheader("Video Settings")
        scene_duration = st.slider(
            "Minimum Scene Duration (seconds)",
            min_value=2,
            max_value=10,
            value=config.DEFAULT_SCENE_DURATION
        )

        # Show character usage if ElevenLabs is being used
        if elevenlabs_key and 'tts_generator' in st.session_state:
            usage = st.session_state.tts_generator.get_character_usage()
            st.metric(
                "ElevenLabs Usage",
                f"{usage['used']}/{usage['limit']}",
                f"{usage['remaining']} remaining"
            )

        # Cleanup button
        if st.button("🗑️ Clear Temp Files"):
            utils.cleanup_temp_files()
            st.success("Temporary files cleared!")

        # Help section
        st.subheader("📚 Quick Help")
        with st.expander("How to use"):
            st.markdown("""
            1. **Write your script** - One line per scene
            2. **Configure settings** - Add API keys if available
            3. **Generate video** - Click the generate button
            4. **Download result** - Preview and download your video

            **Tips:**
            - Keep lines descriptive but concise
            - Use visual, animated-style descriptions
            - Each line becomes one scene in your video
            """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📝 Script Input")

        # Example scripts
        example_scripts = {
            "Fantasy Adventure": """A brave knight enters a mystical enchanted forest filled with glowing trees.
The knight discovers a ancient treasure chest hidden beneath magical vines.
Inside the chest lies a powerful sword that radiates golden light.
The sword grants the knight the power to protect the innocent.
The knight emerges from the forest as a legendary hero.""",

            "Space Exploration": """A sleek spaceship approaches a mysterious alien planet with purple skies.
The astronaut steps onto the planet's surface covered in crystal formations.
Strange alien creatures with friendly eyes greet the visitor peacefully.
The astronaut and aliens share knowledge about their different worlds.
Together they build a bridge of friendship across the galaxy.""",

            "Underwater Adventure": """A colorful submarine dives deep into the sparkling ocean depths.
Schools of rainbow fish swim gracefully around coral reef gardens.
A friendly dolphin guides the submarine to a hidden underwater city.
The city is filled with mermaids and seahorse guardians dancing.
The submarine returns to the surface with magical ocean treasures."""
        }

        selected_example = st.selectbox(
            "Choose an example script or write your own:",
            ["Custom Script"] + list(example_scripts.keys())
        )

        if selected_example != "Custom Script":
            default_script = example_scripts[selected_example]
        else:
            default_script = ""

        script_text = st.text_area(
            "Enter your script (one line = one scene):",
            value=default_script,
            height=300,
            placeholder="Line 1: Once upon a time in a magical forest...\nLine 2: A brave knight discovered a hidden treasure...\nLine 3: The treasure glowed with mysterious power..."
        )

        # Script analysis
        if script_text.strip():
            lines = utils.validate_script_lines(script_text.split('\n'))
            total_chars = sum(len(line) for line in lines)
            estimated_duration = sum(utils.estimate_reading_time(line) for line in lines)

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Scenes", len(lines))
            with col_b:
                st.metric("Characters", total_chars)
            with col_c:
                st.metric("Est. Duration", utils.format_duration(estimated_duration))

        if st.button("🚀 Generate Video", type="primary"):
            if script_text.strip():
                # Validate script
                script_lines = [line.strip() for line in script_text.strip().split('\n') if line.strip()]

                if len(script_lines) > 15:
                    st.warning(f"⚠️ Large script detected ({len(script_lines)} scenes). This may take 5-10 minutes.")
                    if not st.checkbox("✅ I understand this will take time to process", key="large_script_confirm"):
                        st.info("💡 Tip: Try with fewer scenes first to test the system")
                        return

                # Estimate processing time
                estimated_time = len(script_lines) * 20  # ~20 seconds per scene
                if estimated_time > 300:  # 5 minutes
                    st.warning(f"⏱️ Estimated processing time: {estimated_time//60} minutes")

                generate_video(script_text, voice_provider, scene_duration)
            else:
                st.error("❌ Please enter a script!")
    
    with col2:
        st.header("📊 Progress")
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        if st.session_state.processing_complete and st.session_state.final_video_path:
            st.success("✅ Video generation complete!")
            
            # Video preview
            if os.path.exists(st.session_state.final_video_path):
                st.video(st.session_state.final_video_path)
                
                # Download button
                with open(st.session_state.final_video_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Video",
                        data=file.read(),
                        file_name="animated_video.mp4",
                        mime="video/mp4"
                    )

def generate_video(script_text: str, voice_provider: str, scene_duration: int):
    """Generate video from script"""
    # Parse script lines
    script_lines = utils.validate_script_lines(script_text.split('\n'))
    
    if not script_lines:
        st.error("No valid script lines found!")
        return
    
    st.info(f"Processing {len(script_lines)} scenes...")
    
    # Initialize generators
    tts_generator = TTSGenerator(use_elevenlabs=(voice_provider == "Auto (ElevenLabs → Edge TTS)"))
    image_generator = ImageGenerator()
    video_generator = VideoGenerator()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        scene_files = []
        failed_scenes = []
        total_steps = len(script_lines) * 3 + 1  # 3 steps per scene + final concatenation
        current_step = 0

        # Show processing statistics
        stats_container = st.container()

        for i, line in enumerate(script_lines):
            scene_num = i + 1
            status_text.text(f"🎬 Processing scene {scene_num}/{len(script_lines)}: {line[:50]}...")

            try:
                # Step 1: Generate image with retry logic
                status_text.text(f"🎨 Scene {scene_num}: Generating AI image...")
                try:
                    image_path = image_generator.generate_image(line, scene_num)
                    if not os.path.exists(image_path):
                        raise FileNotFoundError(f"Image not generated: {image_path}")
                except Exception as img_error:
                    st.warning(f"⚠️ Scene {scene_num} image generation failed: {str(img_error)}")
                    # Continue with custom scene as fallback
                    image_path = image_generator._generate_custom_scene(line,
                        os.path.join(config.IMAGES_DIR, f"scene_{scene_num}.jpg"), scene_num)

                current_step += 1
                progress_bar.progress(current_step / total_steps)

                # Step 2: Generate audio with retry logic
                status_text.text(f"🎙️ Scene {scene_num}: Generating voice...")
                try:
                    audio_path = tts_generator.generate_speech(line, scene_num)
                    if not os.path.exists(audio_path):
                        raise FileNotFoundError(f"Audio not generated: {audio_path}")
                except Exception as audio_error:
                    st.warning(f"⚠️ Scene {scene_num} audio generation failed: {str(audio_error)}")
                    failed_scenes.append(scene_num)
                    current_step += 2  # Skip video creation
                    progress_bar.progress(current_step / total_steps)
                    continue

                current_step += 1
                progress_bar.progress(current_step / total_steps)

                # Step 3: Create scene video with error handling
                status_text.text(f"🎬 Scene {scene_num}: Creating video scene...")
                try:
                    scene_path = video_generator.create_scene(image_path, audio_path, scene_num, scene_duration)
                    if os.path.exists(scene_path):
                        scene_files.append(scene_path)
                        st.success(f"✅ Scene {scene_num} completed successfully!")
                    else:
                        raise FileNotFoundError(f"Scene video not created: {scene_path}")
                except Exception as video_error:
                    st.error(f"❌ Scene {scene_num} video creation failed: {str(video_error)}")
                    failed_scenes.append(scene_num)

                current_step += 1
                progress_bar.progress(current_step / total_steps)

                # Update statistics
                with stats_container:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Completed", len(scene_files))
                    with col2:
                        st.metric("Failed", len(failed_scenes))
                    with col3:
                        st.metric("Remaining", len(script_lines) - scene_num)

            except Exception as scene_error:
                st.error(f"❌ Critical error in scene {scene_num}: {str(scene_error)}")
                failed_scenes.append(scene_num)
                current_step += 3  # Skip all steps for this scene
                progress_bar.progress(current_step / total_steps)
        
        # Final step: Concatenate all scenes
        if scene_files:
            status_text.text("🎞️ Combining all scenes into final video...")
            try:
                final_video_path = video_generator.concatenate_scenes(scene_files)
                current_step += 1
                progress_bar.progress(1.0)

                # Update session state
                st.session_state.processing_complete = True
                st.session_state.final_video_path = final_video_path

                # Show final results
                status_text.text("✅ Video generation complete!")

                # Success summary
                success_count = len(scene_files)
                total_count = len(script_lines)

                if failed_scenes:
                    st.warning(f"⚠️ Video completed with {success_count}/{total_count} scenes. Failed scenes: {failed_scenes}")
                else:
                    st.success(f"🎉 Perfect! All {success_count} scenes completed successfully!")

                st.success(f"📁 Video saved to: {final_video_path}")

                # Show processing statistics
                if hasattr(video_generator, 'processing_stats'):
                    stats = video_generator.processing_stats
                    st.info(f"📊 Processing Stats - Scenes: {stats['scenes_created']}, Errors: {stats['errors']}")

            except Exception as concat_error:
                st.error(f"❌ Final video concatenation failed: {str(concat_error)}")
                st.info("💡 Individual scene files are still available in the scenes folder")
        else:
            st.error("❌ No scenes were successfully created. Please check your script and try again.")
            if failed_scenes:
                st.error(f"Failed scenes: {failed_scenes}")

    except Exception as e:
        st.error(f"❌ Critical error during video generation: {str(e)}")
        st.exception(e)
        st.info("💡 Try with a shorter script or check your system resources")

if __name__ == "__main__":
    main()
