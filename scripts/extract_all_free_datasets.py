#!/usr/bin/env python3
"""
Comprehensive FREE Dataset Extractor
Extracts ALL curated examples from template guides
ZERO cost - pure extraction
"""

import json
import os
from typing import List, Dict

def extract_all_mathematics() -> List[Dict]:
    """Extract comprehensive mathematics examples"""
    return [
        # Arithmetic
        {'prompt': 'What is 247 + 389?', 'response': '247 + 389 = 636', 'domain': 'mathematics'},
        {'prompt': 'What is 15 × 23?', 'response': '15 × 23 = 345', 'domain': 'mathematics'},
        {'prompt': 'What is 144 ÷ 12?', 'response': '144 ÷ 12 = 12', 'domain': 'mathematics'},
        {'prompt': 'What is 456 - 189?', 'response': '456 - 189 = 267', 'domain': 'mathematics'},
        {'prompt': 'What is 25% of 80?', 'response': '25% of 80 = 0.25 × 80 = 20', 'domain': 'mathematics'},
        
        # Algebra
        {'prompt': 'Solve for x: 2x + 5 = 13', 'response': 'To solve 2x + 5 = 13:\n1. Subtract 5 from both sides: 2x = 8\n2. Divide both sides by 2: x = 4\nAnswer: x = 4', 'domain': 'mathematics'},
        {'prompt': 'Solve the quadratic equation: x² - 5x + 6 = 0', 'response': 'To solve x² - 5x + 6 = 0:\nMethod 1 (Factoring): (x - 2)(x - 3) = 0\nTherefore: x = 2 or x = 3\n\nMethod 2 (Quadratic formula): x = (5 ± √(25-24))/2 = (5 ± 1)/2\nx = 3 or x = 2', 'domain': 'mathematics'},
        {'prompt': 'Solve for y: 3y - 7 = 14', 'response': 'To solve 3y - 7 = 14:\n1. Add 7 to both sides: 3y = 21\n2. Divide both sides by 3: y = 7\nAnswer: y = 7', 'domain': 'mathematics'},
        
        # Geometry
        {'prompt': 'What is the area of a circle with radius 5?', 'response': 'The area of a circle is A = πr²\nWith radius r = 5:\nA = π(5)² = 25π ≈ 78.54 square units', 'domain': 'mathematics'},
        {'prompt': 'What is the Pythagorean theorem?', 'response': 'The Pythagorean theorem states that in a right triangle, the square of the hypotenuse (c) equals the sum of squares of the other two sides (a and b):\n\na² + b² = c²\n\nExample: If a = 3 and b = 4, then c² = 9 + 16 = 25, so c = 5', 'domain': 'mathematics'},
        {'prompt': 'What is the perimeter of a rectangle with length 8 and width 5?', 'response': 'Perimeter of rectangle = 2(length + width)\nP = 2(8 + 5) = 2(13) = 26 units', 'domain': 'mathematics'},
        {'prompt': 'What is the volume of a cube with side length 4?', 'response': 'Volume of cube = side³\nV = 4³ = 4 × 4 × 4 = 64 cubic units', 'domain': 'mathematics'},
        
        # Calculus
        {'prompt': 'What is the derivative of x²?', 'response': 'The derivative of x² with respect to x is 2x.\n\nUsing the power rule: d/dx(xⁿ) = nxⁿ⁻¹\nFor x²: d/dx(x²) = 2x²⁻¹ = 2x', 'domain': 'mathematics'},
        {'prompt': 'What is the integral of 2x?', 'response': 'The integral of 2x with respect to x is x² + C (where C is the constant of integration).\n\n∫2x dx = x² + C\n\nUsing the power rule for integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C', 'domain': 'mathematics'},
        {'prompt': 'What is the derivative of 3x³?', 'response': 'Using the power rule: d/dx(xⁿ) = nxⁿ⁻¹\nFor 3x³: d/dx(3x³) = 3 × 3x² = 9x²', 'domain': 'mathematics'},
        
        # Statistics
        {'prompt': 'What is the mean of 3, 7, 9, 12, 15?', 'response': 'The mean (average) is the sum divided by the count.\n\nSum: 3 + 7 + 9 + 12 + 15 = 46\nCount: 5\nMean: 46 ÷ 5 = 9.2', 'domain': 'mathematics'},
        {'prompt': 'What is the median of 3, 7, 9, 12, 15?', 'response': 'The median is the middle value when numbers are arranged in order.\n\nOrdered: 3, 7, 9, 12, 15\nMiddle position: 3rd number\nMedian: 9', 'domain': 'mathematics'},
        {'prompt': 'What is the mode of 2, 3, 3, 5, 7, 3, 9?', 'response': 'The mode is the value that appears most frequently.\n\nValues: 2, 3, 3, 5, 7, 3, 9\n3 appears 3 times (most frequent)\nMode: 3', 'domain': 'mathematics'},
        {'prompt': 'What is the range of 5, 12, 8, 15, 3?', 'response': 'Range = Largest value - Smallest value\n\nLargest: 15\nSmallest: 3\nRange: 15 - 3 = 12', 'domain': 'mathematics'},
        
        # Number Theory
        {'prompt': 'What is a prime number?', 'response': 'A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.\n\nExamples: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...\n\nNote: 2 is the only even prime number. All other primes are odd.', 'domain': 'mathematics'},
        {'prompt': 'What is the Fibonacci sequence?', 'response': 'The Fibonacci sequence is a series where each number is the sum of the two preceding ones:\n\n0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...\n\nFormula: F(n) = F(n-1) + F(n-2)\nWith F(0) = 0 and F(1) = 1\n\nThis sequence appears throughout nature in spiral patterns, flower petals, and tree branches.', 'domain': 'mathematics'},
        {'prompt': 'What is the greatest common divisor (GCD) of 12 and 18?', 'response': 'GCD is the largest number that divides both numbers evenly.\n\nFactors of 12: 1, 2, 3, 4, 6, 12\nFactors of 18: 1, 2, 3, 6, 9, 18\nCommon factors: 1, 2, 3, 6\nGCD: 6', 'domain': 'mathematics'},
        {'prompt': 'What is the least common multiple (LCM) of 4 and 6?', 'response': 'LCM is the smallest number divisible by both numbers.\n\nMultiples of 4: 4, 8, 12, 16, 20...\nMultiples of 6: 6, 12, 18, 24...\nFirst common multiple: 12\nLCM: 12', 'domain': 'mathematics'}
    ]

