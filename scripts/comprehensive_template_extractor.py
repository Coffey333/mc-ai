#!/usr/bin/env python3
"""
COMPREHENSIVE Template Extractor - Extract EVERYTHING
Based on provided Universal Knowledge & Children's Education templates
ALL examples included - complete extraction
"""

import json
import os
from typing import List, Dict

# ==================== UNIVERSAL KNOWLEDGE ====================

def extract_complete_mathematics() -> List[Dict]:
    """Complete mathematics dataset from template"""
    return [
        # Basic Arithmetic
        {'prompt': 'What is 247 + 389?', 'response': '247 + 389 = 636', 'domain': 'mathematics'},
        {'prompt': 'What is 15 × 23?', 'response': '15 × 23 = 345', 'domain': 'mathematics'},
        {'prompt': 'What is 144 ÷ 12?', 'response': '144 ÷ 12 = 12', 'domain': 'mathematics'},
        {'prompt': 'What is 456 - 189?', 'response': '456 - 189 = 267', 'domain': 'mathematics'},
        {'prompt': 'What is 25% of 80?', 'response': '25% of 80 = 0.25 × 80 = 20', 'domain': 'mathematics'},
        {'prompt': 'What is 3/4 + 1/2?', 'response': '3/4 + 1/2 = 3/4 + 2/4 = 5/4 = 1 1/4', 'domain': 'mathematics'},
        {'prompt': 'What is 2.5 × 4?', 'response': '2.5 × 4 = 10', 'domain': 'mathematics'},
        
        # Algebra
        {'prompt': 'Solve for x: 2x + 5 = 13', 'response': 'To solve 2x + 5 = 13:\n1. Subtract 5 from both sides: 2x = 8\n2. Divide both sides by 2: x = 4\nAnswer: x = 4', 'domain': 'mathematics'},
        {'prompt': 'Solve for y: 3y - 7 = 14', 'response': 'To solve 3y - 7 = 14:\n1. Add 7 to both sides: 3y = 21\n2. Divide both sides by 3: y = 7\nAnswer: y = 7', 'domain': 'mathematics'},
        {'prompt': 'Solve the quadratic equation: x² - 5x + 6 = 0', 'response': 'To solve x² - 5x + 6 = 0:\nMethod 1 (Factoring): (x - 2)(x - 3) = 0\nTherefore: x = 2 or x = 3\n\nMethod 2 (Quadratic formula): x = (5 ± √(25-24))/2 = (5 ± 1)/2\nx = 3 or x = 2', 'domain': 'mathematics'},
        {'prompt': 'What is the slope formula?', 'response': 'The slope formula is:\nm = (y₂ - y₁)/(x₂ - x₁)\n\nExample: Points (2, 3) and (5, 9)\nm = (9 - 3)/(5 - 2) = 6/3 = 2\n\nSlope represents rate of change.', 'domain': 'mathematics'},
        
        # Geometry
        {'prompt': 'What is the area of a circle with radius 5?', 'response': 'The area of a circle is A = πr²\nWith radius r = 5:\nA = π(5)² = 25π ≈ 78.54 square units', 'domain': 'mathematics'},
        {'prompt': 'What is the Pythagorean theorem?', 'response': 'The Pythagorean theorem states that in a right triangle, the square of the hypotenuse (c) equals the sum of squares of the other two sides (a and b):\n\na² + b² = c²\n\nExample: If a = 3 and b = 4, then c² = 9 + 16 = 25, so c = 5', 'domain': 'mathematics'},
        {'prompt': 'What is the perimeter of a rectangle with length 8 and width 5?', 'response': 'Perimeter of rectangle = 2(length + width)\nP = 2(8 + 5) = 2(13) = 26 units', 'domain': 'mathematics'},
        {'prompt': 'What is the volume of a cube with side length 4?', 'response': 'Volume of cube = side³\nV = 4³ = 4 × 4 × 4 = 64 cubic units', 'domain': 'mathematics'},
        {'prompt': 'What is the area of a triangle with base 6 and height 4?', 'response': 'Area of triangle = (1/2) × base × height\nA = (1/2) × 6 × 4 = 12 square units', 'domain': 'mathematics'},
        {'prompt': 'What is the circumference of a circle with radius 3?', 'response': 'Circumference = 2πr\nC = 2π(3) = 6π ≈ 18.85 units', 'domain': 'mathematics'},
        
        # Calculus
        {'prompt': 'What is the derivative of x²?', 'response': 'The derivative of x² with respect to x is 2x.\n\nUsing the power rule: d/dx(xⁿ) = nxⁿ⁻¹\nFor x²: d/dx(x²) = 2x²⁻¹ = 2x', 'domain': 'mathematics'},
        {'prompt': 'What is the derivative of 3x³?', 'response': 'Using the power rule: d/dx(xⁿ) = nxⁿ⁻¹\nFor 3x³: d/dx(3x³) = 3 × 3x² = 9x²', 'domain': 'mathematics'},
        {'prompt': 'What is the integral of 2x?', 'response': 'The integral of 2x with respect to x is x² + C (where C is the constant of integration).\n\n∫2x dx = x² + C\n\nUsing the power rule for integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C', 'domain': 'mathematics'},
        {'prompt': 'What is the derivative of sin(x)?', 'response': 'The derivative of sin(x) is cos(x).\n\nd/dx[sin(x)] = cos(x)', 'domain': 'mathematics'},
        
        # Statistics
        {'prompt': 'What is the mean of 3, 7, 9, 12, 15?', 'response': 'The mean (average) is the sum divided by the count.\n\nSum: 3 + 7 + 9 + 12 + 15 = 46\nCount: 5\nMean: 46 ÷ 5 = 9.2', 'domain': 'mathematics'},
        {'prompt': 'What is the median of 3, 7, 9, 12, 15?', 'response': 'The median is the middle value when numbers are arranged in order.\n\nOrdered: 3, 7, 9, 12, 15\nMiddle position: 3rd number\nMedian: 9', 'domain': 'mathematics'},
        {'prompt': 'What is the mode of 2, 3, 3, 5, 7, 3, 9?', 'response': 'The mode is the value that appears most frequently.\n\nValues: 2, 3, 3, 5, 7, 3, 9\n3 appears 3 times (most frequent)\nMode: 3', 'domain': 'mathematics'},
        {'prompt': 'What is the range of 5, 12, 8, 15, 3?', 'response': 'Range = Largest value - Smallest value\n\nLargest: 15\nSmallest: 3\nRange: 15 - 3 = 12', 'domain': 'mathematics'},
        {'prompt': 'What is standard deviation?', 'response': 'Standard deviation measures how spread out numbers are from the mean.\n\n**Steps:**\n1. Find mean\n2. Subtract mean from each value, square the results\n3. Find average of squared differences\n4. Take square root\n\n**Interpretation:**\n- Small SD: Data clustered near mean\n- Large SD: Data spread out', 'domain': 'mathematics'},
        
        # Number Theory
        {'prompt': 'What is a prime number?', 'response': 'A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.\n\nExamples: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...\n\nNote: 2 is the only even prime number. All other primes are odd.', 'domain': 'mathematics'},
        {'prompt': 'What is the Fibonacci sequence?', 'response': 'The Fibonacci sequence is a series where each number is the sum of the two preceding ones:\n\n0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...\n\nFormula: F(n) = F(n-1) + F(n-2)\nWith F(0) = 0 and F(1) = 1\n\nThis sequence appears throughout nature in spiral patterns, flower petals, and tree branches.', 'domain': 'mathematics'},
        {'prompt': 'What is the greatest common divisor (GCD) of 12 and 18?', 'response': 'GCD is the largest number that divides both numbers evenly.\n\nFactors of 12: 1, 2, 3, 4, 6, 12\nFactors of 18: 1, 2, 3, 6, 9, 18\nCommon factors: 1, 2, 3, 6\nGCD: 6', 'domain': 'mathematics'},
        {'prompt': 'What is the least common multiple (LCM) of 4 and 6?', 'response': 'LCM is the smallest number divisible by both numbers.\n\nMultiples of 4: 4, 8, 12, 16, 20...\nMultiples of 6: 6, 12, 18, 24...\nFirst common multiple: 12\nLCM: 12', 'domain': 'mathematics'},
        {'prompt': 'What is a perfect number?', 'response': 'A perfect number equals the sum of its proper divisors (excluding itself).\n\n**Example: 6**\nDivisors of 6: 1, 2, 3\nSum: 1 + 2 + 3 = 6 ✓\n\n**Example: 28**\nDivisors: 1, 2, 4, 7, 14\nSum: 1 + 2 + 4 + 7 + 14 = 28 ✓\n\nPerfect numbers are rare: 6, 28, 496, 8128...', 'domain': 'mathematics'}
    ]

