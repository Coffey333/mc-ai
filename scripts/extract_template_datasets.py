#!/usr/bin/env python3
"""
Extract high-quality dataset examples from template guides
NO generation cost - pure extraction
"""

import json
import os
from typing import List, Dict

def extract_mathematics_examples() -> List[Dict]:
    """Extract mathematics examples from template"""
    return [
        # Arithmetic
        {'prompt': 'What is 247 + 389?', 'response': '247 + 389 = 636', 'domain': 'mathematics'},
        {'prompt': 'What is 15 × 23?', 'response': '15 × 23 = 345', 'domain': 'mathematics'},
        {'prompt': 'What is 144 ÷ 12?', 'response': '144 ÷ 12 = 12', 'domain': 'mathematics'},
        
        # Algebra
        {'prompt': 'Solve for x: 2x + 5 = 13', 'response': 'To solve 2x + 5 = 13:\n1. Subtract 5 from both sides: 2x = 8\n2. Divide both sides by 2: x = 4\nAnswer: x = 4', 'domain': 'mathematics'},
        {'prompt': 'Solve the quadratic equation: x² - 5x + 6 = 0', 'response': 'To solve x² - 5x + 6 = 0:\nMethod 1 (Factoring): (x - 2)(x - 3) = 0\nTherefore: x = 2 or x = 3\n\nMethod 2 (Quadratic formula): x = (5 ± √(25-24))/2 = (5 ± 1)/2\nx = 3 or x = 2', 'domain': 'mathematics'},
        
        # Geometry
        {'prompt': 'What is the area of a circle with radius 5?', 'response': 'The area of a circle is A = πr²\nWith radius r = 5:\nA = π(5)² = 25π ≈ 78.54 square units', 'domain': 'mathematics'},
        {'prompt': 'What is the Pythagorean theorem?', 'response': 'The Pythagorean theorem states that in a right triangle, the square of the hypotenuse (c) equals the sum of squares of the other two sides (a and b):\n\na² + b² = c²\n\nExample: If a = 3 and b = 4, then c² = 9 + 16 = 25, so c = 5', 'domain': 'mathematics'},
        
        # Calculus
        {'prompt': 'What is the derivative of x²?', 'response': 'The derivative of x² with respect to x is 2x.\n\nUsing the power rule: d/dx(xⁿ) = nxⁿ⁻¹\nFor x²: d/dx(x²) = 2x²⁻¹ = 2x', 'domain': 'mathematics'},
        {'prompt': 'What is the integral of 2x?', 'response': 'The integral of 2x with respect to x is x² + C (where C is the constant of integration).\n\n∫2x dx = x² + C\n\nUsing the power rule for integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C', 'domain': 'mathematics'},
        
        # Statistics
        {'prompt': 'What is the mean of 3, 7, 9, 12, 15?', 'response': 'The mean (average) is the sum divided by the count.\n\nSum: 3 + 7 + 9 + 12 + 15 = 46\nCount: 5\nMean: 46 ÷ 5 = 9.2', 'domain': 'mathematics'},
        {'prompt': 'What is the median of 3, 7, 9, 12, 15?', 'response': 'The median is the middle value when numbers are arranged in order.\n\nOrdered: 3, 7, 9, 12, 15\nMiddle position: 3rd number\nMedian: 9', 'domain': 'mathematics'},
        
        # Number Theory
        {'prompt': 'What is a prime number?', 'response': 'A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.\n\nExamples: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...\n\nNote: 2 is the only even prime number. All other primes are odd.', 'domain': 'mathematics'},
        {'prompt': 'What is the Fibonacci sequence?', 'response': 'The Fibonacci sequence is a series where each number is the sum of the two preceding ones:\n\n0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...\n\nFormula: F(n) = F(n-1) + F(n-2)\nWith F(0) = 0 and F(1) = 1\n\nThis sequence appears throughout nature in spiral patterns, flower petals, and tree branches.', 'domain': 'mathematics'}
    ]

def extract_color_examples() -> List[Dict]:
    """Extract color theory examples"""
    return [
        {'prompt': 'What are the primary colors?', 'response': 'The primary colors depend on the color model:\n\n**Additive (Light/RGB):** Red, Green, Blue\n- Used in screens, TVs, monitors\n- Mixing all three creates white light\n\n**Subtractive (Paint/CMY):** Cyan, Magenta, Yellow\n- Used in printing and painting\n- Mixing all three creates black (in theory, brown in practice)\n\n**Traditional Art:** Red, Yellow, Blue\n- Historically taught in art classes\n- Cannot be created by mixing other colors', 'domain': 'colors'},
        {'prompt': 'What color do you get when you mix red and blue?', 'response': 'Mixing red and blue creates purple (or violet).\n\n**Paint Mixing (Subtractive):**\n- Equal parts: Medium purple\n- More red: Red-purple (magenta-ish)\n- More blue: Blue-purple (violet)\n\n**Light Mixing (Additive/RGB):**\n- Red + Blue = Magenta\n\nThe exact shade depends on the specific reds and blues used.', 'domain': 'colors'},
        {'prompt': 'What emotions does the color blue evoke?', 'response': 'Blue is associated with:\n\n**Positive:**\n- Calmness and tranquility\n- Trust and reliability\n- Professionalism and stability\n- Peace and serenity\n- Intelligence and wisdom\n\n**Context-dependent:**\n- Light blue: Peacefulness, openness\n- Dark blue: Authority, confidence\n- Bright blue: Energy, freshness\n\n**Cultural notes:**\n- Most universally liked color\n- Used by many corporations (Facebook, IBM, Ford)\n- Can evoke sadness in some contexts ("feeling blue")', 'domain': 'colors'},
        {'prompt': 'What is RGB color space?', 'response': 'RGB (Red, Green, Blue) is an additive color model used for displaying colors on screens.\n\n**How it works:**\n- Three channels: Red, Green, Blue\n- Each ranges from 0-255 (8-bit)\n- Total: 16,777,216 possible colors (256³)\n\n**Examples:**\n- Red: (255, 0, 0)\n- Green: (0, 255, 0)\n- Blue: (0, 0, 255)\n- White: (255, 255, 255)\n- Black: (0, 0, 0)\n- Yellow: (255, 255, 0)\n\n**Uses:** Computer screens, TVs, cameras, web design', 'domain': 'colors'}
    ]