def extract_all_colors() -> List[Dict]:
    """Extract comprehensive color theory examples"""
    return [
        {'prompt': 'What are the primary colors?', 'response': 'The primary colors depend on the color model:\n\n**Additive (Light/RGB):** Red, Green, Blue\n- Used in screens, TVs, monitors\n- Mixing all three creates white light\n\n**Subtractive (Paint/CMY):** Cyan, Magenta, Yellow\n- Used in printing and painting\n- Mixing all three creates black (in theory, brown in practice)\n\n**Traditional Art:** Red, Yellow, Blue\n- Historically taught in art classes\n- Cannot be created by mixing other colors', 'domain': 'colors'},
        {'prompt': 'What color do you get when you mix red and blue?', 'response': 'Mixing red and blue creates purple (or violet).\n\n**Paint Mixing (Subtractive):**\n- Equal parts: Medium purple\n- More red: Red-purple (magenta-ish)\n- More blue: Blue-purple (violet)\n\n**Light Mixing (Additive/RGB):**\n- Red + Blue = Magenta\n\nThe exact shade depends on the specific reds and blues used.', 'domain': 'colors'},
        {'prompt': 'What color do you get when you mix red and yellow?', 'response': 'Mixing red and yellow creates orange.\n\n**Paint Mixing:**\n- Equal parts: Medium orange\n- More red: Red-orange\n- More yellow: Yellow-orange\n\n**Light Mixing (RGB):**\n- Red + Green (not yellow) = Yellow\n\nOrange is a secondary color in traditional color theory.', 'domain': 'colors'},
        {'prompt': 'What color do you get when you mix blue and yellow?', 'response': 'Mixing blue and yellow creates green.\n\n**Paint Mixing:**\n- Equal parts: Medium green\n- More blue: Blue-green (teal)\n- More yellow: Yellow-green (lime)\n\n**Light Mixing (RGB):**\n- Blue + Green = Cyan\n\nGreen is a secondary color in traditional color theory.', 'domain': 'colors'},
        {'prompt': 'What emotions does the color blue evoke?', 'response': 'Blue is associated with:\n\n**Positive:**\n- Calmness and tranquility\n- Trust and reliability\n- Professionalism and stability\n- Peace and serenity\n- Intelligence and wisdom\n\n**Context-dependent:**\n- Light blue: Peacefulness, openness\n- Dark blue: Authority, confidence\n- Bright blue: Energy, freshness\n\n**Cultural notes:**\n- Most universally liked color\n- Used by many corporations (Facebook, IBM, Ford)\n- Can evoke sadness in some contexts ("feeling blue")', 'domain': 'colors'},
        {'prompt': 'What emotions does the color red evoke?', 'response': 'Red is associated with:\n\n**Positive:**\n- Passion and love\n- Energy and excitement\n- Courage and confidence\n- Power and strength\n\n**Negative/Alert:**\n- Danger and warning\n- Anger and aggression\n- Urgency and emergency\n\n**Physiological effects:**\n- Can increase heart rate\n- Stimulates appetite\n- Grabs attention quickly\n\n**Cultural uses:**\n- Stop signs, emergency vehicles\n- Valentine\'s Day, passion\n- Power ties in business', 'domain': 'colors'},
        {'prompt': 'What is RGB color space?', 'response': 'RGB (Red, Green, Blue) is an additive color model used for displaying colors on screens.\n\n**How it works:**\n- Three channels: Red, Green, Blue\n- Each ranges from 0-255 (8-bit)\n- Total: 16,777,216 possible colors (256³)\n\n**Examples:**\n- Red: (255, 0, 0)\n- Green: (0, 255, 0)\n- Blue: (0, 0, 255)\n- White: (255, 255, 255)\n- Black: (0, 0, 0)\n- Yellow: (255, 255, 0)\n- Cyan: (0, 255, 255)\n- Magenta: (255, 0, 255)\n\n**Uses:** Computer screens, TVs, cameras, web design', 'domain': 'colors'},
        {'prompt': 'What is HEX color code?', 'response': 'HEX (hexadecimal) color codes represent RGB colors using base-16 notation.\n\n**Format:** #RRGGBB\n- Two digits for Red (00-FF)\n- Two digits for Green (00-FF)\n- Two digits for Blue (00-FF)\n\n**Examples:**\n- #FF0000 = Red (255, 0, 0)\n- #00FF00 = Green (0, 255, 0)\n- #0000FF = Blue (0, 0, 255)\n- #FFFFFF = White\n- #000000 = Black\n- #FF00FF = Magenta\n\n**Shorthand:** #RGB = #F00 (red)', 'domain': 'colors'},
        {'prompt': 'What is the difference between violet and purple?', 'response': '**Violet:**\n- A spectral color (appears in rainbow)\n- Shortest wavelength visible (~380-450 nm)\n- Pure violet cannot be created by mixing\n- Appears on visible light spectrum\n\n**Purple:**\n- A non-spectral color\n- Created by mixing red and blue\n- Does not appear in rainbow\n- Many shades: lavender, mauve, magenta\n\n**Key difference:** Violet is pure light, purple is a mixture our brain creates.', 'domain': 'colors'},
        {'prompt': 'What is color blindness?', 'response': 'Color blindness (color vision deficiency) is decreased ability to see color or differences between colors.\n\n**Types:**\n1. **Red-Green** (most common, ~8% men, 0.5% women)\n   - Protanopia: No red cones\n   - Deuteranopia: No green cones\n\n2. **Blue-Yellow** (rare)\n   - Tritanopia: No blue cones\n\n3. **Complete** (very rare)\n   - Achromatopsia: No color vision\n\n**Causes:** Genetic (X-linked), age-related, eye diseases, medication\n\n**Impact:** Difficulty with red/green and blue/yellow combinations', 'domain': 'colors'}
    ]

