#!/usr/bin/env python3
"""
COMPLETE FREE DATASET INTEGRATION
1. Download GoEmotions (58k examples from Google)
2. Extract ALL template examples (children's ed, science, etc.)
"""

import requests
import json
import os
from typing import List, Dict
import time

# ==================== GO EMOTIONS (GOOGLE) ====================

def download_goemotions() -> List[Dict]:
    """Download GoEmotions dataset from GitHub"""
    print("\n📥 Downloading GoEmotions (58k emotion examples from Google)...")
    
    urls = {
        'train': 'https://raw.githubusercontent.com/google-research/google-research/master/goemotions/data/train.tsv',
        'dev': 'https://raw.githubusercontent.com/google-research/google-research/master/goemotions/data/dev.tsv',
        'test': 'https://raw.githubusercontent.com/google-research/google-research/master/goemotions/data/test.tsv'
    }
    
    emotions = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 
               'caring', 'confusion', 'curiosity', 'desire', 'disappointment',
               'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear',
               'gratitude', 'grief', 'joy', 'love', 'nervousness', 'optimism',
               'pride', 'realization', 'relief', 'remorse', 'sadness', 'surprise']
    
    all_examples = []
    
    for split, url in urls.items():
        print(f"  Downloading {split}...", end=' ', flush=True)
        
        try:
            response = requests.get(url, timeout=60)
            
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                
                for line in lines[1:]:  # Skip header
                    parts = line.split('\t')
                    if len(parts) >= 29:
                        text = parts[0]
                        emotion_vals = parts[1:28]
                        
                        active_emotions = []
                        for i, val in enumerate(emotion_vals):
                            if val == '1':
                                active_emotions.append(emotions[i])
                        
                        if active_emotions and text.strip():
                            all_examples.append({
                                'prompt': f"What emotion is expressed in: '{text}'",
                                'response': f"This text expresses {', '.join(active_emotions)}. The primary emotion is {active_emotions[0]}.",
                                'domain': 'emotion_detection',
                                'emotions': active_emotions,
                                'text': text
                            })
                
                print(f"✓ ({len(all_examples)} total so far)")
            else:
                print(f"✗ HTTP {response.status_code}")
        
        except Exception as e:
            print(f"✗ Error: {e}")
    
    return all_examples

# ==================== CHILDREN'S EDUCATION (ALL AGES) ====================

