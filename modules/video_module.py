"""
Video Generation Module
Handles creation of individual scene videos and final video concatenation using MoviePy
"""
import os
import time
from typing import List
from moviepy import (
    ImageClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, TextClip, CompositeAudioClip,
    VideoFileClip, ColorClip
)
import streamlit as st
import config
import utils

class VideoGenerator:
    def __init__(self):
        self.temp_clips = []  # Keep track of clips for cleanup
        self.processing_stats = {'scenes_created': 0, 'total_duration': 0, 'errors': 0}
        self.memory_cleanup_threshold = 5  # Clean memory every 5 scenes

        # Verify system capabilities
        try:
            from moviepy.config import check_for_imageio_ffmpeg
            check_for_imageio_ffmpeg()
            st.success("🎬 Optimized Video Generator Ready!")
        except Exception as e:
            st.warning(f"⚠️ FFmpeg optimization unavailable: {str(e)}")
            st.info("💡 Video generation will use fallback encoding")
    
    def create_scene(self, image_path: str, audio_path: str, scene_number: int, min_duration: int = None) -> str:
        """Create a video scene from image and audio (text is already in the image)"""
        if min_duration is None:
            min_duration = config.DEFAULT_SCENE_DURATION

        scene_filename = utils.get_scene_filename(scene_number, "mp4")
        scene_path = os.path.join(config.SCENES_DIR, scene_filename)

        try:
            # Load audio to get duration
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration

            # Use the longer of audio duration or minimum duration
            video_duration = max(audio_duration, min_duration)

            # Create image clip with proper sizing to avoid blur
            image_clip = ImageClip(image_path, duration=video_duration)

            # Properly resize image to match video resolution without distortion
            image_clip = self._resize_image_properly(image_clip, config.VIDEO_RESOLUTION)

            # Remove zoom effect to prevent blur - keep image static and sharp

            # Use only the image clip (text is already in the image)
            final_video_clip = image_clip

            # Combine with audio
            final_clip = final_video_clip.with_audio(audio_clip)

            # Write video file with balanced quality and speed settings
            final_clip.write_videofile(
                scene_path,
                fps=config.VIDEO_FPS,
                preset='medium',  # Better quality than ultrafast
                codec='libx264',
                bitrate='1500k',  # Higher bitrate for better quality
                threads=4
            )

            # Clean up clips
            audio_clip.close()
            image_clip.close()
            final_video_clip.close()
            final_clip.close()

            return scene_path

        except Exception as e:
            self.processing_stats['errors'] += 1
            st.error(f"❌ Error creating scene {scene_number}: {str(e)}")
            # Attempt cleanup even on error
            try:
                if 'audio_clip' in locals() and audio_clip:
                    audio_clip.close()
                if 'image_clip' in locals() and image_clip:
                    image_clip.close()
                if 'final_clip' in locals() and final_clip:
                    final_clip.close()
            except:
                pass
            raise

        finally:
            # Update statistics
            self.processing_stats['scenes_created'] += 1

            # Periodic memory cleanup
            if self.processing_stats['scenes_created'] % self.memory_cleanup_threshold == 0:
                self._perform_memory_cleanup()

    def _get_optimal_encoding_params(self, scene_number):
        """Get optimal encoding parameters based on scene number and system"""
        base_params = {
            'fps': config.VIDEO_FPS,
            'codec': 'libx264',
            'threads': 4,
            'verbose': False,
            'logger': None
        }

        # Adjust quality based on scene number (first few scenes get higher quality)
        if scene_number <= 3:
            base_params.update({
                'preset': 'medium',
                'bitrate': '2000k'
            })
        else:
            base_params.update({
                'preset': 'fast',
                'bitrate': '1500k'
            })

        return base_params

    def _cleanup_clips(self, clips):
        """Safely cleanup video clips"""
        for clip in clips:
            if clip is not None:
                try:
                    clip.close()
                except Exception as e:
                    st.warning(f"⚠️ Clip cleanup warning: {str(e)}")

    def _perform_memory_cleanup(self):
        """Perform garbage collection and memory cleanup"""
        import gc
        gc.collect()
        st.info(f"🧹 Memory cleanup performed after {self.processing_stats['scenes_created']} scenes")

    def _resize_image_properly(self, image_clip, target_resolution):
        """Resize image properly to avoid blur and maintain aspect ratio"""
        # Get original dimensions
        original_size = image_clip.size
        target_width, target_height = target_resolution

        # Calculate aspect ratios
        original_ratio = original_size[0] / original_size[1]
        target_ratio = target_width / target_height

        if original_ratio > target_ratio:
            # Image is wider, fit to width
            new_width = target_width
            new_height = int(target_width / original_ratio)
        else:
            # Image is taller, fit to height
            new_height = target_height
            new_width = int(target_height * original_ratio)

        # Resize and center
        resized_clip = image_clip.resized((new_width, new_height))

        # If the resized image doesn't fill the target, add black bars
        if new_width != target_width or new_height != target_height:
            # Create black background
            black_bg = ColorClip(size=target_resolution, color=(0, 0, 0), duration=image_clip.duration)
            # Center the resized image on the black background
            resized_clip = CompositeVideoClip([
                black_bg,
                resized_clip.with_position('center')
            ])

        return resized_clip

    def _create_subtitle_clip(self, text: str, duration: float):
        """Create a centered subtitle clip with proper text wrapping"""
        try:
            # Wrap text to fit screen width (approximate)
            wrapped_text = self._wrap_subtitle_text(text, max_chars_per_line=50)

            # Create text clip with MoviePy 2.x compatible parameters
            subtitle = TextClip(
                text=wrapped_text,
                font_size=28,  # Slightly smaller for wrapped text
                color='white',
                font='Arial',
                stroke_color='black',
                stroke_width=2
            ).with_duration(duration)

            # Position at bottom center with margin
            subtitle = subtitle.with_position(('center', 0.85))  # 85% down from top

            return subtitle

        except Exception as e:
            # Fallback to even simpler text
            st.warning(f"Using basic subtitle due to: {str(e)}")
            try:
                # Try with wrapped text but simpler formatting
                wrapped_text = self._wrap_subtitle_text(text, max_chars_per_line=40)
                return TextClip(
                    text=wrapped_text,
                    font_size=24,
                    color='white'
                ).with_duration(duration).with_position('center')
            except Exception as e2:
                # Last resort - no subtitles
                st.warning(f"Could not create subtitles: {str(e2)}")
                return None

    def _wrap_subtitle_text(self, text: str, max_chars_per_line: int = 50) -> str:
        """Wrap subtitle text to multiple lines"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            # Check if adding this word would exceed the line length
            if current_length + len(word) + 1 <= max_chars_per_line:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word)
                else:
                    # Single word is too long, add it anyway
                    lines.append(word)
                    current_length = 0

        if current_line:
            lines.append(' '.join(current_line))

        # Join lines with newline characters
        return '\n'.join(lines[:3])  # Limit to 3 lines max
    
    def concatenate_scenes(self, scene_paths: List[str]) -> str:
        """Concatenate all scene videos into final video"""
        output_filename = f"final_video_{int(time.time())}.mp4"
        output_path = os.path.join(config.OUTPUT_DIR, output_filename)
        
        try:
            # Load all scene clips
            clips = []
            for scene_path in scene_paths:
                if os.path.exists(scene_path):
                    clip = VideoFileClip(scene_path)
                    clips.append(clip)
                else:
                    st.warning(f"Scene file not found: {scene_path}")
            
            if not clips:
                raise ValueError("No valid scene clips found")
            
            # Concatenate clips
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Add fade transitions between scenes
            final_video = self._add_transitions(final_video, clips)
            
            # Write final video with quality optimization
            final_video.write_videofile(
                output_path,
                fps=config.VIDEO_FPS,
                preset='medium',  # Better quality
                codec='libx264',
                bitrate='2000k',  # Higher bitrate for final video
                threads=4
            )
            
            # Clean up clips
            for clip in clips:
                clip.close()
            final_video.close()
            
            return output_path
            
        except Exception as e:
            st.error(f"Error concatenating scenes: {str(e)}")
            raise
    
    def _add_transitions(self, final_video, clips):
        """Add smooth transitions between scenes"""
        try:
            # For now, return the video as-is
            # You can implement fade transitions here if needed
            return final_video
        except Exception:
            # If transitions fail, return original video
            return final_video
    
    def create_title_scene(self, title: str, duration: int = 3) -> str:
        """Create a title scene for the video"""
        title_path = os.path.join(config.SCENES_DIR, "title_scene.mp4")
        
        try:
            # Create text clip
            title_clip = TextClip(
                title,
                fontsize=60,
                color='white',
                font='Arial-Bold',
                size=config.VIDEO_RESOLUTION
            ).set_duration(duration)
            
            # Create background
            bg_clip = ColorClip(
                size=config.VIDEO_RESOLUTION,
                color=(0, 0, 0),
                duration=duration
            )
            
            # Composite title over background
            final_clip = CompositeVideoClip([bg_clip, title_clip])
            
            # Write video
            final_clip.write_videofile(
                title_path,
                fps=config.VIDEO_FPS,
                codec='libx264',
                verbose=False,
                logger=None
            )
            
            # Clean up
            title_clip.close()
            bg_clip.close()
            final_clip.close()
            
            return title_path
            
        except Exception as e:
            st.warning(f"Could not create title scene: {str(e)}")
            return None
    
    def get_video_info(self, video_path: str) -> dict:
        """Get information about a video file"""
        try:
            from moviepy.editor import VideoFileClip
            
            with VideoFileClip(video_path) as clip:
                return {
                    'duration': clip.duration,
                    'fps': clip.fps,
                    'size': clip.size,
                    'has_audio': clip.audio is not None
                }
        except Exception as e:
            st.error(f"Error getting video info: {str(e)}")
            return {}
    
    def cleanup_temp_files(self):
        """Clean up temporary video files"""
        for clip in self.temp_clips:
            try:
                clip.close()
            except:
                pass
        self.temp_clips.clear()
