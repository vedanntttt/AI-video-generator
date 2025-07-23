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
import demo_scripts

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
    if 'scene_files' not in st.session_state:
        st.session_state.scene_files = []
    
    # Create necessary directories
    utils.create_directories()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # System status
        st.subheader("🔧 System Status")
        
        # Check FFmpeg
        if utils.check_ffmpeg():
            st.success("✅ FFmpeg available")
        else:
            st.error("❌ FFmpeg not found")
            st.info("Install FFmpeg for video processing")

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
        
        # Quality settings
        video_quality = st.selectbox(
            "Video Quality",
            ["High (1080p)", "Medium (720p)", "Low (480p)"],
            index=1
        )
        
        # Update config based on quality selection
        if video_quality == "High (1080p)":
            config.VIDEO_RESOLUTION = (1920, 1080)
            config.IMAGE_SIZE = (1920, 1080)
        elif video_quality == "Medium (720p)":
            config.VIDEO_RESOLUTION = (1280, 720)
            config.IMAGE_SIZE = (1280, 720)
        else:  # Low (480p)
            config.VIDEO_RESOLUTION = (854, 480)
            config.IMAGE_SIZE = (854, 480)

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
            
        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            enable_subtitles = st.checkbox("Add Subtitles to Video", value=False)
            enable_background_music = st.checkbox("Add Background Music", value=False)
            batch_processing = st.checkbox("Batch Processing Mode", value=False)

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
            - Try different video quality settings based on your needs
            """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📝 Script Input")

        # Demo scripts section with enhanced variety
        with st.expander("🎬 Try Demo Scripts", expanded=False):
            st.markdown("**Choose from pre-made scripts to test the generator:**")
            
            demo_titles = demo_scripts.get_all_demo_titles()
            selected_demo = st.selectbox(
                "Select a demo script:",
                [""] + demo_titles,
                format_func=lambda x: "Choose a demo..." if x == "" else x
            )
            
            if selected_demo and selected_demo != "":
                st.info(f"**{selected_demo}:** {demo_scripts.get_demo_description(selected_demo)}")
                if st.button("📋 Load Demo Script"):
                    st.session_state.demo_script = demo_scripts.get_demo_script(selected_demo)
                    st.success(f"✅ Loaded: {selected_demo}")
                    st.rerun()
        
        # Get default script from session state if demo was loaded
        default_script = st.session_state.get('demo_script', '')

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

            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("Scenes", len(lines))
            with col_b:
                st.metric("Characters", total_chars)
            with col_c:
                st.metric("Est. Duration", utils.format_duration(estimated_duration))
            with col_d:
                complexity = "Simple" if len(lines) <= 5 else "Medium" if len(lines) <= 10 else "Complex"
                st.metric("Complexity", complexity)

        # Generation options
        col_gen1, col_gen2 = st.columns(2)
        
        with col_gen1:
            if st.button("🚀 Generate Video", type="primary"):
                if script_text.strip():
                    generate_video_workflow(script_text, voice_provider, scene_duration, video_quality)
                else:
                    st.error("❌ Please enter a script!")
        
        with col_gen2:
            if st.button("🎬 Preview First Scene"):
                if script_text.strip():
                    preview_first_scene(script_text, voice_provider)
                else:
                    st.error("❌ Please enter a script!")
    
    with col2:
        st.header("📊 Progress & Results")
        
        # Progress tracking
        if 'current_progress' in st.session_state:
            progress_bar = st.progress(st.session_state.current_progress)
            status_text = st.text(st.session_state.get('current_status', 'Ready'))
        
        # Results section
        if st.session_state.processing_complete and st.session_state.final_video_path:
            st.success("✅ Video generation complete!")
            
            # Video preview
            if os.path.exists(st.session_state.final_video_path):
                st.video(st.session_state.final_video_path)
                
                # Video info
                try:
                    video_info = utils.get_video_info(st.session_state.final_video_path)
                    if video_info:
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.metric("Duration", f"{video_info.get('duration', 0):.1f}s")
                        with col_info2:
                            st.metric("Size", f"{video_info.get('file_size', 0):.1f} MB")
                except:
                    pass
                
                # Download button
                with open(st.session_state.final_video_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Video",
                        data=file.read(),
                        file_name="animated_video.mp4",
                        mime="video/mp4"
                    )
                
                # Individual scene downloads
                if st.session_state.scene_files:
                    with st.expander("📁 Individual Scenes"):
                        for i, scene_file in enumerate(st.session_state.scene_files):
                            if os.path.exists(scene_file):
                                scene_name = f"Scene {i+1}"
                                with open(scene_file, "rb") as f:
                                    st.download_button(
                                        label=f"📥 {scene_name}",
                                        data=f.read(),
                                        file_name=f"scene_{i+1}.mp4",
                                        mime="video/mp4",
                                        key=f"download_scene_{i}"
                                    )

def preview_first_scene(script_text: str, voice_provider: str):
    """Preview the first scene only"""
    script_lines = utils.validate_script_lines(script_text.split('\n'))
    if not script_lines:
        st.error("No valid script lines found!")
        return
    
    first_line = script_lines[0]
    st.info(f"🎬 Previewing first scene: {first_line[:50]}...")
    
    # Initialize generators
    tts_generator = TTSGenerator(use_elevenlabs=(voice_provider == "Auto (ElevenLabs → Edge TTS)"))
    image_generator = ImageGenerator()
    
    try:
        # Generate image for first scene
        with st.spinner("🎨 Generating AI image..."):
            image_path = image_generator.generate_image(first_line, 1)
        
        # Generate audio for first scene
        with st.spinner("🎙️ Generating voice..."):
            audio_path = tts_generator.generate_speech(first_line, 1)
        
        # Show preview
        if os.path.exists(image_path):
            st.image(image_path, caption="Generated Image")
        
        if os.path.exists(audio_path):
            st.audio(audio_path, format="audio/mp3")
        
        st.success("✅ First scene preview complete!")
        
    except Exception as e:
        st.error(f"❌ Preview failed: {str(e)}")

def generate_video_workflow(script_text: str, voice_provider: str, scene_duration: int, video_quality: str):
    """Enhanced video generation workflow with better error handling"""
    # Parse script lines
    script_lines = utils.validate_script_lines(script_text.split('\n'))
    
    if not script_lines:
        st.error("No valid script lines found!")
        return
    
    # Validate script length
    if len(script_lines) > 20:
        st.warning(f"⚠️ Large script detected ({len(script_lines)} scenes). This may take 10-15 minutes.")
        if not st.checkbox("✅ I understand this will take time to process"):
            st.info("💡 Tip: Try with fewer scenes first to test the system")
            return
    
    st.info(f"Processing {len(script_lines)} scenes...")
    
    # Initialize generators
    tts_generator = TTSGenerator(use_elevenlabs=(voice_provider == "Auto (ElevenLabs → Edge TTS)"))
    image_generator = ImageGenerator()
    video_generator = VideoGenerator()
    
    # Store in session state
    st.session_state.tts_generator = tts_generator
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        scene_files = []
        failed_scenes = []
        total_steps = len(script_lines) * 3 + 1  # 3 steps per scene + final concatenation
        current_step = 0

        # Show processing statistics
        stats_container = st.container()
        
        # Processing timer
        import time
        start_time = time.time()

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
                    elapsed_time = time.time() - start_time
                    avg_time_per_scene = elapsed_time / scene_num if scene_num > 0 else 0
                    remaining_scenes = len(script_lines) - scene_num
                    estimated_remaining = remaining_scenes * avg_time_per_scene
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Completed", len(scene_files))
                    with col2:
                        st.metric("Failed", len(failed_scenes))
                    with col3:
                        st.metric("Remaining", remaining_scenes)
                    with col4:
                        st.metric("Est. Time Left", f"{estimated_remaining/60:.1f}m")

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
                st.session_state.scene_files = scene_files

                # Show final results
                status_text.text("✅ Video generation complete!")

                # Success summary
                success_count = len(scene_files)
                total_count = len(script_lines)
                total_time = time.time() - start_time

                if failed_scenes:
                    st.warning(f"⚠️ Video completed with {success_count}/{total_count} scenes. Failed scenes: {failed_scenes}")
                else:
                    st.success(f"🎉 Perfect! All {success_count} scenes completed successfully!")

                st.success(f"📁 Video saved to: {final_video_path}")
                st.info(f"⏱️ Total processing time: {total_time/60:.1f} minutes")

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

def generate_video(script_text: str, voice_provider: str, scene_duration: int):
    """Legacy function - redirects to new workflow"""
    generate_video_workflow(script_text, voice_provider, scene_duration, "Medium (720p)")

if __name__ == "__main__":
    main()