def extract_childrens_education_complete() -> List[Dict]:
    """Complete children's education dataset (ages 0-18)"""
    return [
        # Early Childhood (0-5)
        {'prompt': 'What should a 2-year-old be able to do?', 'response': '**Typical milestones for 2-year-olds:**\n\n**Physical:**\n- Walk and run steadily\n- Climb furniture\n- Kick and throw ball\n- Stack 4+ blocks\n\n**Language:**\n- Say 50+ words\n- Combine 2 words\n- Follow simple instructions\n\n**Social/Emotional:**\n- Show affection\n- Play alongside others\n- Show defiance\n\n**Cognitive:**\n- Find hidden objects\n- Sort shapes/colors\n- Begin pretend play\n\n**Note:** Every child develops at their own pace.', 'domain': 'kids_education'},
        
        {'prompt': 'What activities are good for 3-year-olds?', 'response': '**Activities for 3-year-olds:**\n\n**Physical:** Obstacle courses, dancing, ball games, tricycle, playground\n\n**Fine Motor:** Playdough, coloring, blocks, puzzles, stringing beads\n\n**Cognitive:** Sorting games, counting, matching, simple board games\n\n**Language:** Reading (20 min daily), singing, storytelling, pretend play\n\n**Social/Emotional:** Playdates, role-playing, emotion recognition\n\n**Screen time:** Max 1 hour/day high-quality programming', 'domain': 'kids_education'},
        
        {'prompt': 'How do I teach my 4-year-old the alphabet?', 'response': '**Teaching the alphabet:**\n\n**1. Alphabet Song** - Sing daily, point to letters\n\n**2. Hands-on:** Puzzles, magnetic letters, playdough letters\n\n**3. Letter Sounds:** Start with their name, "A says /a/ like apple"\n\n**4. Writing:** Start with their name, trace then draw\n\n**5. Make it Fun:** Letter hunts, crafts, alphabet snacks\n\n**6. Read Together:** 20 min daily, point to words\n\n**Timeline:** Most recognize 10-15 letters by age 4, all 26 by age 5', 'domain': 'kids_education'},
        
        {'prompt': 'How do I handle tantrums in a 3-year-old?', 'response': '**Managing tantrums:**\n\n**Why they happen:** Limited language, testing boundaries, tired/hungry, big emotions\n\n**Prevention:** Consistent routines, adequate sleep, regular meals, give choices, prepare for transitions\n\n**During tantrum:**\n- Stay calm (deep breaths)\n- Ensure safety\n- Don\'t give in to demands\n- Acknowledge feelings: "I see you\'re angry"\n- Wait it out patiently\n\n**After:**\n- Offer comfort\n- Help name emotion\n- Teach better coping\n- Follow through with boundary\n\n**Seek help if:** Increasing after age 4, child hurts self/others, lasts >15 min regularly', 'domain': 'kids_education'},
        
        # Elementary (6-11)
        {'prompt': 'Can you help me with my multiplication tables?', 'response': "**Learning multiplication tables:**\n\n**Understanding:** Multiplication is repeated addition! 3×4 = '3 groups of 4' = 12\n\n**Easy tricks:**\n- ×0: Always 0\n- ×1: Same number\n- ×2: Double it!\n- ×5: Ends in 0 or 5\n- ×9: Finger trick!\n- ×10: Add a zero\n- ×11: Repeat digit (11×3=33)\n\n**Practice:** Flash cards daily, skip counting, math games, multiplication songs\n\n**Remember:** Order doesn't matter! 3×4 = 4×3", 'domain': 'kids_education'},
        
        {'prompt': 'How can I improve my reading?', 'response': '**Becoming a better reader:**\n\n**1. Read Daily:** 20-30 minutes\n\n**2. Choose Right Books:** "Just right" = know most words, learn a few new ones\n\n**3. Strategies:**\n- Before: Preview, predict\n- During: Sound out words, visualize, ask questions\n- After: Summarize, discuss\n\n**4. Build Vocabulary:** Keep "new words" notebook\n\n**5. Reading Spot:** Quiet, comfortable, good lighting\n\n**6. Try Genres:** Adventure, mystery, fantasy, graphic novels, nonfiction\n\n**7. Activities:** Reading challenges, library card, audiobooks, buddy reading\n\n**The more you read, the better you get!**', 'domain': 'kids_education'},
        
        {'prompt': 'Why do leaves change color in fall?', 'response': '**Fall leaf colors explained:**\n\n**Summer:** Chlorophyll (GREEN) makes food via photosynthesis\n\n**Fall:**\n1. Days get shorter → less sunlight\n2. Trees stop making chlorophyll\n3. Green fades\n4. Hidden colors appear!\n\n**The Colors:**\n- 🟡 Yellow (always there, now visible)\n- 🟠 Orange (same pigment as carrots!)\n- 🔴 Red (made NEW in fall from trapped sugars)\n- 🟤 Brown (waste products)\n\n**Why leaves fall:** Tree seals connection, saves energy for winter\n\n**Best colors:** Sunny days + cool nights!\n\n**Activity:** Collect leaves, press in book, make chart!', 'domain': 'kids_education'},
        
        {'prompt': 'What should I do if someone is bullying me?', 'response': '**If being bullied:**\n\n**Remember: NOT your fault!**\n\n**Types:** Physical, verbal, social, cyber\n\n**What to Do:**\n\n**1. Stay Safe** - Get away if danger, go to trusted adult\n\n**2. Use Words (if safe)** - Say firmly: "Stop. I don\'t like that." Walk away\n\n**3. TELL ADULT** (NOT tattling!)\n- Parent, teacher, counselor, principal\n- Keep telling until someone helps!\n\n**4. Document:** Write what happened (date, time, place), save messages\n\n**5. Protect Yourself:** Stay near friends/adults, block online\n\n**Resources:**\n- StopBullying.gov\n- Crisis Text: HELLO to 741741\n- School counselor\n\n**You are brave for speaking up!**', 'domain': 'kids_education'},
        
        {'prompt': 'How do I study for a test?', 'response': '**Study strategies:**\n\n**Schedule:**\n- 1 Week Before: Review all material\n- 3-4 Days Before: 20-30 min daily, focus on hard topics\n- 1 Day Before: Quick review, sleep 8-10 hours!\n- Test Day: Eat breakfast, brief review, stay calm\n\n**Techniques:**\n1. **Flashcards:** Question front, answer back\n2. **Teaching:** Explain to parent/pet/stuffed animal\n3. **Practice Problems:** Do examples, time yourself\n4. **Color Coding:** Highlighters for ideas/details/vocabulary\n5. **Memory Tricks:** Acronyms (HOMES=Great Lakes), rhymes, stories\n6. **Study Games:** Quiz friends, songs, online games\n\n**Tips:** Quiet spot, take breaks every 20-30 min, snacks/water, no cramming!', 'domain': 'kids_education'},
        
        # Middle School (12-14)
        {'prompt': 'Can you explain how to solve linear equations?', 'response': '**Solving Linear Equations:**\n\n**Goal:** Isolate the variable (get x by itself)\n\n**Golden Rule:** Whatever you do to one side, do to the other!\n\n**Example: 2x + 5 = 13**\n\n**Step 1:** Subtract 5 from both sides\n2x + 5 - 5 = 13 - 5\n2x = 8\n\n**Step 2:** Divide both sides by 2\n2x/2 = 8/2\nx = 4\n\n**Check:** 2(4) + 5 = 8 + 5 = 13 ✓\n\n**Order of operations (reverse):**\n1. Undo addition/subtraction\n2. Undo multiplication/division\n3. Undo exponents/roots\n\n**Practice makes perfect!**', 'domain': 'kids_education'},
        
        {'prompt': 'How do I write a good essay?', 'response': '**Essay writing guide:**\n\n**Structure:**\n\n**1. Introduction**\n- Hook (interesting opening)\n- Background info\n- Thesis statement (main argument)\n\n**2. Body Paragraphs** (3-5)\n- Topic sentence\n- Evidence/examples\n- Explanation\n- Connection to thesis\n\n**3. Conclusion**\n- Restate thesis (different words)\n- Summarize main points\n- Final thought/call to action\n\n**Writing Process:**\n1. Brainstorm ideas\n2. Create outline\n3. Write rough draft\n4. Revise (check flow, arguments)\n5. Edit (grammar, spelling)\n6. Proofread (read aloud!)\n\n**Tips:** Strong topic sentences, varied sentences, transition words, specific examples', 'domain': 'kids_education'},
        
        # High School (15-18)
        {'prompt': 'How do I prepare for the SAT?', 'response': '**SAT Preparation:**\n\n**Timeline (3-6 months):**\n\n**Phase 1: Baseline**\n- Take practice test\n- Identify weak areas\n- Set target score\n\n**Phase 2: Content Review**\n- Study math concepts\n- Grammar rules\n- Reading strategies\n- Essay writing (if applicable)\n\n**Phase 3: Practice**\n- Weekly practice tests\n- Review mistakes thoroughly\n- Time management drills\n- Use official College Board materials\n\n**Test Day:**\n- Sleep 8 hours\n- Healthy breakfast\n- Arrive early\n- Bring: ID, calculator, #2 pencils, snacks\n\n**Resources:**\n- Khan Academy (free)\n- Official SAT practice tests\n- SAT prep books\n- Consider tutor if needed', 'domain': 'kids_education'},
        
        {'prompt': 'How do I choose a college major?', 'response': '**Choosing a college major:**\n\n**Self-Assessment:**\n1. **Interests:** What do you enjoy learning about?\n2. **Strengths:** What are you naturally good at?\n3. **Values:** What\'s important to you? (helping others, creativity, money, etc.)\n4. **Career Goals:** What jobs interest you?\n\n**Research:**\n- Explore major descriptions\n- Talk to students/professors in field\n- Job outlook and salary data\n- Required courses\n- Internship opportunities\n\n**Try it out:**\n- Take intro courses in different fields\n- Job shadow professionals\n- Volunteer/intern in areas of interest\n- Join related clubs\n\n**Remember:**\n- Many change majors (30-50% of students)\n- Can pursue careers outside your major\n- Liberal arts gives flexibility\n- It\'s okay to be undecided!', 'domain': 'kids_education'}
    ]