def extract_children_education() -> List[Dict]:
    """Extract children's education examples"""
    return [
        # Early Childhood
        {'prompt': 'What should a 2-year-old be able to do?', 'response': '**Typical milestones for 2-year-olds:**\n\n**Physical:**\n- Walk and run steadily\n- Climb furniture\n- Kick and throw ball\n- Stack 4+ blocks\n\n**Language:**\n- Say 50+ words\n- Combine 2 words ("more juice")\n- Follow simple instructions\n\n**Social/Emotional:**\n- Show affection\n- Play alongside others\n- Show defiance (saying "no")\n\n**Cognitive:**\n- Find hidden objects\n- Sort shapes/colors\n- Begin pretend play\n\n**Note:** Every child develops at their own pace. Consult pediatrician if concerned.', 'domain': 'kids_education'},
        
        {'prompt': 'What activities are good for 3-year-olds?', 'response': '**Great activities for 3-year-olds:**\n\n**Physical:** Obstacle courses, dancing, ball games, tricycle, playground\n\n**Fine Motor:** Playdough, coloring, building blocks, 4-8 piece puzzles, stringing beads\n\n**Cognitive:** Sorting games (colors/shapes), counting, matching games, simple board games\n\n**Language:** Reading (20 min daily), singing songs, storytelling, pretend play\n\n**Social/Emotional:** Playdates, role-playing, emotion recognition, helping with chores\n\n**Screen time:** Limit to 1 hour/day of high-quality programming', 'domain': 'kids_education'},
        
        {'prompt': 'How do I teach my 4-year-old the alphabet?', 'response': '**Fun ways to teach the alphabet:**\n\n**1. Alphabet Song**\n- Sing daily, point to letters, use visual charts\n\n**2. Hands-on Activities**\n- Alphabet puzzles, magnetic letters, letter blocks, playdough letters\n\n**3. Letter Sounds (Phonics)**\n- Start with their name\n- "A says /a/ like apple"\n- Find objects that start with each letter\n\n**4. Writing Practice**\n- Start with their name\n- Trace letters, then draw\n- Celebrate attempts!\n\n**5. Make it Fun!**\n- Hunt for letters on signs\n- Letter of the week\n- Alphabet crafts\n\n**6. Read Together**\n- 20 minutes daily\n- Point to words\n- Ask "What letter is that?"\n\n**Timeline:** Most recognize 10-15 letters by age 4, all 26 by age 5', 'domain': 'kids_education'},
        
        # Elementary
        {'prompt': 'Can you help me with my multiplication tables?', 'response': "**Let's learn multiplication tables!**\n\n**Understanding:** Multiplication is repeated addition!\n- 3 × 4 means '3 groups of 4' = 12\n\n**Easy tricks:**\n- ×0: Always 0\n- ×1: Same number\n- ×2: Double it!\n- ×5: Ends in 0 or 5\n- ×9: Finger trick!\n- ×10: Add a zero\n- ×11: Repeat digit (11×3=33)\n\n**Practice:**\n- Flash cards daily\n- Skip counting\n- Math games online\n- Multiplication songs\n\n**Remember:** Order doesn't matter! 3×4 = 4×3", 'domain': 'kids_education'},
        
        {'prompt': 'How can I improve my reading?', 'response': '**Tips to become a better reader:**\n\n**1. Read Every Day** (20-30 minutes)\n\n**2. Choose the Right Books**\n- Just right: Know most words, learn a few new ones\n\n**3. Reading Strategies**\n- Before: Look at cover, predict\n- During: Sound out words, visualize, ask questions\n- After: Summarize, discuss\n\n**4. Build Vocabulary**\n- Keep a "new words" notebook\n- Use new words in sentences\n\n**5. Find Your Reading Spot**\n- Quiet, comfortable, good lighting\n\n**6. Try Different Genres**\n- Adventure, mystery, fantasy, graphic novels, comics, nonfiction\n\n**7. Activities**\n- Join reading challenges\n- Get library card\n- Listen to audiobooks while reading\n- Read to younger siblings/pets\n\n**Remember:** The more you read, the better you get!', 'domain': 'kids_education'},
        
        {'prompt': 'Why do leaves change color in fall?', 'response': '**The Science of Fall Colors!**\n\n**Summer:** Leaves have chlorophyll (makes them GREEN)\n- Chlorophyll helps make food (photosynthesis)\n\n**Fall happens:**\n1. Days get shorter, less sunlight\n2. Trees stop making chlorophyll\n3. Green fades away\n4. Hidden colors appear!\n\n**The Colors:**\n- 🟡 Yellow (always there, now visible)\n- 🟠 Orange (same as carrots!)\n- 🔴 Red (made NEW in fall)\n- 🟤 Brown (waste products)\n\n**Why leaves fall:**\n- Tree seals off connection\n- Saves energy for winter\n\n**Best colors:** Sunny days + cool nights!\n\n**Try this:** Collect different colored leaves, press in book, make chart!', 'domain': 'kids_education'},
        
        {'prompt': 'What should I do if someone is bullying me?', 'response': '**If someone is bullying you:**\n\n**Remember: Bullying is NEVER your fault.**\n\n**Types:** Physical, verbal, social, cyber\n\n**What to Do:**\n\n**1. Stay Safe**\n- Get away if in danger\n- Go to trusted adult\n\n**2. Use Your Words** (if safe)\n- Say firmly: "Stop. I don\'t like that."\n- Walk away with confidence\n\n**3. TELL AN ADULT** (NOT tattling!)\n- Parent, teacher, counselor, principal\n- Keep telling until someone helps!\n\n**4. Document It**\n- Write down what happened (date, time, place)\n- Save mean messages\n\n**5. Protect Yourself**\n- Stay near friends/adults\n- Block them online\n\n**Resources:**\n- StopBullying.gov\n- Crisis Text Line: Text HELLO to 741741\n- School counselor\n\n**You are brave for speaking up!**', 'domain': 'kids_education'},
        
        {'prompt': 'How do I study for a test?', 'response': '**Study Strategies That Work!**\n\n**Schedule:**\n- 1 Week Before: Review all material\n- 3-4 Days Before: Study 20-30 min daily, focus on hard topics\n- 1 Day Before: Quick review, good sleep (8-10 hours!)\n- Test Day: Eat breakfast, review briefly, stay calm\n\n**Techniques:**\n\n**1. Flashcards** - Question on front, answer on back\n\n**2. Teaching Method** - Explain out loud to parent/pet/stuffed animal\n\n**3. Practice Problems** - Do examples, time yourself\n\n**4. Color Coding** - Highlighters for main ideas, details, vocabulary\n\n**5. Memory Tricks**\n- Acronyms: HOMES = Great Lakes\n- Rhymes: "I before E except after C"\n- Make up silly stories\n\n**6. Study Games** - Quiz friends, make songs, online games\n\n**Tips:**\n- Quiet study spot\n- Take breaks every 20-30 min\n- Snacks and water\n- No cramming last minute!', 'domain': 'kids_education'}
    ]

