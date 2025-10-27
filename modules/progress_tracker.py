"""
Progress Tracking Module
Provides real-time progress updates during video generation
"""
import streamlit as st
import time
from typing import Dict, Any

class ProgressTracker:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all progress tracking"""
        self.current_step = 0
        self.total_steps = 0
        self.step_details = {}
        self.start_time = None
        self.step_start_time = None
        
    def initialize(self, total_scenes: int):
        """Initialize progress tracking for a video generation job"""
        self.reset()
        self.total_steps = total_scenes * 3 + 2  # TTS + Image + Scene per scene + Final assembly + Cleanup
        self.start_time = time.time()
        
        # Initialize progress containers
        if 'progress_container' not in st.session_state:
            st.session_state.progress_container = st.empty()
        if 'status_container' not in st.session_state:
            st.session_state.status_container = st.empty()
    
    def start_step(self, step_name: str, details: str = ""):
        """Start a new step in the process"""
        self.current_step += 1
        self.step_start_time = time.time()
        
        progress = self.current_step / self.total_steps
        
        # Update progress bar
        if 'progress_container' in st.session_state:
            st.session_state.progress_container.progress(
                progress, 
                text=f"Step {self.current_step}/{self.total_steps}: {step_name}"
            )
        
        # Update status
        if 'status_container' in st.session_state:
            elapsed = time.time() - self.start_time if self.start_time else 0
            eta = (elapsed / progress * (1 - progress)) if progress > 0 else 0
            
            status_text = f"""
            **Current Step:** {step_name}
            **Details:** {details}
            **Progress:** {self.current_step}/{self.total_steps} ({progress*100:.1f}%)
            **Elapsed Time:** {self._format_time(elapsed)}
            **Estimated Remaining:** {self._format_time(eta)}
            """
            st.session_state.status_container.info(status_text)
    
    def complete_step(self, success: bool = True, message: str = ""):
        """Mark current step as complete"""
        if self.step_start_time:
            step_duration = time.time() - self.step_start_time
            self.step_details[self.current_step] = {
                'duration': step_duration,
                'success': success,
                'message': message
            }
    
    def finish(self, success: bool = True):
        """Finish the entire process"""
        total_time = time.time() - self.start_time if self.start_time else 0
        
        if success:
            if 'status_container' in st.session_state:
                st.session_state.status_container.success(
                    f"✅ Video generation completed successfully!\n"
                    f"Total time: {self._format_time(total_time)}"
                )
            if 'progress_container' in st.session_state:
                st.session_state.progress_container.progress(1.0, text="✅ Complete!")
        else:
            if 'status_container' in st.session_state:
                st.session_state.status_container.error(
                    f"❌ Video generation failed.\n"
                    f"Time elapsed: {self._format_time(total_time)}"
                )
    
    def _format_time(self, seconds: float) -> str:
        """Format time in a human-readable way"""
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current progress statistics"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        progress = self.current_step / self.total_steps if self.total_steps > 0 else 0
        
        return {
            'current_step': self.current_step,
            'total_steps': self.total_steps,
            'progress_percent': progress * 100,
            'elapsed_time': elapsed,
            'estimated_total': elapsed / progress if progress > 0 else 0,
            'step_details': self.step_details
        }