def extract_complete_colors() -> List[Dict]:
    """Complete color theory dataset"""
    return [
        # Color Theory Basics
        {'prompt': 'What are the primary colors?', 'response': 'The primary colors depend on the color model:\n\n**Additive (Light/RGB):** Red, Green, Blue\n- Used in screens, TVs, monitors\n- Mixing all three creates white light\n\n**Subtractive (Paint/CMY):** Cyan, Magenta, Yellow\n- Used in printing and painting\n- Mixing all three creates black (in theory, brown in practice)\n\n**Traditional Art:** Red, Yellow, Blue\n- Historically taught in art classes\n- Cannot be created by mixing other colors', 'domain': 'colors'},
        {'prompt': 'What are secondary colors?', 'response': 'Secondary colors are created by mixing two primary colors:\n\n**Traditional (RYB):**\n- Red + Yellow = Orange\n- Yellow + Blue = Green\n- Blue + Red = Purple\n\n**Additive (RGB):**\n- Red + Green = Yellow\n- Green + Blue = Cyan\n- Blue + Red = Magenta\n\n**Subtractive (CMY):**\n- Cyan + Magenta = Blue\n- Magenta + Yellow = Red\n- Yellow + Cyan = Green', 'domain': 'colors'},
        {'prompt': 'What are tertiary colors?', 'response': 'Tertiary colors are made by mixing a primary and a secondary color:\n\n**Examples:**\n- Red-Orange (Vermillion)\n- Yellow-Orange (Amber)\n- Yellow-Green (Chartreuse)\n- Blue-Green (Teal)\n- Blue-Purple (Violet)\n- Red-Purple (Magenta)\n\nThese create subtle, nuanced shades.', 'domain': 'colors'},
        {'prompt': 'What color do you get when you mix red and blue?', 'response': 'Mixing red and blue creates purple (or violet).\n\n**Paint Mixing (Subtractive):**\n- Equal parts: Medium purple\n- More red: Red-purple (magenta-ish)\n- More blue: Blue-purple (violet)\n\n**Light Mixing (Additive/RGB):**\n- Red + Blue = Magenta\n\nThe exact shade depends on the specific reds and blues used.', 'domain': 'colors'},
        {'prompt': 'What color do you get when you mix red and yellow?', 'response': 'Mixing red and yellow creates orange.\n\n**Paint Mixing:**\n- Equal parts: Medium orange\n- More red: Red-orange\n- More yellow: Yellow-orange\n\n**Light Mixing (RGB):**\n- Red + Green (not yellow) = Yellow\n\nOrange is a secondary color in traditional color theory.', 'domain': 'colors'},
        {'prompt': 'What color do you get when you mix blue and yellow?', 'response': 'Mixing blue and yellow creates green.\n\n**Paint Mixing:**\n- Equal parts: Medium green\n- More blue: Blue-green (teal)\n- More yellow: Yellow-green (lime)\n\n**Light Mixing (RGB):**\n- Blue + Green = Cyan\n\nGreen is a secondary color in traditional color theory.', 'domain': 'colors'},
        {'prompt': 'What color do you get when you mix all primary colors?', 'response': '**Additive (Light - RGB):**\nRed + Green + Blue = White light\nExample: All pixels on at full brightness\n\n**Subtractive (Paint - RYB):**\nRed + Yellow + Blue = Brown/Muddy gray\nThis is why mixing too many paint colors creates mud\n\n**Subtractive (Printing - CMY):**\nCyan + Magenta + Yellow = Black (theoretical) or dark brown (practical)', 'domain': 'colors'},
        
        # Color Psychology
        {'prompt': 'What emotions does the color blue evoke?', 'response': 'Blue is associated with:\n\n**Positive:**\n- Calmness and tranquility\n- Trust and reliability\n- Professionalism and stability\n- Peace and serenity\n- Intelligence and wisdom\n\n**Context-dependent:**\n- Light blue: Peacefulness, openness\n- Dark blue: Authority, confidence\n- Bright blue: Energy, freshness\n\n**Cultural notes:**\n- Most universally liked color\n- Used by many corporations (Facebook, IBM, Ford)\n- Can evoke sadness ("feeling blue")', 'domain': 'colors'},
        {'prompt': 'What emotions does the color red evoke?', 'response': 'Red is associated with:\n\n**Positive:**\n- Passion and love\n- Energy and excitement\n- Courage and confidence\n- Power and strength\n\n**Negative/Alert:**\n- Danger and warning\n- Anger and aggression\n- Urgency and emergency\n\n**Physiological effects:**\n- Can increase heart rate\n- Stimulates appetite\n- Grabs attention quickly\n\n**Uses:** Stop signs, emergency vehicles, Valentine\'s Day', 'domain': 'colors'},
        {'prompt': 'What emotions does the color yellow evoke?', 'response': 'Yellow is associated with:\n\n**Positive:**\n- Happiness and joy\n- Optimism and energy\n- Creativity and inspiration\n- Warmth and sunshine\n\n**Negative:**\n- Caution and warning (traffic signs)\n- Anxiety (too bright/intense)\n- Cowardice (cultural)\n\n**Uses:**\n- Attention-grabbing (highlighters)\n- Cheerful branding\n- Safety equipment', 'domain': 'colors'},
        {'prompt': 'What emotions does the color green evoke?', 'response': 'Green is associated with:\n\n**Positive:**\n- Nature and growth\n- Health and freshness\n- Harmony and balance\n- Renewal and life\n- Wealth and prosperity\n\n**Negative:**\n- Envy and jealousy\n- Nausea (pale green)\n\n**Uses:**\n- Environmental brands\n- Health products\n- Financial services', 'domain': 'colors'},
        
        # Color Spaces
        {'prompt': 'What is RGB color space?', 'response': 'RGB (Red, Green, Blue) is an additive color model used for displaying colors on screens.\n\n**How it works:**\n- Three channels: Red, Green, Blue\n- Each ranges from 0-255 (8-bit)\n- Total: 16,777,216 possible colors (256³)\n\n**Examples:**\n- Red: (255, 0, 0)\n- Green: (0, 255, 0)\n- Blue: (0, 0, 255)\n- White: (255, 255, 255)\n- Black: (0, 0, 0)\n- Yellow: (255, 255, 0)\n- Cyan: (0, 255, 255)\n- Magenta: (255, 0, 255)\n\n**Uses:** Computer screens, TVs, cameras, web design', 'domain': 'colors'},
        {'prompt': 'What is HEX color code?', 'response': 'HEX (hexadecimal) color codes represent RGB colors using base-16 notation.\n\n**Format:** #RRGGBB\n- Two digits for Red (00-FF)\n- Two digits for Green (00-FF)\n- Two digits for Blue (00-FF)\n\n**Examples:**\n- #FF0000 = Red (255, 0, 0)\n- #00FF00 = Green (0, 255, 0)\n- #0000FF = Blue (0, 0, 255)\n- #FFFFFF = White\n- #000000 = Black\n- #FF00FF = Magenta\n\n**Shorthand:** #RGB = #F00 (red)', 'domain': 'colors'},
        {'prompt': 'What is CMYK color space?', 'response': 'CMYK (Cyan, Magenta, Yellow, Key/Black) is a subtractive color model used for printing.\n\n**How it works:**\n- Four inks: Cyan, Magenta, Yellow, Black\n- Each ranges from 0-100%\n- Colors subtract light (unlike RGB which adds)\n\n**Why Black (K)?**\n- Mixing C+M+Y makes muddy brown, not true black\n- Black ink produces deeper blacks\n- Saves on expensive colored ink\n\n**Uses:** Printing, offset lithography, color printing', 'domain': 'colors'},
        
        # Advanced Color Concepts
        {'prompt': 'What is the difference between violet and purple?', 'response': '**Violet:**\n- A spectral color (appears in rainbow)\n- Shortest wavelength visible (~380-450 nm)\n- Pure violet cannot be created by mixing\n- Appears on visible light spectrum\n\n**Purple:**\n- A non-spectral color\n- Created by mixing red and blue\n- Does not appear in rainbow\n- Many shades: lavender, mauve, magenta\n\n**Key difference:** Violet is pure light, purple is a mixture our brain creates.', 'domain': 'colors'},
        {'prompt': 'What is color blindness?', 'response': 'Color blindness (color vision deficiency) is decreased ability to see color or differences between colors.\n\n**Types:**\n1. **Red-Green** (most common, ~8% men, 0.5% women)\n   - Protanopia: No red cones\n   - Deuteranopia: No green cones\n\n2. **Blue-Yellow** (rare)\n   - Tritanopia: No blue cones\n\n3. **Complete** (very rare)\n   - Achromatopsia: No color vision\n\n**Causes:** Genetic (X-linked), age-related, eye diseases, medication\n\n**Impact:** Difficulty with red/green and blue/yellow combinations', 'domain': 'colors'},
        {'prompt': 'What are complementary colors?', 'response': 'Complementary colors are opposite each other on the color wheel.\n\n**Primary complementary pairs:**\n- Red ↔ Green\n- Blue ↔ Orange\n- Yellow ↔ Purple\n\n**Properties:**\n- Create maximum contrast\n- Make each other appear brighter\n- Mix to create gray/brown\n- Used for visual pop in design\n\n**Examples in nature:**\n- Red strawberries on green leaves\n- Orange sunset against blue sky', 'domain': 'colors'},
        {'prompt': 'What are analogous colors?', 'response': 'Analogous colors are next to each other on the color wheel.\n\n**Examples:**\n- Red, Red-Orange, Orange\n- Blue, Blue-Green, Green\n- Yellow, Yellow-Green, Green\n\n**Properties:**\n- Create harmony and unity\n- Easy on the eyes\n- One color dominates, others support\n- Common in nature\n\n**Uses:**\n- Creating calm, comfortable designs\n- Nature photography\n- Seasonal color palettes', 'domain': 'colors'}
    ]

