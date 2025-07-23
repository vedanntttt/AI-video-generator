"""
Text-to-Speech Module
Handles voice generation using ElevenLabs API (primary) and Edge TTS (fallback)
"""
import os
import asyncio
import edge_tts
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import VoiceSettings
    ELEVENLABS_AVAILABLE = True
except ImportError:
    try:
        from elevenlabs import generate, save, set_api_key, get_api_key
        from elevenlabs.api.error import UnauthenticatedRateLimitError, AuthorizationError
        ELEVENLABS_AVAILABLE = True
    except ImportError:
        ELEVENLABS_AVAILABLE = False
import config
import utils
import streamlit as st

class TTSGenerator:
    def __init__(self, use_elevenlabs: bool = True):
        self.use_elevenlabs = use_elevenlabs
        self.elevenlabs_available = False
        self.character_count = 0
        self.elevenlabs_client = None

        # Initialize ElevenLabs if API key is available
        if self.use_elevenlabs and config.ELEVENLABS_API_KEY and ELEVENLABS_AVAILABLE:
            try:
                # Try new API first
                self.elevenlabs_client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
                self.elevenlabs_available = True
                st.info("✅ ElevenLabs API initialized successfully")
            except Exception as e:
                try:
                    # Fallback to old API
                    set_api_key(config.ELEVENLABS_API_KEY)
                    get_api_key()
                    self.elevenlabs_available = True
                    st.info("✅ ElevenLabs API initialized successfully (legacy)")
                except Exception as e2:
                    st.warning(f"⚠️ ElevenLabs API not available: {str(e)}. Using Edge TTS instead.")
                    self.elevenlabs_available = False
        else:
            st.info("🔊 Using Edge TTS for voice generation")
    
    def generate_speech(self, text: str, scene_number: int) -> str:
        """Generate speech audio for given text"""
        audio_filename = utils.get_scene_filename(scene_number, "mp3")
        audio_path = os.path.join(config.AUDIO_DIR, audio_filename)
        
        # Try ElevenLabs first if available
        if self.elevenlabs_available and self._can_use_elevenlabs(text):
            try:
                return self._generate_elevenlabs_speech(text, audio_path)
            except Exception as e:
                st.warning(f"ElevenLabs failed for scene {scene_number}: {str(e)}. Falling back to Edge TTS.")
        
        # Fallback to Edge TTS
        return self._generate_edge_tts_speech(text, audio_path)
    
    def _can_use_elevenlabs(self, text: str) -> bool:
        """Check if we can use ElevenLabs based on character limit"""
        text_length = len(text)
        if self.character_count + text_length > config.ELEVENLABS_FREE_CHAR_LIMIT:
            st.warning(f"⚠️ ElevenLabs character limit reached ({config.ELEVENLABS_FREE_CHAR_LIMIT}). Using Edge TTS.")
            return False
        return True
    
    def _generate_elevenlabs_speech(self, text: str, output_path: str) -> str:
        """Generate speech using ElevenLabs API"""
        try:
            if self.elevenlabs_client:
                # Use new API
                audio = self.elevenlabs_client.generate(
                    text=text,
                    voice="Rachel",
                    model="eleven_monolingual_v1"
                )

                # Save the audio file
                with open(output_path, "wb") as f:
                    for chunk in audio:
                        f.write(chunk)
            else:
                # Use old API
                audio = generate(
                    text=text,
                    voice="Rachel",
                    model="eleven_monolingual_v1"
                )
                save(audio, output_path)

            # Update character count
            self.character_count += len(text)

            return output_path

        except Exception as e:
            if "rate limit" in str(e).lower():
                st.warning("⚠️ ElevenLabs rate limit reached. Switching to Edge TTS.")
                self.elevenlabs_available = False
            st.error(f"ElevenLabs error: {str(e)}")
            raise
    
    def _generate_edge_tts_speech(self, text: str, output_path: str) -> str:
        """Generate speech using Edge TTS (free)"""
        try:
            # Run Edge TTS asynchronously
            asyncio.run(self._edge_tts_async(text, output_path))
            return output_path
        except Exception as e:
            st.error(f"Edge TTS error: {str(e)}")
            raise
    
    async def _edge_tts_async(self, text: str, output_path: str):
        """Async function for Edge TTS"""
        # Available voices: en-US-AriaNeural, en-US-JennyNeural, en-US-GuyNeural, etc.
        voice = "en-US-AriaNeural"
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
    
    def get_character_usage(self) -> dict:
        """Get current character usage for ElevenLabs"""
        return {
            "used": self.character_count,
            "limit": config.ELEVENLABS_FREE_CHAR_LIMIT,
            "remaining": config.ELEVENLABS_FREE_CHAR_LIMIT - self.character_count
        }
