"""
Standalone AI Art Generator for MC AI
NO external APIs - completely self-contained
Uses PIL, numpy, and mathematical algorithms for art generation
NOW WITH PROMPT-AWARE GENERATION!
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
from PIL.Image import Image as PILImage
from typing import Dict, List, Optional, Tuple
import random
import math
from datetime import datetime
import colorsys
import re

class StandaloneArtGenerator:
    """
    Self-contained art generation system
    Creates unique images based on prompts, emotions, and styles
    NOW INTERPRETS PROMPTS FOR RELEVANT IMAGERY!
    """
    
    def __init__(self):
        self.output_path = "static/generated_art"
        os.makedirs(self.output_path, exist_ok=True)
        
        # Color palettes for emotions
        self.emotion_colors = {
            'joy': [(255, 223, 0), (255, 165, 0), (255, 105, 180), (255, 192, 203)],
            'calm': [(173, 216, 230), (176, 224, 230), (135, 206, 235), (100, 149, 237)],
            'energy': [(255, 0, 0), (255, 69, 0), (255, 140, 0), (255, 215, 0)],
            'mystery': [(75, 0, 130), (72, 61, 139), (123, 104, 238), (138, 43, 226)],
            'nature': [(34, 139, 34), (60, 179, 113), (46, 139, 87), (143, 188, 143)],
            'sadness': [(70, 130, 180), (100, 149, 237), (176, 196, 222), (119, 136, 153)],
            'passion': [(220, 20, 60), (178, 34, 34), (139, 0, 0), (255, 20, 147)],
            'peace': [(135, 206, 250), (176, 224, 230), (240, 248, 255), (230, 230, 250)],
            'anxiety': [(139, 0, 139), (148, 0, 211), (75, 0, 130), (128, 0, 128)],
            'love': [(255, 182, 193), (255, 192, 203), (255, 105, 180), (219, 112, 147)]
        }
        
        # Theme-based color palettes (NEW!)
        self.theme_colors = {
            'ocean': [(0, 105, 148), (0, 119, 182), (100, 149, 237), (135, 206, 250), (173, 216, 230)],
            'sunset': [(255, 94, 77), (255, 120, 0), (255, 165, 0), (255, 200, 124), (255, 223, 186)],
            'forest': [(34, 139, 34), (0, 100, 0), (85, 107, 47), (107, 142, 35), (154, 205, 50)],
            'fire': [(220, 20, 60), (255, 69, 0), (255, 140, 0), (255, 165, 0), (255, 215, 0)],
            'space': [(0, 0, 50), (25, 25, 112), (72, 61, 139), (138, 43, 226), (147, 112, 219)],
            'desert': [(237, 201, 175), (210, 180, 140), (244, 164, 96), (218, 165, 32), (184, 134, 11)],
            'snow': [(240, 248, 255), (230, 230, 250), (176, 224, 230), (173, 216, 230), (135, 206, 250)],
            'city': [(105, 105, 105), (128, 128, 128), (169, 169, 169), (192, 192, 192), (211, 211, 211)],
            'rainbow': [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
        }
        
        # Keyword detection for prompt analysis (NEW!)
        self.keyword_themes = {
            'ocean': ['ocean', 'sea', 'water', 'wave', 'beach', 'tide', 'surf', 'marine', 'aquatic'],
            'sunset': ['sunset', 'sunrise', 'dusk', 'dawn', 'twilight', 'evening', 'golden hour'],
            'forest': ['forest', 'tree', 'woods', 'jungle', 'leaves', 'nature', 'wilderness'],
            'fire': ['fire', 'flame', 'burn', 'inferno', 'blaze', 'ember', 'heat'],
            'space': ['space', 'galaxy', 'star', 'cosmic', 'nebula', 'planet', 'universe', 'celestial'],
            'desert': ['desert', 'sand', 'dune', 'arid', 'dry', 'oasis'],
            'snow': ['snow', 'ice', 'winter', 'frost', 'frozen', 'cold', 'blizzard'],
            'city': ['city', 'urban', 'building', 'skyline', 'metropolis', 'street'],
            'rainbow': ['rainbow', 'colorful', 'vibrant', 'spectrum', 'prism']
        }
        
        # Artistic styles
        self.styles = {
            'abstract': self._generate_abstract,
            'geometric': self._generate_geometric,
            'organic': self._generate_organic,
            'fractal': self._generate_fractal,
            'waves': self._generate_waves,
            'particles': self._generate_particles,
            'gradient': self._generate_gradient,
            'mandala': self._generate_mandala,
            'galaxy': self._generate_galaxy,
            'landscape': self._generate_landscape
        }
    
    def _analyze_prompt(self, prompt: str) -> Dict:
        """
        Analyze prompt to extract themes, subjects, and keywords (NEW!)
        """
        prompt_lower = prompt.lower()
        detected_themes = []
        detected_subjects = []
        
        # Detect themes
        for theme, keywords in self.keyword_themes.items():
            if any(keyword in prompt_lower for keyword in keywords):
                detected_themes.append(theme)
        
        # Extract subject keywords
        subjects = {
            'cat': ['cat', 'kitten', 'feline'],
            'dog': ['dog', 'puppy', 'canine'],
            'bird': ['bird', 'eagle', 'owl', 'parrot'],
            'mountain': ['mountain', 'peak', 'cliff', 'hill'],
            'flower': ['flower', 'rose', 'bloom', 'blossom'],
            'heart': ['heart', 'love', 'romance'],
            'sun': ['sun', 'solar', 'sunshine'],
            'moon': ['moon', 'lunar', 'crescent'],
            'cloud': ['cloud', 'sky', 'atmosphere']
        }
        
        for subject, keywords in subjects.items():
            if any(keyword in prompt_lower for keyword in keywords):
                detected_subjects.append(subject)
        
        return {
            'themes': detected_themes,
            'subjects': detected_subjects,
            'has_themes': len(detected_themes) > 0,
            'has_subjects': len(detected_subjects) > 0,
            'original': prompt
        }
    
    def generate_art(self, prompt: str, 
                    style: str = 'abstract',
                    emotion: str = 'joy',
                    width: int = 1024,
                    height: int = 1024,
                    seed: int = None) -> Dict:
        """
        Generate art based on parameters
        NOW WITH PROMPT ANALYSIS!
        """
        if seed:
            random.seed(seed)
            np.random.seed(seed)
        
        # Analyze the prompt (NEW!)
        prompt_analysis = self._analyze_prompt(prompt)
        
        # Get color palette - prioritize theme colors over emotion colors
        if prompt_analysis['has_themes'] and prompt_analysis['themes'][0] in self.theme_colors:
            colors = self.theme_colors[prompt_analysis['themes'][0]]
        else:
            colors = self.emotion_colors.get(emotion.lower(), self.emotion_colors['joy'])
        
        # Get style function
        style_func = self.styles.get(style.lower(), self._generate_abstract)
        
        # Generate base image with prompt context
        image = style_func(width, height, colors, prompt, prompt_analysis)
        
        # Add subjects/elements based on prompt (NEW!)
        image = self._add_prompt_elements(image, prompt_analysis, colors)
        
        # Apply emotion-based post-processing
        image = self._apply_emotion_effects(image, emotion)
        
        # Add text overlay with prompt (NEW!)
        image = self._add_text_overlay(image, prompt, width, height)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"art_{style}_{emotion}_{timestamp}.png"
        filepath = f"{self.output_path}/{filename}"
        
        image.save(filepath, 'PNG', quality=95)
        
        return {
            'success': True,
            'image_path': filepath,
            'image_url': f'/{filepath}',
            'prompt': prompt,
            'style': style,
            'emotion': emotion,
            'dimensions': (width, height),
            'seed': seed,
            'detected_themes': prompt_analysis['themes'],
            'detected_subjects': prompt_analysis['subjects']
        }
    
    def _add_prompt_elements(self, image: PILImage, analysis: Dict, colors: List[Tuple]) -> PILImage:
        """
        Add visual elements based on prompt analysis (NEW!)
        """
        draw = ImageDraw.Draw(image, 'RGBA')
        width, height = image.size
        
        # Add subject-based shapes
        for subject in analysis['subjects']:
            if subject == 'sun':
                # Draw sun
                x, y = random.randint(width//4, 3*width//4), random.randint(height//4, height//2)
                r = random.randint(80, 150)
                sun_color = (255, 215, 0, 200)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=sun_color)
                # Sun rays
                for i in range(12):
                    angle = i * math.pi / 6
                    x2 = x + (r + 50) * math.cos(angle)
                    y2 = y + (r + 50) * math.sin(angle)
                    draw.line([x, y, x2, y2], fill=sun_color, width=8)
            
            elif subject == 'moon':
                # Draw moon
                x, y = random.randint(width//4, 3*width//4), random.randint(height//4, height//2)
                r = random.randint(60, 120)
                moon_color = (245, 245, 220, 220)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=moon_color)
                # Craters
                for _ in range(5):
                    cx = x + random.randint(-r//2, r//2)
                    cy = y + random.randint(-r//2, r//2)
                    cr = random.randint(5, 20)
                    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(200, 200, 180, 150))
            
            elif subject == 'mountain':
                # Draw mountains
                num_peaks = random.randint(3, 6)
                for i in range(num_peaks):
                    base_x = (i * width) // num_peaks
                    peak_x = base_x + width // (2 * num_peaks)
                    peak_y = random.randint(height//3, height//2)
                    base_y = height
                    
                    points = [
                        (base_x, base_y),
                        (peak_x, peak_y),
                        (base_x + width // num_peaks, base_y)
                    ]
                    color = random.choice(colors) + (random.randint(180, 220),)
                    draw.polygon(points, fill=color)
            
            elif subject == 'heart':
                # Draw heart shape
                cx, cy = width // 2, height // 2
                size = min(width, height) // 4
                heart_color = (255, 105, 180, 200)
                
                # Simple heart using circles and triangle
                draw.ellipse([cx-size, cy-size//2, cx, cy+size//2], fill=heart_color)
                draw.ellipse([cx, cy-size//2, cx+size, cy+size//2], fill=heart_color)
                draw.polygon([(cx-size, cy), (cx, cy+size), (cx+size, cy)], fill=heart_color)
            
            elif subject == 'cat':
                # Draw recognizable cat
                cx, cy = width // 2, height // 2
                size = min(width, height) // 4
                
                # Cat colors (cute palette)
                body_color = (255, 160, 122, 255)  # Salmon
                detail_color = (255, 192, 203, 255)  # Pink
                eye_color = (64, 224, 208, 255)  # Turquoise
                
                # Body (sitting cat)
                body_width = int(size * 1.5)
                body_height = int(size * 1.3)
                draw.ellipse([cx-body_width//2, cy-body_height//2, 
                            cx+body_width//2, cy+body_height//2], fill=body_color)
                
                # Head (above body)
                head_size = int(size * 0.9)
                head_y = cy - body_height//2 - head_size//3
                draw.ellipse([cx-head_size//2, head_y-head_size//2, 
                            cx+head_size//2, head_y+head_size//2], fill=body_color)
                
                # Ears (triangular)
                ear_size = int(size * 0.6)
                # Left ear
                draw.polygon([
                    (cx-head_size//3, head_y-head_size//2),
                    (cx-head_size//2-ear_size//4, head_y-head_size//2-ear_size),
                    (cx-head_size//6, head_y-head_size//2)
                ], fill=body_color)
                # Right ear
                draw.polygon([
                    (cx+head_size//6, head_y-head_size//2),
                    (cx+head_size//2+ear_size//4, head_y-head_size//2-ear_size),
                    (cx+head_size//3, head_y-head_size//2)
                ], fill=body_color)
                
                # Inner ears (pink)
                draw.polygon([
                    (cx-head_size//4, head_y-head_size//2+ear_size//4),
                    (cx-head_size//2-ear_size//6, head_y-head_size//2-ear_size//2),
                    (cx-head_size//5, head_y-head_size//2+ear_size//4)
                ], fill=detail_color)
                draw.polygon([
                    (cx+head_size//5, head_y-head_size//2+ear_size//4),
                    (cx+head_size//2+ear_size//6, head_y-head_size//2-ear_size//2),
                    (cx+head_size//4, head_y-head_size//2+ear_size//4)
                ], fill=detail_color)
                
                # Eyes
                eye_offset = head_size // 4
                eye_size = head_size // 6
                # Left eye
                draw.ellipse([cx-eye_offset-eye_size, head_y-eye_size//2,
                            cx-eye_offset+eye_size, head_y+eye_size//2], fill=eye_color)
                draw.ellipse([cx-eye_offset-eye_size//3, head_y-eye_size//3,
                            cx-eye_offset+eye_size//3, head_y+eye_size//3], fill=(0, 0, 0, 255))
                # Right eye
                draw.ellipse([cx+eye_offset-eye_size, head_y-eye_size//2,
                            cx+eye_offset+eye_size, head_y+eye_size//2], fill=eye_color)
                draw.ellipse([cx+eye_offset-eye_size//3, head_y-eye_size//3,
                            cx+eye_offset+eye_size//3, head_y+eye_size//3], fill=(0, 0, 0, 255))
                
                # Nose (pink triangle)
                nose_size = head_size // 10
                draw.polygon([
                    (cx, head_y+nose_size*2),
                    (cx-nose_size, head_y+nose_size),
                    (cx+nose_size, head_y+nose_size)
                ], fill=detail_color)
                
                # Whiskers
                whisker_length = size // 2
                whisker_y = head_y
                for i in [-1, 0, 1]:
                    # Left whiskers
                    draw.line([cx-head_size//2, whisker_y+i*10, 
                             cx-head_size//2-whisker_length, whisker_y+i*15], 
                             fill=(0, 0, 0, 200), width=2)
                    # Right whiskers
                    draw.line([cx+head_size//2, whisker_y+i*10,
                             cx+head_size//2+whisker_length, whisker_y+i*15], 
                             fill=(0, 0, 0, 200), width=2)
                
                # Tail (curved)
                tail_start_x = cx + body_width//2 - 20
                tail_start_y = cy
                for i in range(5):
                    tx = tail_start_x + i * 30
                    ty = tail_start_y - i * 40 - (i*i) * 5
                    draw.ellipse([tx-15, ty-15, tx+15, ty+15], fill=body_color)
            
            elif subject == 'dog':
                # Draw recognizable dog
                cx, cy = width // 2, height // 2
                size = min(width, height) // 4
                
                dog_color = (210, 180, 140, 255)  # Tan
                detail_color = (139, 69, 19, 255)  # Brown
                
                # Body
                body_width = int(size * 1.6)
                body_height = size
                draw.ellipse([cx-body_width//2, cy-body_height//2,
                            cx+body_width//2, cy+body_height//2], fill=dog_color)
                
                # Head (side view)
                head_size = int(size * 0.8)
                head_x = cx - body_width//2 - head_size//3
                draw.ellipse([head_x-head_size//2, cy-head_size//2,
                            head_x+head_size//2, cy+head_size//2], fill=dog_color)
                
                # Floppy ears
                ear_size = int(size * 0.7)
                # Left ear
                draw.ellipse([head_x-head_size//2-ear_size//3, cy-ear_size//4,
                            head_x-head_size//2+ear_size//3, cy+ear_size], fill=detail_color)
                
                # Nose/snout
                snout_x = head_x - head_size//3
                draw.ellipse([snout_x-20, cy-10, snout_x+20, cy+10], fill=(0, 0, 0, 255))
                
                # Eye
                draw.ellipse([head_x-10, cy-head_size//4-10,
                            head_x+10, cy-head_size//4+10], fill=(0, 0, 0, 255))
                
                # Tail (wagging)
                tail_x = cx + body_width//2
                draw.arc([tail_x-30, cy-60, tail_x+50, cy+20], 
                        start=-30, end=120, fill=dog_color, width=20)
            
            elif subject == 'bird':
                # Draw recognizable bird
                cx, cy = width // 2, height // 2
                size = min(width, height) // 4
                
                bird_color = (135, 206, 250, 255)  # Sky blue
                wing_color = (100, 149, 237, 255)  # Cornflower blue
                
                # Body
                draw.ellipse([cx-size//2, cy-size//3, cx+size//2, cy+size//3], fill=bird_color)
                
                # Head
                head_size = size // 2
                draw.ellipse([cx-head_size//2, cy-size//2-head_size//2,
                            cx+head_size//2, cy-size//2+head_size//2], fill=bird_color)
                
                # Beak
                beak_points = [
                    (cx, cy-size//2),
                    (cx-head_size//3, cy-size//2-head_size//4),
                    (cx-head_size//3, cy-size//2+head_size//4)
                ]
                draw.polygon(beak_points, fill=(255, 165, 0, 255))
                
                # Eye
                draw.ellipse([cx+head_size//6, cy-size//2-5,
                            cx+head_size//6+10, cy-size//2+5], fill=(0, 0, 0, 255))
                
                # Wings (spread)
                # Left wing
                wing_points = [
                    (cx-size//2, cy),
                    (cx-size-size//2, cy-size//2),
                    (cx-size-size//3, cy+size//4)
                ]
                draw.polygon(wing_points, fill=wing_color)
                # Right wing
                wing_points_r = [
                    (cx+size//2, cy),
                    (cx+size+size//2, cy-size//2),
                    (cx+size+size//3, cy+size//4)
                ]
                draw.polygon(wing_points_r, fill=wing_color)
                
                # Tail feathers
                for i in range(3):
                    offset = (i-1) * 20
                    draw.line([cx, cy+size//3, cx+offset, cy+size], 
                            fill=wing_color, width=10)
        
        return image
    
    def _add_text_overlay(self, image: PILImage, prompt: str, width: int, height: int) -> PILImage:
        """
        Add text overlay showing the prompt (NEW!)
        """
        draw = ImageDraw.Draw(image, 'RGBA')
        
        # Add semi-transparent background for text
        text_bg_height = 80
        draw.rectangle([0, height - text_bg_height, width, height], 
                      fill=(0, 0, 0, 180))
        
        # Add prompt text
        try:
            font_size = 24
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Truncate prompt if too long
        display_prompt = prompt if len(prompt) <= 80 else prompt[:77] + "..."
        
        # Calculate text position (centered)
        bbox = draw.textbbox((0, 0), display_prompt, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        text_y = height - text_bg_height + 25
        
        # Draw text with outline for visibility
        outline_color = (0, 0, 0, 255)
        for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-1,-1), (-1,1), (1,-1), (1,1)]:
            draw.text((text_x + dx, text_y + dy), display_prompt, font=font, fill=outline_color)
        
        draw.text((text_x, text_y), display_prompt, font=font, fill=(255, 255, 255, 255))
        
        return image
    
    # ==================== STYLE GENERATORS (ENHANCED) ====================
    
    def _generate_abstract(self, width: int, height: int, 
                          colors: List[Tuple], prompt: str, analysis: Dict) -> PILImage:
        """Generate abstract art - NOW PROMPT-AWARE"""
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image, 'RGBA')
        
        # More shapes for more detail
        num_shapes = random.randint(100, 200)
        
        # Bias shape positions based on themes
        for i in range(num_shapes):
            shape_type = random.choice(['rectangle', 'ellipse', 'polygon', 'line'])
            color = random.choice(colors) + (random.randint(120, 255),)
            
            if shape_type == 'rectangle':
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                x2 = x1 + random.randint(30, 200)
                y2 = y1 + random.randint(30, 200)
                draw.rectangle([x1, y1, x2, y2], fill=color)
                
            elif shape_type == 'ellipse':
                x = random.randint(0, width)
                y = random.randint(0, height)
                r = random.randint(20, 150)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
                
            elif shape_type == 'polygon':
                points = [(random.randint(0, width), random.randint(0, height)) 
                         for _ in range(random.randint(3, 6))]
                draw.polygon(points, fill=color)
            
            elif shape_type == 'line':
                x1, y1 = random.randint(0, width), random.randint(0, height)
                x2, y2 = random.randint(0, width), random.randint(0, height)
                draw.line([x1, y1, x2, y2], fill=color, width=random.randint(3, 15))
        
        # Light blur for cohesion
        image = image.filter(ImageFilter.GaussianBlur(radius=1))
        
        return image
    
    def _generate_geometric(self, width: int, height: int,
                           colors: List[Tuple], prompt: str, analysis: Dict) -> PILImage:
        """Generate geometric patterns"""
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Variable cell size for more interest
        cell_size = random.randint(30, 80)
        
        for y in range(0, height, cell_size):
            for x in range(0, width, cell_size):
                color = random.choice(colors)
                pattern = random.choice(['square', 'circle', 'triangle', 'diamond', 'hexagon'])
                
                if pattern == 'square':
                    draw.rectangle([x, y, x+cell_size, y+cell_size], 
                                 fill=color, outline='black', width=2)
                elif pattern == 'circle':
                    draw.ellipse([x, y, x+cell_size, y+cell_size],
                               fill=color, outline='black', width=2)
                elif pattern == 'triangle':
                    points = [(x+cell_size//2, y), (x, y+cell_size), 
                             (x+cell_size, y+cell_size)]
                    draw.polygon(points, fill=color, outline='black')
                elif pattern == 'diamond':
                    points = [(x+cell_size//2, y), (x+cell_size, y+cell_size//2),
                             (x+cell_size//2, y+cell_size), (x, y+cell_size//2)]
                    draw.polygon(points, fill=color, outline='black')
                elif pattern == 'hexagon':
                    points = [
                        (x + cell_size//2, y),
                        (x + cell_size, y + cell_size//4),
                        (x + cell_size, y + 3*cell_size//4),
                        (x + cell_size//2, y + cell_size),
                        (x, y + 3*cell_size//4),
                        (x, y + cell_size//4)
                    ]
                    draw.polygon(points, fill=color, outline='black')
        
        return image
    
    def _generate_organic(self, width: int, height: int,
                         colors: List[Tuple], prompt: str, analysis: Dict) -> PILImage:
        """Generate organic flowing shapes"""
        image = Image.new('RGB', (width, height), color=colors[0])
        draw = ImageDraw.Draw(image, 'RGBA')
        
        # More curves for detail
        num_curves = random.randint(20, 40)
        
        for _ in range(num_curves):
            points = []
            x = random.randint(0, width)
            y = random.randint(0, height)
            
            # Longer, more detailed curves
            for i in range(80):
                angle = i * 0.15 + random.uniform(-0.3, 0.3)
                step = random.randint(8, 25)
                x += step * math.cos(angle)
                y += step * math.sin(angle)
                
                x = max(0, min(width, x))
                y = max(0, min(height, y))
                
                points.append((int(x), int(y)))
            
            # Draw curve with varying thickness
            color = random.choice(colors) + (random.randint(120, 200),)
            for i in range(len(points) - 1):
                thickness = random.randint(8, 30)
                draw.line([points[i], points[i+1]], fill=color, width=thickness)
        
        return image
    
    def _generate_fractal(self, width: int, height: int,
                         colors: List[Tuple], prompt: str, analysis: Dict) -> PILImage:
        """Generate fractal patterns"""
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        # Enhanced fractal with zoom variation
        zoom = random.uniform(0.8, 1.5)
        move_x = random.uniform(-1, 0)
        move_y = random.uniform(-0.5, 0.5)
        max_iter = 100
        
        for x in range(width):
            for y in range(height):
                zx = 1.5 * (x - width / 2) / (0.5 * zoom * width) + move_x
                zy = (y - height / 2) / (0.5 * zoom * height) + move_y
                
                c = complex(zx, zy)
                z = complex(0, 0)
                
                iteration = 0
                while abs(z) <= 2 and iteration < max_iter:
                    z = z*z + c
                    iteration += 1
                
                if iteration == max_iter:
                    pixels[x, y] = (0, 0, 0)
                else:
                    color_idx = iteration % len(colors)
                    color = colors[color_idx]
                    brightness = int(255 * (iteration / max_iter))
                    pixels[x, y] = tuple(min(255, int(c * brightness / 255)) for c in color)
        
        return image
    
    def _generate_waves(self, width: int, height: int,
                       colors: List[Tuple], prompt: str, analysis: Dict) -> PILImage:
        """Generate wave patterns"""
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        # More complex wave combinations
        num_waves = random.randint(5, 12)
        
        for x in range(width):
            for y in range(height):
                value = 0
                
                for i in range(num_waves):
                    freq = random.uniform(0.005, 0.03)
                    amp = random.uniform(30, 150)
                    phase = random.uniform(0, 2 * math.pi)
                    
                    value += amp * math.sin(freq * x + phase) * math.cos(freq * y + phase)
                
                value = (value + 800) / 1600
                value = max(0, min(1, value))
                
                color_idx = int(value * (len(colors) - 1))
                pixels[x, y] = colors[color_idx]
        
        return image
    
    def _generate_particles(self, width: int, height: int,
                           colors: List[Tuple], prompt: str, analysis: Dict) -> PILImage:
        """Generate particle system"""
        image = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(image, 'RGBA')
        
        # More particles with clusters
        num_particles = random.randint(2000, 5000)
        
        center_x = width // 2
        center_y = height // 2
        
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, min(width, height) * 0.5)
            
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            
            size = random.randint(1, 8)
            color = random.choice(colors) + (random.randint(120, 255),)
            
            draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
        
        # Enhanced glow
        image = image.filter(ImageFilter.GaussianBlur(radius=4))
        
        return image
    
    def _generate_gradient(self, width: int, height: int,
                          colors: List[Tuple], prompt: str, analysis: Dict) -> PILImage:
        """Generate gradient art"""
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        # Multi-directional gradient
        for y in range(height):
            for x in range(width):
                t = math.sqrt((x/width)**2 + (y/height)**2)
                t = min(1, t)
                
                color_idx = t * (len(colors) - 1)
                idx1 = int(color_idx)
                idx2 = min(idx1 + 1, len(colors) - 1)
                blend = color_idx - idx1
                
                color1 = colors[idx1]
                color2 = colors[idx2]
                
                r = int(color1[0] * (1 - blend) + color2[0] * blend)
                g = int(color1[1] * (1 - blend) + color2[1] * blend)
                b = int(color1[2] * (1 - blend) + color2[2] * blend)
                
                pixels[x, y] = (r, g, b)
        
        return image
    
    def _generate_mandala(self, width: int, height: int,
                         colors: List[Tuple], prompt: str, analysis: Dict) -> PILImage:
        """Generate mandala pattern"""
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image, 'RGBA')
        
        center_x = width // 2
        center_y = height // 2
        
        segments = random.randint(8, 16)
        
        for segment in range(segments):
            angle = (2 * math.pi * segment) / segments
            
            # More layers for detail
            for layer in range(8):
                radius = (layer + 1) * min(width, height) // 18
                color = random.choice(colors) + (random.randint(150, 255),)
                
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                size = random.randint(15, 60)
                shape = random.choice(['circle', 'diamond', 'star'])
                
                if shape == 'circle':
                    draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
                elif shape == 'diamond':
                    points = [(x, y-size), (x+size, y), (x, y+size), (x-size, y)]
                    draw.polygon(points, fill=color)
        
        return image
    
    def _generate_galaxy(self, width: int, height: int,
                        colors: List[Tuple], prompt: str, analysis: Dict) -> PILImage:
        """Generate galaxy/space art"""
        image = Image.new('RGB', (width, height), color=(0, 0, 20))
        draw = ImageDraw.Draw(image, 'RGBA')
        
        # More stars with size variation
        num_stars = random.randint(800, 1500)
        for _ in range(num_stars):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 5)
            brightness = random.randint(150, 255)
            draw.ellipse([x-size, y-size, x+size, y+size], 
                        fill=(brightness, brightness, brightness))
        
        # Enhanced nebula with more variation
        num_clouds = random.randint(5, 10)
        for _ in range(num_clouds):
            x = random.randint(-width//4, width)
            y = random.randint(-height//4, height)
            size = random.randint(150, 400)
            color = random.choice(colors) + (random.randint(60, 180),)
            draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
        
        # Stronger blur for nebula
        image = image.filter(ImageFilter.GaussianBlur(radius=25))
        
        return image
    
    def _generate_landscape(self, width: int, height: int,
                           colors: List[Tuple], prompt: str, analysis: Dict) -> PILImage:
        """Generate abstract landscape"""
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        # Enhanced sky gradient
        sky_colors = colors[:2] if len(colors) >= 2 else colors
        for y in range(height // 2):
            t = y / (height // 2)
            color = tuple(int(sky_colors[0][i] * (1-t) + sky_colors[1][i] * t) 
                         for i in range(3))
            for x in range(width):
                pixels[x, y] = color
        
        # Textured ground
        ground_colors = colors[2:] if len(colors) > 2 else colors
        for y in range(height // 2, height):
            for x in range(width):
                color = random.choice(ground_colors)
                noise = random.randint(-15, 15)
                pixels[x, y] = tuple(max(0, min(255, c + noise)) for c in color)
        
        # More detailed hills
        draw = ImageDraw.Draw(image, 'RGBA')
        for layer in range(5):
            points = []
            y_base = height // 2 + layer * 40
            
            for x in range(0, width + 10, 10):
                y = y_base + int(50 * math.sin(x * 0.015 + layer) + 20 * math.cos(x * 0.03))
                points.append((x, y))
            
            points.append((width, height))
            points.append((0, height))
            
            color = random.choice(colors) + (random.randint(180, 220),)
            draw.polygon(points, fill=color)
        
        return image
    
    def _apply_emotion_effects(self, image: PILImage, emotion: str) -> PILImage:
        """Apply emotion-based post-processing effects"""
        
        if emotion.lower() in ['calm', 'peace']:
            image = image.filter(ImageFilter.GaussianBlur(radius=1))
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)
            
        elif emotion.lower() in ['energy', 'passion']:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.4)
            
        elif emotion.lower() in ['mystery', 'anxiety']:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(0.8)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
        elif emotion.lower() == 'sadness':
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(0.6)
            image = image.filter(ImageFilter.GaussianBlur(radius=1))
        
        return image