def extract_earth_science_complete() -> List[Dict]:
    """Complete earth science dataset"""
    return [
        {'prompt': 'What are the layers of the Earth?', 'response': 'Earth has four main layers:\n\n**1. Crust** (outermost)\n- Thickness: 5-70 km\n- Oceanic (thinner, denser) and continental (thicker, lighter)\n- What we live on\n\n**2. Mantle**\n- Thickness: ~2,900 km\n- Semi-solid rock, flows slowly\n- Convection drives plate tectonics\n- Temperature: 500-4,000°C\n\n**3. Outer Core**\n- Thickness: ~2,200 km\n- Liquid iron and nickel\n- Creates Earth\'s magnetic field\n- Temperature: 4,000-6,000°C\n\n**4. Inner Core** (center)\n- Radius: ~1,220 km\n- Solid iron/nickel\n- Temperature: 5,000-7,000°C (hot as sun\'s surface!)\n- Solid due to extreme pressure', 'domain': 'earth_science'},
        
        {'prompt': 'How do earthquakes happen?', 'response': 'Earthquakes occur when stress in Earth\'s crust is released:\n\n**Main Cause: Tectonic Plates**\n1. Plates move (collide, separate, slide past)\n2. Stress builds along faults\n3. Rock suddenly breaks\n4. Energy released as seismic waves\n5. Waves travel through Earth, cause shaking\n\n**Other Causes:**\n- Volcanic activity (magma movement)\n- Human activity (mining, fracking)\n\n**Measurement:**\n- **Magnitude:** Richter or Moment Magnitude (energy released)\n- **Intensity:** Modified Mercalli (damage/effects)\n\n**Safety:** Drop, Cover, Hold On during earthquake', 'domain': 'earth_science'},
        
        {'prompt': 'How does the water cycle work?', 'response': 'The water cycle is continuous movement of water:\n\n**Steps:**\n\n**1. Evaporation**\n- Sun heats water in oceans/lakes/rivers\n- Liquid → water vapor (gas)\n- Rises into atmosphere\n\n**2. Transpiration**\n- Plants release water vapor through leaves\n- Combines with evaporation\n\n**3. Condensation**\n- Water vapor cools in atmosphere\n- Forms tiny droplets\n- Creates clouds and fog\n\n**4. Precipitation**\n- Droplets combine, get heavy\n- Fall as rain, snow, sleet, hail\n\n**5. Collection**\n- Water collects in oceans, lakes, rivers, groundwater\n- Cycle begins again\n\n**Importance:** Provides fresh water, regulates climate, distributes heat', 'domain': 'earth_science'},
        
        {'prompt': 'What causes seasons?', 'response': 'Seasons are caused by Earth\'s tilted axis:\n\n**Key Fact:** Earth\'s axis tilts 23.5° relative to its orbit\n\n**How it works:**\n\n**Summer (for hemisphere):**\n- Tilted toward sun\n- Direct sunlight\n- Longer days\n- Warmer temperatures\n\n**Winter (for hemisphere):**\n- Tilted away from sun\n- Indirect sunlight\n- Shorter days\n- Colder temperatures\n\n**Spring/Fall:**\n- Neither tilted toward nor away\n- Moderate temperatures\n- Equal day/night\n\n**Note:** When Northern Hemisphere has summer, Southern has winter (opposite tilt)\n\n**NOT caused by:** Distance from sun (Earth\'s orbit is nearly circular)', 'domain': 'earth_science'},
        
        {'prompt': 'What is the rock cycle?', 'response': 'The rock cycle shows how rocks transform:\n\n**Three Rock Types:**\n\n**1. Igneous**\n- Form from cooled magma/lava\n- Examples: granite, basalt\n\n**2. Sedimentary**\n- Form from compressed sediments\n- Examples: sandstone, limestone\n\n**3. Metamorphic**\n- Form from heat/pressure changing existing rocks\n- Examples: marble (from limestone), slate (from shale)\n\n**Transformations:**\n- Igneous → (weathering) → Sedimentary\n- Sedimentary → (heat/pressure) → Metamorphic\n- Metamorphic → (melting) → Igneous\n- Any rock → (extreme heat) → Igneous\n\n**Processes:** Weathering, erosion, deposition, compaction, heat, pressure, melting\n\n**Timeline:** Can take millions of years!', 'domain': 'earth_science'}
    ]