def extract_plants_botany() -> List[Dict]:
    """Extract plant/botany examples"""
    return [
        {'prompt': 'What is photosynthesis?', 'response': 'Photosynthesis is the process by which plants convert light energy into chemical energy (glucose).\n\n**Equation:** 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂\n\n**Process:**\n1. Plants absorb sunlight through chlorophyll\n2. Light energy splits water molecules\n3. CO₂ combines with hydrogen\n4. Produces glucose and releases oxygen\n\n**Importance:**\n- Produces oxygen we breathe\n- Creates food for plants\n- Base of food chains\n- Removes CO₂ from atmosphere', 'domain': 'plants_botany'},
        
        {'prompt': 'What are the main parts of a plant?', 'response': 'Plants have several key parts:\n\n**1. Roots**\n- Anchor plant in soil\n- Absorb water and nutrients\n- Store food (in some plants)\n\n**2. Stem**\n- Supports leaves and flowers\n- Transports water and nutrients\n- Stores food (in some plants)\n\n**3. Leaves**\n- Perform photosynthesis\n- Gas exchange (O₂ and CO₂)\n- Transpiration (water loss)\n\n**4. Flowers** (in flowering plants)\n- Reproductive structures\n- Produce seeds\n- Attract pollinators\n\n**5. Seeds/Fruit**\n- Contain embryo\n- Enable reproduction\n- Protect and disperse offspring', 'domain': 'plants_botany'},
        
        {'prompt': 'How do I care for a snake plant?', 'response': 'Snake Plant (Sansevieria) - easiest houseplant!\n\n**Light:** Low to bright indirect (very tolerant)\n\n**Water:** Every 2-3 weeks, let soil dry completely\n- Overwatering is the main killer!\n- Less water in winter\n\n**Soil:** Well-draining cactus/succulent mix\n\n**Temperature:** 60-85°F (15-29°C)\n\n**Benefits:**\n- Purifies air (removes toxins)\n- Produces oxygen at night\n- Nearly indestructible\n\n**Perfect for:** Beginners, low-light spaces, forgetful waterers!', 'domain': 'plants_botany'},
        
        {'prompt': 'How do I grow tomatoes?', 'response': 'Growing tomatoes successfully:\n\n**Starting:**\n- Start seeds indoors 6-8 weeks before last frost\n- Or buy seedlings from nursery\n\n**Planting:**\n- Full sun (6-8 hours daily)\n- Rich, well-draining soil (pH 6.0-6.8)\n- Space 24-36 inches apart\n- Plant deep (bury stem up to first leaves)\n\n**Care:**\n- Water deeply (1-2 inches per week)\n- Mulch around plants\n- Fertilize every 2-3 weeks\n- Stake or cage for support\n- Prune suckers for bigger fruit\n\n**Harvest:**\n- Pick when fully colored\n- 60-85 days from transplanting\n- Store on counter, not fridge\n\n**Common issues:**\n- Blossom end rot: Add calcium, water consistently\n- Hornworms: Hand pick', 'domain': 'plants_botany'},
        
        {'prompt': 'What is the difference between annuals and perennials?', 'response': '**Annual Plants:**\n- Complete life cycle in one year\n- Germinate, grow, flower, seed, die\n- Must replant each year\n- Examples: marigolds, zinnias, tomatoes, basil\n- Longer flowering periods\n- Good for: seasonal color, vegetables\n\n**Perennial Plants:**\n- Live for multiple years (3+ years)\n- Die back in winter, regrow in spring\n- Establish root systems that survive winter\n- Examples: hostas, daylilies, lavender, strawberries\n- Lower maintenance after establishment\n- Good for: permanent landscape, less replanting\n\n**Biennials** (bonus):\n- Two-year life cycle\n- Year 1: vegetative growth\n- Year 2: flower, seed, die\n- Examples: carrots, parsley, foxglove', 'domain': 'plants_botany'}
    ]