def save_comprehensive_datasets():
    """Save all comprehensive extracted datasets"""
    print("\n" + "="*80)
    print("📦 COMPREHENSIVE TEMPLATE EXTRACTION - ALL EXAMPLES")
    print("="*80)
    print("\nExtracting EVERYTHING from your provided templates...\n")
    
    datasets = {
        'mathematics': extract_complete_mathematics(),
        'colors': extract_complete_colors(),
        # More to add after this batch
    }
    
    total_new = 0
    for domain, examples in datasets.items():
        domain_dir = f'datasets/{domain}'
        os.makedirs(domain_dir, exist_ok=True)
        
        filepath = f'{domain_dir}/knowledge.json'
        
        # Merge with existing
        existing = []
        if os.path.exists(filepath):
            try:
                with open(filepath) as f:
                    existing = json.load(f)
                    if not isinstance(existing, list):
                        existing = []
            except:
                existing = []
        
        # Deduplicate
        all_examples = existing + examples
        unique_examples = []
        seen = set()
        for ex in all_examples:
            key = ex.get('prompt', '')
            if key not in seen:
                seen.add(key)
                unique_examples.append(ex)
        
        with open(filepath, 'w') as f:
            json.dump(unique_examples, f, indent=2)
        
        new_count = len(unique_examples) - len(existing)
        total_new += new_count
        print(f"✅ {domain}: +{new_count} new (total: {len(unique_examples)})")
    
    print(f"\n{'='*80}")
    print(f"🎉 Phase 1 Complete: Added {total_new} examples")
    print(f"💰 Cost: $0.00 (FREE extraction)")
    print(f"\n📝 Note: More domains coming in next phases...")
    print(f"{'='*80}")
    
    return total_new

if __name__ == "__main__":
    save_comprehensive_datasets()
