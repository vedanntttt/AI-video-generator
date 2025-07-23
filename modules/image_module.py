"""
Enhanced Image Generation Module
Handles intelligent AI image generation using FREE Bing Image Creator (DALL-E 3)
with scene-specific prompts and perfect script-to-image matching
"""
import os
import time
import requests
import re
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import streamlit as st
import config
import utils

class ImageGenerator:
    def __init__(self):
        self.bing_usage_count = 0
        self.scene_cache = {}  # Cache for generated scenes
        self.prompt_templates = self._load_prompt_templates()
        st.success("🎨 Enhanced AI Image Generator Ready - FREE Bing Image Creator (DALL-E 3)!")

    def _load_prompt_templates(self):
        """Load intelligent prompt templates for different scene types"""
        return {
            'character_action': "Animated Disney Pixar style, {character} {action} in {setting}, vibrant colors, detailed background, cinematic lighting, high quality 3D animation",
            'location': "Beautiful animated landscape, {location}, Disney Pixar animation style, vibrant colors, detailed environment, cinematic composition, high quality digital art",
            'object_focus': "Animated scene featuring {object} in {setting}, Disney Pixar style, colorful, detailed, magical atmosphere, high quality 3D rendering",
            'emotion_scene': "Emotional animated scene, {character} feeling {emotion} in {setting}, Disney Pixar style, expressive, colorful, cinematic lighting",
            'action_scene': "Dynamic animated action scene, {action} happening in {setting}, Disney Pixar style, movement, energy, vibrant colors, detailed",
            'magical': "Magical animated scene, {elements} with glowing effects in {setting}, Disney Pixar fantasy style, sparkles, enchanted atmosphere",
            'default': "Animated Disney Pixar style scene: {description}, vibrant colors, detailed background, cinematic lighting, high quality 3D animation"
        }

    def _analyze_script_line(self, text):
        """Intelligently analyze script line to extract key elements"""
        text_lower = text.lower()

        # Extract characters
        characters = []
        character_patterns = [
            r'\b(knight|princess|dragon|unicorn|wizard|fairy|king|queen|prince|hero|warrior)\b',
            r'\b(boy|girl|man|woman|child|person|someone)\b',
            r'\b(cat|dog|bird|horse|lion|tiger|bear|wolf)\b'
        ]

        for pattern in character_patterns:
            matches = re.findall(pattern, text_lower)
            characters.extend(matches)

        # Extract actions
        actions = []
        action_patterns = [
            r'\b(walks?|runs?|flies?|jumps?|dances?|sings?|fights?|explores?|discovers?|enters?|exits?)\b',
            r'\b(looks?|sees?|finds?|takes?|gives?|holds?|carries?|throws?|catches?)\b',
            r'\b(speaks?|talks?|whispers?|shouts?|laughs?|cries?|smiles?)\b'
        ]

        for pattern in action_patterns:
            matches = re.findall(pattern, text_lower)
            actions.extend(matches)

        # Extract settings/locations
        settings = []
        setting_patterns = [
            r'\b(castle|forest|ocean|mountain|cave|village|city|palace|tower|bridge)\b',
            r'\b(garden|field|meadow|valley|river|lake|beach|desert|jungle|island)\b',
            r'\b(room|hall|chamber|kitchen|bedroom|library|dungeon|attic)\b',
            r'\b(magical?|enchanted|mysterious|dark|bright|colorful|ancient|hidden)\b'
        ]

        for pattern in setting_patterns:
            matches = re.findall(pattern, text_lower)
            settings.extend(matches)

        # Extract objects
        objects = []
        object_patterns = [
            r'\b(sword|crown|treasure|crystal|gem|book|key|door|window|tree)\b',
            r'\b(flower|star|moon|sun|cloud|rainbow|fire|water|light|shadow)\b',
            r'\b(magic|spell|potion|wand|staff|ring|necklace|chest|box)\b'
        ]

        for pattern in object_patterns:
            matches = re.findall(pattern, text_lower)
            objects.extend(matches)

        # Extract emotions
        emotions = []
        emotion_patterns = [
            r'\b(happy|sad|angry|excited|scared|brave|curious|surprised|worried|joyful)\b',
            r'\b(peaceful|calm|nervous|confident|proud|shy|amazed|delighted)\b'
        ]

        for pattern in emotion_patterns:
            matches = re.findall(pattern, text_lower)
            emotions.extend(matches)

        return {
            'characters': list(set(characters)),
            'actions': list(set(actions)),
            'settings': list(set(settings)),
            'objects': list(set(objects)),
            'emotions': list(set(emotions)),
            'original_text': text
        }

    def _generate_intelligent_prompt(self, text):
        """Generate intelligent, scene-specific prompts for DALL-E 3"""
        analysis = self._analyze_script_line(text)

        # Determine the best template based on content analysis
        template_key = 'default'
        template_vars = {'description': text}

        if analysis['characters'] and analysis['actions']:
            template_key = 'character_action'
            template_vars = {
                'character': analysis['characters'][0],
                'action': analysis['actions'][0],
                'setting': analysis['settings'][0] if analysis['settings'] else 'beautiful landscape'
            }
        elif analysis['emotions'] and analysis['characters']:
            template_key = 'emotion_scene'
            template_vars = {
                'character': analysis['characters'][0],
                'emotion': analysis['emotions'][0],
                'setting': analysis['settings'][0] if analysis['settings'] else 'peaceful environment'
            }
        elif 'magical' in text.lower() or 'magic' in text.lower() or 'crystal' in text.lower():
            template_key = 'magical'
            template_vars = {
                'elements': ', '.join(analysis['objects'][:2]) if analysis['objects'] else 'magical elements',
                'setting': analysis['settings'][0] if analysis['settings'] else 'enchanted realm'
            }
        elif analysis['actions']:
            template_key = 'action_scene'
            template_vars = {
                'action': analysis['actions'][0],
                'setting': analysis['settings'][0] if analysis['settings'] else 'dynamic environment'
            }
        elif analysis['settings']:
            template_key = 'location'
            template_vars = {
                'location': analysis['settings'][0]
            }
        elif analysis['objects']:
            template_key = 'object_focus'
            template_vars = {
                'object': analysis['objects'][0],
                'setting': analysis['settings'][0] if analysis['settings'] else 'beautiful scene'
            }

        # Generate the prompt
        try:
            prompt = self.prompt_templates[template_key].format(**template_vars)
        except KeyError:
            # Fallback to default template
            prompt = self.prompt_templates['default'].format(description=text)

        # Add quality enhancers
        quality_enhancers = [
            "masterpiece quality",
            "professional animation",
            "detailed textures",
            "perfect lighting",
            "4K resolution"
        ]

        prompt += f", {', '.join(quality_enhancers[:2])}"

        # Ensure prompt length is appropriate for DALL-E 3
        if len(prompt) > 400:
            prompt = prompt[:397] + "..."

        return prompt
    
    def generate_image(self, text: str, scene_number: int) -> str:
        """Generate optimized AI image perfectly matched to script line"""
        try:
            image_filename = utils.get_scene_filename(scene_number, "jpg")
            image_path = os.path.join(config.IMAGES_DIR, image_filename)

            # Check cache first
            cache_key = f"{text}_{scene_number}"
            if cache_key in self.scene_cache:
                st.info(f"🔄 Using cached image for scene {scene_number}")
                return self.scene_cache[cache_key]

            # Generate intelligent, scene-specific prompt
            intelligent_prompt = self._generate_intelligent_prompt(text)

            # Show enhanced Bing Image Creator instructions
            result_path = self._generate_with_enhanced_bing_instructions(
                intelligent_prompt, image_path, scene_number, text
            )

            # Cache the result
            self.scene_cache[cache_key] = result_path

            return result_path

        except Exception as e:
            st.error(f"❌ Error generating image for scene {scene_number}: {str(e)}")
            # Create fallback custom scene
            return self._generate_custom_scene(text, image_path, scene_number)

    def _create_bing_prompt(self, text: str) -> str:
        """Create an enhanced prompt for Bing Image Creator (DALL-E 3)"""
        # Add style keywords for animated/cartoon look
        style_prefix = "Animated cartoon style, vibrant colors, Disney Pixar style, high quality digital art: "

        # Clean and enhance the text
        enhanced_text = text.strip()
        if not enhanced_text.endswith('.'):
            enhanced_text += '.'

        # Combine with style
        full_prompt = style_prefix + enhanced_text

        # Ensure prompt isn't too long
        if len(full_prompt) > 400:
            full_prompt = full_prompt[:397] + "..."

        return full_prompt

    def _generate_with_enhanced_bing_instructions(self, prompt: str, output_path: str, scene_number: int, original_text: str) -> str:
        """Generate image using enhanced FREE Bing Image Creator with intelligent prompts"""

        # Update usage count
        self.bing_usage_count += 1

        # Show usage statistics
        if self.bing_usage_count <= 5:
            st.success(f"🆓 FREE AI Image Generation - Scene {scene_number} (Usage: {self.bing_usage_count})")
        elif self.bing_usage_count <= 15:
            st.info(f"🎨 Generating Scene {scene_number} - Usage: {self.bing_usage_count} images (still free!)")
        else:
            st.warning(f"⚠️ Heavy usage: {self.bing_usage_count} images. Consider daily limits.")

        # Show enhanced instructions
        with st.expander(f"🎨 AI Image Generation - Scene {scene_number}: \"{original_text[:50]}...\"", expanded=True):

            # Show analysis
            analysis = self._analyze_script_line(original_text)
            if analysis['characters'] or analysis['settings'] or analysis['objects']:
                st.markdown("**🔍 Scene Analysis:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if analysis['characters']:
                        st.markdown(f"**Characters:** {', '.join(analysis['characters'][:3])}")
                with col2:
                    if analysis['settings']:
                        st.markdown(f"**Setting:** {', '.join(analysis['settings'][:2])}")
                with col3:
                    if analysis['objects']:
                        st.markdown(f"**Elements:** {', '.join(analysis['objects'][:2])}")

            st.markdown(f"""
            **✨ Intelligent DALL-E 3 Prompt Generated:**

            **🔗 Step 1:** Go to [Bing Image Creator](https://www.bing.com/images/create) (FREE!)

            **📝 Step 2:** Copy this scene-optimized prompt:
            ```
            {prompt}
            ```

            **🎨 Step 3:**
            1. Paste the prompt and click "Create"
            2. Wait for 4 high-quality AI images
            3. Choose the image that best matches: "{original_text}"
            4. Right-click → "Save image as..." → `{os.path.basename(output_path)}`
            5. Place in the `{config.IMAGES_DIR}` folder

            **⚡ Quick Upload:** Upload your generated image below:
            """)

            uploaded_file = st.file_uploader(
                f"Upload AI image for scene {scene_number}",
                type=['png', 'jpg', 'jpeg', 'webp'],
                key=f"bing_image_upload_{scene_number}"
            )

            if uploaded_file is not None:
                # Save uploaded image
                image = Image.open(uploaded_file)
                # Resize to HD resolution
                image = image.resize(config.IMAGE_SIZE, Image.Resampling.LANCZOS)
                image.save(output_path)

                # Add centered text overlay
                self._add_text_overlay(output_path, original_text, scene_number)

                st.success(f"✅ AI image saved for scene {scene_number} with centered text!")
                return output_path

        # Check if image was manually placed
        if os.path.exists(output_path):
            # Add text overlay to manually placed image
            self._add_text_overlay(output_path, original_text, scene_number)
            st.success(f"✅ Found AI image for scene {scene_number} - Added centered text!")
            return output_path

        # Create custom scene as fallback
        st.info(f"Creating custom animated scene for scene {scene_number} (you can replace with Bing image later)")
        return self._generate_custom_scene(original_text, output_path, scene_number)

    def _add_text_overlay(self, image_path: str, text: str, scene_number: int):
        """Add perfectly centered, professional subtitle-style text overlay"""
        try:
            # Open and enhance image
            img = Image.open(image_path)

            # Enhance image quality
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)  # Slight contrast boost

            draw = ImageDraw.Draw(img)

            # Load optimal fonts with fallbacks
            text_font = self._get_optimal_font(img.width)
            scene_font = self._get_scene_font()

            # Add subtle scene number
            scene_text = f"Scene {scene_number}"
            self._draw_scene_number(draw, scene_text, scene_font)

            # Process and wrap text intelligently
            wrapped_lines = self._intelligent_text_wrap(text, text_font, img.width)

            # Calculate perfect positioning
            positioning = self._calculate_text_positioning(wrapped_lines, text_font, img.width, img.height)

            # Draw text with professional styling
            self._draw_professional_text(draw, wrapped_lines, text_font, positioning)

            # Save with optimization
            img.save(image_path, quality=95, optimize=True)

        except Exception as e:
            st.error(f"❌ Error adding text overlay: {str(e)}")
            # Fallback to simple text overlay
            self._add_simple_text_overlay(image_path, text, scene_number)

    def _get_optimal_font(self, image_width):
        """Get optimal font size based on image width"""
        base_size = max(32, min(56, image_width // 25))  # Responsive font size

        font_paths = [
            "arial.ttf", "calibri.ttf", "segoeui.ttf", "tahoma.ttf",
            "/System/Library/Fonts/Arial.ttf",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Linux
        ]

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, base_size)
            except:
                continue

        return ImageFont.load_default()

    def _get_scene_font(self):
        """Get font for scene number"""
        font_paths = ["arial.ttf", "calibri.ttf", "segoeui.ttf"]

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, 20)
            except:
                continue

        return ImageFont.load_default()

    def _draw_scene_number(self, draw, scene_text, scene_font):
        """Draw scene number with subtle styling"""
        # Semi-transparent background
        bbox = draw.textbbox((0, 0), scene_text, font=scene_font)
        padding = 8
        draw.rectangle([15, 15, bbox[2] + 30, bbox[3] + 30],
                      fill=(0, 0, 0, 120), outline=(255, 255, 255, 80))

        # Scene number text
        draw.text((23, 23), scene_text, fill=(255, 255, 255), font=scene_font)

    def _intelligent_text_wrap(self, text, font, image_width):
        """Intelligently wrap text with proper line breaks"""
        max_width = image_width - 120  # Generous margins
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)

            if bbox[2] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Word too long, force break
                    lines.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def _calculate_text_positioning(self, lines, font, image_width, image_height):
        """Calculate optimal text positioning"""
        line_height = font.getbbox("Ay")[3] + 15  # Dynamic line height
        total_height = len(lines) * line_height - 5

        # Center vertically
        start_y = (image_height - total_height) // 2

        return {
            'start_y': start_y,
            'line_height': line_height,
            'image_width': image_width
        }

    def _draw_professional_text(self, draw, lines, font, positioning):
        """Draw text with professional movie-style subtitles"""
        for i, line in enumerate(lines):
            # Calculate center position for this line
            bbox = draw.textbbox((0, 0), line, font=font)
            line_x = (positioning['image_width'] - bbox[2]) // 2
            line_y = positioning['start_y'] + (i * positioning['line_height'])

            # Professional shadow effect (multiple layers)
            shadow_offsets = [(3, 3), (2, 2), (4, 4)]
            for offset_x, offset_y in shadow_offsets:
                draw.text((line_x + offset_x, line_y + offset_y), line,
                         fill=(0, 0, 0), font=font)

            # Main text (crisp white)
            draw.text((line_x, line_y), line, fill=(255, 255, 255), font=font)

    def _add_simple_text_overlay(self, image_path: str, text: str, scene_number: int):
        """Fallback simple text overlay"""
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()

            # Simple centered text
            bbox = draw.textbbox((0, 0), text, font=font)
            x = (img.width - bbox[2]) // 2
            y = (img.height - bbox[3]) // 2

            # Shadow and text
            draw.text((x + 2, y + 2), text, fill=(0, 0, 0), font=font)
            draw.text((x, y), text, fill=(255, 255, 255), font=font)

            img.save(image_path)
        except Exception as e:
            st.error(f"❌ Fallback text overlay failed: {str(e)}")

    def _generate_custom_scene(self, text: str, output_path: str, scene_number: int) -> str:
        """Generate custom animated scene as fallback"""
        st.info(f"🎨 Creating custom animated scene for scene {scene_number}...")

        # Create the custom scene image
        img = self._create_placeholder_image(text, scene_number)
        img.save(output_path)

        return output_path
    
    def _enhance_prompt(self, text: str) -> str:
        """Enhance the text prompt for better image generation"""
        # Add style keywords for animated/cartoon look
        style_keywords = config.IMAGE_STYLE_PROMPT
        enhanced = f"{text}, {style_keywords}"
        
        # Limit prompt length (Bing has character limits)
        if len(enhanced) > 200:
            enhanced = enhanced[:197] + "..."
        
        return enhanced
    
    def _generate_automated(self, prompt: str, output_path: str, scene_number: int) -> str:
        """Attempt automated image generation (experimental)"""
        # This is a placeholder for potential automation
        # For now, we'll create a simple placeholder image
        st.info(f"🎨 Generating image for scene {scene_number}...")
        
        # Create a placeholder image with the prompt text
        # In a real implementation, you might use:
        # - Selenium to automate Bing Image Creator
        # - Alternative free APIs like Hugging Face Diffusers
        # - Local Stable Diffusion models
        
        placeholder_image = self._create_placeholder_image(prompt, scene_number)
        placeholder_image.save(output_path)
        
        return output_path
    
    def _create_placeholder_image(self, prompt: str, scene_number: int) -> Image.Image:
        """Create an animated-style scene image with clean centered subtitle text"""
        import random

        # Create image with video resolution
        img = Image.new('RGB', config.IMAGE_SIZE)
        draw = ImageDraw.Draw(img)

        # Create animated scene background with visual elements
        self._draw_animated_scene(img, draw, prompt)

        # Try to use better fonts
        try:
            text_font = ImageFont.truetype("arial.ttf", 48)
            scene_font = ImageFont.truetype("arial.ttf", 24)
        except:
            try:
                text_font = ImageFont.truetype("calibri.ttf", 48)
                scene_font = ImageFont.truetype("calibri.ttf", 24)
            except:
                text_font = ImageFont.load_default()
                scene_font = ImageFont.load_default()

        # Add scene number in corner (clean, no background)
        scene_text = f"Scene {scene_number}"
        draw.text((20, 20), scene_text, fill=(255, 255, 255), font=scene_font)

        # Add clean centered subtitle text
        wrapped_lines = self._wrap_text(prompt, text_font, config.IMAGE_SIZE[0] - 100)

        # Calculate perfect center position
        line_height = 60
        total_text_height = len(wrapped_lines) * line_height - 10
        center_y = (config.IMAGE_SIZE[1] - total_text_height) // 2

        # Draw each line perfectly centered with clean subtitle style
        for i, line in enumerate(wrapped_lines):
            line_bbox = draw.textbbox((0, 0), line, font=text_font)
            line_x = (config.IMAGE_SIZE[0] - line_bbox[2]) // 2
            line_y = center_y + (i * line_height)

            # Add text with strong shadow for maximum readability (subtitle style)
            shadow_offset = 4
            # Multiple shadow layers for better contrast
            draw.text((line_x + shadow_offset, line_y + shadow_offset), line, fill=(0, 0, 0), font=text_font)
            draw.text((line_x + shadow_offset-1, line_y + shadow_offset-1), line, fill=(0, 0, 0), font=text_font)
            draw.text((line_x + shadow_offset+1, line_y + shadow_offset+1), line, fill=(0, 0, 0), font=text_font)

            # Main white text
            draw.text((line_x, line_y), line, fill=(255, 255, 255), font=text_font)

        return img

    def _get_scene_colors(self, prompt: str) -> tuple:
        """Get appropriate colors based on scene content"""
        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in ['forest', 'tree', 'nature', 'garden', 'unicorn']):
            return ((20, 100, 20), (50, 200, 50))  # Vibrant forest green
        elif any(word in prompt_lower for word in ['ocean', 'sea', 'water', 'underwater']):
            return ((0, 50, 100), (0, 150, 255))  # Deep ocean blue
        elif any(word in prompt_lower for word in ['space', 'star', 'galaxy', 'planet', 'alien']):
            return ((20, 0, 60), (80, 20, 120))  # Deep space purple
        elif any(word in prompt_lower for word in ['fire', 'flame', 'dragon', 'volcano']):
            return ((100, 0, 0), (255, 100, 0))  # Bright fire colors
        elif any(word in prompt_lower for word in ['castle', 'knight', 'dark', 'mysterious']):
            return ((40, 40, 60), (80, 80, 100))  # Dark castle theme
        elif any(word in prompt_lower for word in ['crystal', 'magic', 'glowing', 'magical']):
            return ((60, 0, 100), (120, 50, 200))  # Magical purple
        elif any(word in prompt_lower for word in ['treasure', 'gold', 'golden']):
            return ((100, 80, 0), (255, 215, 0))  # Golden treasure
        elif any(word in prompt_lower for word in ['ice', 'snow', 'winter', 'frozen']):
            return ((100, 150, 200), (200, 230, 255))  # Ice blue
        elif any(word in prompt_lower for word in ['desert', 'sand', 'dune']):
            return ((150, 100, 50), (255, 200, 100))  # Desert sand
        else:
            return ((50, 100, 200), (100, 200, 255))  # Bright sky blue

    def _draw_animated_scene(self, img: Image.Image, draw: ImageDraw.Draw, prompt: str):
        """Draw an animated-style scene with visual elements based on the story"""
        import random

        prompt_lower = prompt.lower()
        width, height = config.IMAGE_SIZE

        # Draw sky/background
        if any(word in prompt_lower for word in ['castle', 'knight', 'dark', 'mysterious']):
            # Dark castle scene
            self._draw_castle_scene(draw, width, height)
        elif any(word in prompt_lower for word in ['forest', 'tree', 'unicorn', 'magical']):
            # Magical forest scene
            self._draw_forest_scene(draw, width, height)
        elif any(word in prompt_lower for word in ['ocean', 'sea', 'underwater', 'fish']):
            # Ocean scene
            self._draw_ocean_scene(draw, width, height)
        elif any(word in prompt_lower for word in ['space', 'planet', 'alien', 'spaceship']):
            # Space scene
            self._draw_space_scene(draw, width, height)
        elif any(word in prompt_lower for word in ['crystal', 'treasure', 'gold', 'glowing']):
            # Treasure/crystal scene
            self._draw_treasure_scene(draw, width, height)
        else:
            # Default fantasy scene
            self._draw_default_scene(draw, width, height)

    def _draw_castle_scene(self, draw: ImageDraw.Draw, width: int, height: int):
        """Draw a dark castle scene"""
        # Dark sky gradient
        for y in range(height // 2):
            ratio = y / (height // 2)
            color = (int(20 + ratio * 40), int(20 + ratio * 40), int(60 + ratio * 40))
            draw.line([(0, y), (width, y)], fill=color)

        # Ground
        for y in range(height // 2, height):
            draw.line([(0, y), (width, y)], fill=(40, 60, 40))

        # Castle silhouette
        castle_points = [
            (width//4, height//2), (width//4, height//3), (width//3, height//3),
            (width//3, height//4), (width*2//3, height//4), (width*2//3, height//3),
            (width*3//4, height//3), (width*3//4, height//2)
        ]
        draw.polygon(castle_points, fill=(30, 30, 30))

        # Castle towers
        draw.rectangle([width//4-20, height//4, width//4+20, height//2], fill=(25, 25, 25))
        draw.rectangle([width*3//4-20, height//4, width*3//4+20, height//2], fill=(25, 25, 25))

        # Windows (glowing)
        for i in range(3):
            x = width//4 + i * 100
            y = height//3 + 20
            draw.rectangle([x, y, x+15, y+20], fill=(255, 255, 100))

    def _draw_forest_scene(self, draw: ImageDraw.Draw, width: int, height: int):
        """Draw a magical forest scene"""
        # Sky gradient
        for y in range(height // 2):
            ratio = y / (height // 2)
            color = (int(100 + ratio * 50), int(150 + ratio * 50), int(255 - ratio * 50))
            draw.line([(0, y), (width, y)], fill=color)

        # Ground
        for y in range(height // 2, height):
            draw.line([(0, y), (width, y)], fill=(34, 139, 34))

        # Trees
        import random
        for i in range(5):
            x = random.randint(50, width-50)
            tree_height = random.randint(100, 200)
            # Tree trunk
            draw.rectangle([x-10, height//2, x+10, height//2 + tree_height//3], fill=(101, 67, 33))
            # Tree crown
            draw.ellipse([x-40, height//2 - tree_height//2, x+40, height//2 + tree_height//4], fill=(0, 128, 0))

        # Magical sparkles
        for i in range(10):
            x = random.randint(0, width)
            y = random.randint(0, height//2)
            draw.ellipse([x-3, y-3, x+3, y+3], fill=(255, 255, 100))

    def _draw_ocean_scene(self, draw: ImageDraw.Draw, width: int, height: int):
        """Draw an ocean scene"""
        # Ocean gradient
        for y in range(height):
            ratio = y / height
            color = (int(0 + ratio * 50), int(100 + ratio * 50), int(200 + ratio * 55))
            draw.line([(0, y), (width, y)], fill=color)

        # Waves
        import math
        for wave in range(3):
            y_base = height // 3 + wave * 50
            for x in range(0, width, 10):
                wave_y = y_base + int(20 * math.sin(x * 0.02 + wave))
                draw.ellipse([x-5, wave_y-5, x+5, wave_y+5], fill=(255, 255, 255, 100))

        # Fish
        import random
        for i in range(5):
            x = random.randint(50, width-50)
            y = random.randint(height//3, height-50)
            # Simple fish shape
            draw.ellipse([x-15, y-8, x+15, y+8], fill=(255, 165, 0))
            draw.polygon([(x+15, y), (x+25, y-5), (x+25, y+5)], fill=(255, 140, 0))

    def _draw_space_scene(self, draw: ImageDraw.Draw, width: int, height: int):
        """Draw a space scene"""
        # Space background
        for y in range(height):
            draw.line([(0, y), (width, y)], fill=(10, 10, 30))

        # Stars
        import random
        for i in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            draw.ellipse([x-size, y-size, x+size, y+size], fill=(255, 255, 255))

        # Planet
        planet_x, planet_y = width//4, height//3
        draw.ellipse([planet_x-60, planet_y-60, planet_x+60, planet_y+60], fill=(150, 100, 200))

        # Spaceship
        ship_x, ship_y = width*3//4, height*2//3
        draw.ellipse([ship_x-30, ship_y-10, ship_x+30, ship_y+10], fill=(200, 200, 200))
        draw.polygon([(ship_x-30, ship_y), (ship_x-40, ship_y-5), (ship_x-40, ship_y+5)], fill=(150, 150, 150))

    def _draw_treasure_scene(self, draw: ImageDraw.Draw, width: int, height: int):
        """Draw a treasure/crystal scene"""
        # Cave background
        for y in range(height):
            ratio = y / height
            color = (int(60 + ratio * 40), int(40 + ratio * 30), int(80 + ratio * 40))
            draw.line([(0, y), (width, y)], fill=color)

        # Treasure chest
        chest_x, chest_y = width//2, height*2//3
        draw.rectangle([chest_x-40, chest_y-20, chest_x+40, chest_y+20], fill=(139, 69, 19))
        draw.rectangle([chest_x-35, chest_y-15, chest_x+35, chest_y-5], fill=(255, 215, 0))

        # Glowing crystals
        import random
        for i in range(8):
            x = random.randint(50, width-50)
            y = random.randint(height//2, height-50)
            crystal_height = random.randint(20, 40)
            # Crystal shape
            points = [(x, y-crystal_height), (x-10, y), (x+10, y)]
            draw.polygon(points, fill=(100, 255, 255))
            # Glow effect
            draw.ellipse([x-15, y-5, x+15, y+5], fill=(200, 255, 255, 50))

    def _draw_default_scene(self, draw: ImageDraw.Draw, width: int, height: int):
        """Draw a default fantasy scene"""
        # Sky gradient
        for y in range(height // 2):
            ratio = y / (height // 2)
            color = (int(135 + ratio * 50), int(206 + ratio * 49), int(235 + ratio * 20))
            draw.line([(0, y), (width, y)], fill=color)

        # Ground
        for y in range(height // 2, height):
            draw.line([(0, y), (width, y)], fill=(34, 139, 34))

        # Simple landscape elements
        # Hills
        import random
        for i in range(3):
            hill_x = i * width // 3
            hill_points = [(hill_x, height//2), (hill_x + width//6, height//3), (hill_x + width//3, height//2)]
            draw.polygon(hill_points, fill=(0, 100, 0))

        # Sun
        sun_x, sun_y = width - 100, 80
        draw.ellipse([sun_x-30, sun_y-30, sun_x+30, sun_y+30], fill=(255, 255, 0))

    def _wrap_text(self, text: str, font, max_width: int) -> list:
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            # Test if adding this word would exceed width
            test_line = ' '.join(current_line + [word])
            bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), test_line, font=font)

            if bbox[2] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word is too long, add it anyway
                    lines.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        return lines[:4]  # Limit to 4 lines max

    def _extract_key_words(self, prompt: str) -> list:
        """Extract key visual words from prompt"""
        # Common words to ignore
        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}

        words = prompt.lower().replace(',', '').replace('.', '').split()
        key_words = [word for word in words if word not in stop_words and len(word) > 2]
        return key_words[:5]  # Return top 5 key words

    def _add_decorative_elements(self, draw: ImageDraw.Draw, prompt: str):
        """Add simple decorative elements based on content"""
        prompt_lower = prompt.lower()

        # Add stars for space scenes
        if any(word in prompt_lower for word in ['space', 'star', 'galaxy', 'night']):
            import random
            for _ in range(20):
                x = random.randint(0, config.IMAGE_SIZE[0])
                y = random.randint(0, config.IMAGE_SIZE[1] // 2)
                size = random.randint(2, 4)
                draw.ellipse([x-size, y-size, x+size, y+size], fill=(255, 255, 255))

        # Add simple shapes for other scenes
        elif any(word in prompt_lower for word in ['sun', 'sunny', 'bright']):
            # Draw sun
            sun_x, sun_y = config.IMAGE_SIZE[0] - 100, 80
            draw.ellipse([sun_x-30, sun_y-30, sun_x+30, sun_y+30], fill=(255, 255, 0))

        elif any(word in prompt_lower for word in ['mountain', 'hill']):
            # Draw simple mountains
            points = [(0, config.IMAGE_SIZE[1]), (200, config.IMAGE_SIZE[1]//2), (400, config.IMAGE_SIZE[1])]
            draw.polygon(points, fill=(139, 69, 19))
    
    def _generate_manual_fallback(self, prompt: str, output_path: str, scene_number: int) -> str:
        """Fallback to manual image generation instructions"""
        st.warning(f"🎨 Manual image generation required for scene {scene_number}")
        
        # Show instructions to user
        with st.expander(f"📋 Manual Image Generation Instructions - Scene {scene_number}", expanded=True):
            st.markdown(f"""
            **Prompt for Bing Image Creator:**
            ```
            {prompt}
            ```
            
            **Steps:**
            1. Go to [Bing Image Creator](https://www.bing.com/images/create)
            2. Copy the prompt above
            3. Generate the image
            4. Download the best image
            5. Save it as: `{os.path.basename(output_path)}`
            6. Place it in the `{config.IMAGES_DIR}` folder
            
            **Alternative:** Upload your own image below:
            """)
            
            uploaded_file = st.file_uploader(
                f"Upload image for scene {scene_number}",
                type=['png', 'jpg', 'jpeg', 'webp'],
                key=f"image_upload_{scene_number}"
            )
            
            if uploaded_file is not None:
                # Save uploaded image
                image = Image.open(uploaded_file)
                # Resize to match video resolution
                image = image.resize(config.IMAGE_SIZE, Image.Resampling.LANCZOS)
                image.save(output_path)
                st.success(f"✅ Image saved for scene {scene_number}")
                return output_path
        
        # Check if image was manually placed
        if os.path.exists(output_path):
            st.success(f"✅ Found image for scene {scene_number}")
            return output_path
        
        # Create placeholder if no image provided
        st.info(f"Creating placeholder image for scene {scene_number}")
        placeholder_image = self._create_placeholder_image(prompt, scene_number)
        placeholder_image.save(output_path)
        
        return output_path
    
    def validate_image(self, image_path: str) -> bool:
        """Validate that the image file is valid and properly formatted"""
        try:
            with Image.open(image_path) as img:
                # Check if image can be opened
                img.verify()
                return True
        except Exception:
            return False
    
    def resize_image(self, image_path: str) -> str:
        """Resize image to match video resolution"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to video resolution
                img = img.resize(config.IMAGE_SIZE, Image.Resampling.LANCZOS)
                img.save(image_path)
                
            return image_path
        except Exception as e:
            st.error(f"Error resizing image: {str(e)}")
            raise