def extract_earth_science() -> List[Dict]:
    """Extract earth science examples"""
    return [
        {'prompt': 'What are the layers of the Earth?', 'response': 'Earth has four main layers:\n\n**1. Crust** (outermost)\n- Thickness: 5-70 km\n- Two types: oceanic (thinner) and continental (thicker)\n- What we live on\n\n**2. Mantle**\n- Thickness: ~2,900 km\n- Semi-solid rock that flows slowly\n- Contains most of Earth\'s mass\n- Temperature: 500-4,000°C\n- Convection currents drive plate tectonics\n\n**3. Outer Core**\n- Thickness: ~2,200 km\n- Liquid iron and nickel\n- Temperature: 4,000-6,000°C\n- Movement creates Earth\'s magnetic field\n\n**4. Inner Core** (center)\n- Radius: ~1,220 km\n- Solid iron and nickel\n- Temperature: 5,000-7,000°C (hot as sun\'s surface!)\n- Solid despite heat due to extreme pressure', 'domain': 'earth_science'},
        
        {'prompt': 'How do earthquakes happen?', 'response': 'Earthquakes occur when stress in Earth\'s crust is released:\n\n**Causes:**\n1. **Tectonic plates moving** (most common)\n   - Plates collide, separate, or slide past each other\n   - Stress builds up along faults\n   - Rock suddenly breaks, releases energy\n\n2. **Volcanic activity**\n   - Magma movement creates tremors\n\n3. **Human activity** (rare)\n   - Mining, reservoir filling, fracking\n\n**Process:**\n1. Stress accumulates along fault line\n2. Rock reaches breaking point\n3. Sudden rupture releases energy as seismic waves\n4. Waves travel through Earth, cause shaking\n\n**Measurement:**\n- Magnitude: Richter or Moment Magnitude Scale (energy released)\n- Intensity: Modified Mercalli Scale (damage/effects)\n\n**Safety:** Drop, Cover, Hold On during earthquake', 'domain': 'earth_science'},
        
        {'prompt': 'How does the water cycle work?', 'response': 'The water cycle is continuous movement of water on, above, and below Earth\'s surface:\n\n**Steps:**\n\n**1. Evaporation**\n- Sun heats water in oceans, lakes, rivers\n- Liquid water becomes water vapor (gas)\n- Rises into atmosphere\n\n**2. Transpiration**\n- Plants release water vapor through leaves\n- Combines with evaporation\n\n**3. Condensation**\n- Water vapor cools in atmosphere\n- Forms tiny water droplets\n- Creates clouds and fog\n\n**4. Precipitation**\n- Droplets combine, get heavy\n- Fall as rain, snow, sleet, hail\n\n**5. Collection**\n- Water collects in oceans, lakes, rivers, groundwater\n- Cycle begins again\n\n**Importance:**\n- Provides fresh water\n- Regulates climate\n- Distributes heat around globe', 'domain': 'earth_science'}
    ]