def extract_plants_complete() -> List[Dict]:
    """Complete plants/botany dataset"""
    return [
        {'prompt': 'What is photosynthesis?', 'response': 'Photosynthesis converts light energy into chemical energy (glucose).\n\n**Equation:** 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂\n\n**Process:**\n1. Chlorophyll absorbs sunlight\n2. Light energy splits water molecules\n3. CO₂ combines with hydrogen\n4. Produces glucose + releases oxygen\n\n**Importance:**\n- Produces oxygen we breathe\n- Creates food for plants\n- Base of food chains\n- Removes CO₂ from atmosphere', 'domain': 'plants_botany'},
        
        {'prompt': 'What are the main parts of a plant?', 'response': 'Plants have key parts with specific functions:\n\n**1. Roots**\n- Anchor in soil\n- Absorb water/nutrients\n- Store food (some plants)\n\n**2. Stem**\n- Supports leaves/flowers\n- Transports water/nutrients\n- Stores food (some plants)\n\n**3. Leaves**\n- Perform photosynthesis\n- Gas exchange (O₂/CO₂)\n- Transpiration\n\n**4. Flowers** (flowering plants)\n- Reproductive structures\n- Produce seeds\n- Attract pollinators\n\n**5. Seeds/Fruit**\n- Contain embryo\n- Enable reproduction\n- Protect/disperse offspring', 'domain': 'plants_botany'},
        
        {'prompt': 'How do I care for a snake plant?', 'response': 'Snake Plant (Sansevieria) - easiest houseplant!\n\n**Light:** Low to bright indirect (very tolerant)\n\n**Water:**\n- Every 2-3 weeks\n- Let soil dry completely\n- Less in winter\n- Overwatering = main killer!\n\n**Soil:** Well-draining cactus/succulent mix\n\n**Temperature:** 60-85°F (15-29°C)\n\n**Benefits:**\n- Purifies air (removes toxins)\n- Produces oxygen at night\n- Nearly indestructible\n- Perfect for beginners', 'domain': 'plants_botany'},
        
        {'prompt': 'How do I grow tomatoes?', 'response': 'Growing tomatoes successfully:\n\n**Starting:**\n- Seeds indoors 6-8 weeks before last frost\n- Or buy seedlings\n- Choose: determinate (bush) or indeterminate (vine)\n\n**Planting:**\n- Full sun (6-8 hours)\n- Rich, well-draining soil (pH 6.0-6.8)\n- Space 24-36" apart\n- Plant deep (bury stem to first leaves)\n\n**Care:**\n- Water deeply (1-2" per week)\n- Mulch around plants\n- Fertilize every 2-3 weeks\n- Stake or cage for support\n- Prune suckers (side shoots)\n\n**Harvest:** 60-85 days, pick when fully colored\n\n**Issues:**\n- Blossom end rot: Add calcium, water consistently\n- Hornworms: Hand pick', 'domain': 'plants_botany'},
        
        {'prompt': 'What is the difference between annuals and perennials?', 'response': '**Annual Plants:**\n- Complete life cycle in one year\n- Germinate, grow, flower, seed, die\n- Replant each year\n- Examples: marigolds, zinnias, tomatoes, basil\n- Longer flowering\n- Good for: seasonal color, vegetables\n\n**Perennial Plants:**\n- Live 3+ years\n- Die back in winter, regrow in spring\n- Roots survive winter\n- Examples: hostas, daylilies, lavender, strawberries\n- Lower maintenance after establishment\n- Good for: permanent landscape\n\n**Biennials:**\n- Two-year cycle\n- Year 1: growth, Year 2: flower/seed/die\n- Examples: carrots, parsley, foxglove', 'domain': 'plants_botany'}
    ]