def extract_children_education_examples() -> List[Dict]:
    """Extract children's education examples"""
    return [
        {'prompt': 'What activities are good for 3-year-olds?', 'response': '**Great activities for 3-year-olds to promote development:**\n\n**Physical Development:**\n1. Obstacle courses, dancing, ball games\n2. Tricycle riding, playground time\n\n**Fine Motor Skills:**\n1. Playdough, coloring, building blocks\n2. Puzzles (4-8 pieces), stringing beads\n\n**Cognitive:**\n1. Sorting games (colors, shapes)\n2. Counting, matching games, simple board games\n\n**Language:**\n1. Reading books (20 min daily)\n2. Singing songs, storytelling, pretend play\n\n**Social/Emotional:**\n1. Playdates, role-playing\n2. Emotion recognition, helping with chores\n\n**Screen time:** Limit to 1 hour/day of high-quality programming', 'domain': 'kids_education'},
        {'prompt': 'Can you help me with my multiplication tables?', 'response': "**Let's learn multiplication tables!**\n\n**Understanding:** Multiplication is repeated addition!\n- 3 × 4 means '3 groups of 4' = 12\n\n**Easy tricks:**\n- ×0: Always 0\n- ×1: Same number\n- ×2: Double it!\n- ×5: Ends in 0 or 5\n- ×9: Finger trick!\n- ×10: Add a zero\n- ×11: Repeat digit (11×3=33)\n\n**Practice:**\n- Flash cards daily\n- Skip counting\n- Math games online\n- Multiplication songs\n\n**Remember:** Order doesn't matter! 3×4 = 4×3", 'domain': 'kids_education'},
        {'prompt': 'Why do leaves change color in fall?', 'response': '**The Science of Fall Colors!**\n\n**Summer:** Leaves have chlorophyll (makes them GREEN)\n- Chlorophyll helps make food (photosynthesis)\n\n**Fall happens:**\n1. Days get shorter, less sunlight\n2. Trees stop making chlorophyll\n3. Green fades away\n4. Hidden colors appear!\n\n**The Colors:**\n- 🟡 Yellow (always there, now visible)\n- 🟠 Orange (same as carrots!)\n- 🔴 Red (made NEW in fall)\n- 🟤 Brown (waste products)\n\n**Why leaves fall:**\n- Tree seals off connection\n- Saves energy for winter\n\n**Best colors:** Sunny days + cool nights!', 'domain': 'kids_education'}
    ]

def extract_plant_examples() -> List[Dict]:
    """Extract plant/botany examples"""
    return [
        {'prompt': 'What is photosynthesis?', 'response': 'Photosynthesis is the process by which plants convert light energy into chemical energy (glucose).\n\n**Equation:** 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂\n\n**Process:**\n1. Plants absorb sunlight through chlorophyll\n2. Light energy splits water molecules\n3. CO₂ combines with hydrogen\n4. Produces glucose and releases oxygen\n\n**Importance:**\n- Produces oxygen we breathe\n- Creates food for plants\n- Base of food chains\n- Removes CO₂ from atmosphere', 'domain': 'plants_botany'},
        {'prompt': 'How do I care for a snake plant?', 'response': 'Snake Plant (Sansevieria) - easiest houseplant!\n\n**Light:** Low to bright indirect (very tolerant)\n**Water:** Every 2-3 weeks, let soil dry completely\n**Soil:** Well-draining cactus/succulent mix\n**Temperature:** 60-85°F\n\n**Benefits:**\n- Purifies air\n- Produces oxygen at night\n- Nearly indestructible\n\n**Warning:** Overwatering is the main killer!', 'domain': 'plants_botany'}
    ]

def save_extracted_datasets():
    """Save all extracted examples"""
    print("\n" + "="*60)
    print("📦 EXTRACTING HIGH-QUALITY TEMPLATE DATASETS")
    print("="*60)
    print("\nNO cost - pure extraction from curated examples\n")
    
    domains = {
        'mathematics': extract_mathematics_examples(),
        'colors': extract_color_examples(),
        'kids_education': extract_children_education_examples(),
        'plants_botany': extract_plant_examples()
    }
    
    total = 0
    for domain, examples in domains.items():
        domain_dir = f'datasets/{domain}'
        os.makedirs(domain_dir, exist_ok=True)
        
        filepath = f'{domain_dir}/knowledge.json'
        with open(filepath, 'w') as f:
            json.dump(examples, f, indent=2)
        
        print(f"✅ {domain}: {len(examples)} examples")
        total += len(examples)
    
    print(f"\n{'='*60}")
    print(f"🎉 Extracted {total} high-quality examples")
    print(f"💰 Cost: $0.00 (pure extraction)")
    print(f"{'='*60}")
    
    return total

if __name__ == "__main__":
    save_extracted_datasets()