def save_all_free_datasets():
    """Save all extracted free examples"""
    print("\n" + "="*70)
    print("📦 EXTRACTING ALL FREE DATASETS FROM TEMPLATES")
    print("="*70)
    print("\nZERO cost - pure extraction from curated examples\n")
    
    datasets = {
        'mathematics': extract_all_mathematics(),
        'colors': extract_all_colors(),
        'kids_education': extract_children_education(),
        'plants_botany': extract_plants_botany(),
        'earth_science': extract_earth_science()
    }
    
    total = 0
    for domain, examples in datasets.items():
        domain_dir = f'datasets/{domain}'
        os.makedirs(domain_dir, exist_ok=True)
        
        filepath = f'{domain_dir}/knowledge.json'
        
        # Merge with existing if present
        existing = []
        if os.path.exists(filepath):
            try:
                with open(filepath) as f:
                    existing = json.load(f)
                    if not isinstance(existing, list):
                        existing = []
            except:
                existing = []
        
        # Combine and deduplicate
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
        print(f"✅ {domain}: +{new_count} new examples (total: {len(unique_examples)})")
        total += new_count
    
    print(f"\n{'='*70}")
    print(f"🎉 Extracted {total} NEW high-quality examples")
    print(f"💰 Cost: $0.00 (100% FREE extraction)")
    print(f"{'='*70}")
    
    return total

if __name__ == "__main__":
    total = save_all_free_datasets()
    
    # Count final totals
    print(f"\n📊 FINAL DATASET STATUS")
    print(f"="*70)
    
    grand_total = 0
    domains = {}
    for root, dirs, files in os.walk('datasets'):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath) as f:
                        data = json.load(f)
                        count = len(data) if isinstance(data, list) else len(data.get('examples', []))
                        domain = os.path.basename(root)
                        domains[domain] = count
                        grand_total += count
                except:
                    pass
    
    print(f"\n✨ **Total Examples: {grand_total:,}**")
    print(f"✨ **Total Domains: {len(domains)}**")
    print(f"\nAll domains:")
    for domain in sorted(domains.keys()):
        print(f"  • {domain}: {domains[domain]} examples")