def save_all_comprehensive():
    """Save everything - GoEmotions + all templates"""
    print("\n" + "="*80)
    print("🌟 COMPLETE FREE DATASET INTEGRATION")
    print("="*80)
    print("\nDownloading public datasets + extracting all template examples...\n")
    
    # Download GoEmotions
    goemotions = download_goemotions()
    
    # Get all template examples
    template_datasets = {
        'kids_education': extract_childrens_education_complete(),
        'earth_science': extract_earth_science_complete(),
        'plants_botany': extract_plants_complete()
    }
    
    # Save GoEmotions
    if goemotions:
        domain_dir = 'datasets/emotion_detection'
        os.makedirs(domain_dir, exist_ok=True)
        filepath = f'{domain_dir}/knowledge.json'
        
        # Sample only first 1000 for now (full dataset is huge)
        sampled = goemotions[:1000] if len(goemotions) > 1000 else goemotions
        
        with open(filepath, 'w') as f:
            json.dump(sampled, f, indent=2)
        
        print(f"\n✅ emotion_detection (GoEmotions): 1,000 examples sampled from {len(goemotions):,} total")
        print(f"   (Full dataset available - using sample for efficiency)")
    
    # Save template examples
    total_new = 0
    for domain, examples in template_datasets.items():
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
    print(f"🎉 COMPLETE! Added 1,000 GoEmotions + {total_new} template examples")
    print(f"💰 Cost: $0.00 (100% FREE)")
    print(f"{'='*80}")

if __name__ == "__main__":
    save_all_comprehensive()
