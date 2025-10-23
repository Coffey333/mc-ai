#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE TEMPLATE EXTRACTION
Extract ALL remaining examples from user's provided templates:
- Chemistry (periodic table, elements, reactions)
- Biology (cells, DNA, evolution, ecosystems)
- Space/Astronomy (planets, stars, universe)
- Physics (expanded coverage)
"""

import json
import os
from typing import List, Dict

def extract_chemistry_complete() -> List[Dict]:
    """Complete chemistry dataset from templates"""
    return [
        # Periodic Table & Elements
        {'prompt': 'What is the periodic table?', 'response': 'The periodic table organizes all known chemical elements by atomic number and properties.\n\n**Organization:**\n- Rows (Periods): Same number of electron shells\n- Columns (Groups): Similar chemical properties\n- Left to right: Atomic number increases\n\n**Groups:**\n- Group 1: Alkali metals (reactive)\n- Group 2: Alkaline earth metals\n- Groups 3-12: Transition metals\n- Group 17: Halogens (very reactive)\n- Group 18: Noble gases (inert)\n\n**Creator:** Dmitri Mendeleev (1869)\n\n**Total Elements:** 118 (as of 2024)', 'domain': 'chemistry'},
        
        {'prompt': 'What is an atom?', 'response': 'An atom is the smallest unit of matter that retains chemical properties.\n\n**Structure:**\n\n**Nucleus (center):**\n- Protons (+charge)\n- Neutrons (no charge)\n\n**Electron Cloud (surrounding):**\n- Electrons (-charge)\n- Orbits in shells/orbitals\n\n**Properties:**\n- Atomic number = # protons\n- Mass number = protons + neutrons\n- Neutral atom: # protons = # electrons\n- Most of atom is empty space!\n\n**Size:** ~0.1 nanometers diameter', 'domain': 'chemistry'},
        
        {'prompt': 'What is water made of?', 'response': 'Water is made of hydrogen and oxygen atoms.\n\n**Chemical Formula:** H₂O\n- 2 Hydrogen atoms\n- 1 Oxygen atom\n\n**Properties:**\n- Polar molecule (slightly charged ends)\n- Forms hydrogen bonds\n- Universal solvent\n- Expands when frozen\n- High specific heat\n\n**Importance:**\n- Essential for all life\n- 71% of Earth\'s surface\n- 60% of human body\n- Regulates temperature', 'domain': 'chemistry'},
        
        {'prompt': 'What are the states of matter?', 'response': 'Matter exists in different states based on energy/temperature:\n\n**1. Solid**\n- Fixed shape and volume\n- Particles tightly packed, vibrate in place\n- Example: ice, wood, metal\n\n**2. Liquid**\n- Fixed volume, no fixed shape\n- Particles close but move freely\n- Takes shape of container\n- Example: water, oil, juice\n\n**3. Gas**\n- No fixed shape or volume\n- Particles far apart, move rapidly\n- Fills entire container\n- Example: air, steam, helium\n\n**4. Plasma** (less common)\n- Ionized gas, very high energy\n- Example: lightning, sun, neon signs\n\n**5. Bose-Einstein Condensate** (very rare)\n- Near absolute zero temperature\n- Atoms behave as single quantum entity', 'domain': 'chemistry'},
        
        {'prompt': 'What is a chemical reaction?', 'response': 'A chemical reaction occurs when substances interact to form new substances.\n\n**Signs of Reaction:**\n- Color change\n- Temperature change (hot/cold)\n- Gas production (bubbles)\n- Precipitate formation (solid)\n- Light emission\n\n**Types:**\n1. **Synthesis:** A + B → AB (combining)\n2. **Decomposition:** AB → A + B (breaking apart)\n3. **Single Replacement:** A + BC → AC + B\n4. **Double Replacement:** AB + CD → AD + CB\n5. **Combustion:** Fuel + O₂ → CO₂ + H₂O + energy\n\n**Law of Conservation:** Matter cannot be created or destroyed, only rearranged\n\n**Balanced Equation:** Same number of each atom on both sides', 'domain': 'chemistry'},
        
        {'prompt': 'What is pH?', 'response': 'pH measures how acidic or basic (alkaline) a solution is.\n\n**Scale:** 0-14\n- 0-6: Acidic (more H⁺ ions)\n- 7: Neutral (pure water)\n- 8-14: Basic/Alkaline (more OH⁻ ions)\n\n**Examples:**\n- Battery acid: pH 0\n- Lemon juice: pH 2\n- Coffee: pH 5\n- Pure water: pH 7\n- Baking soda: pH 9\n- Bleach: pH 12\n- Drain cleaner: pH 14\n\n**Importance:**\n- Blood pH: 7.35-7.45 (tightly regulated)\n- Soil pH affects plant growth\n- Stomach pH: ~2 (digest food)', 'domain': 'chemistry'},
        
        {'prompt': 'What are acids and bases?', 'response': '**Acids:**\n- Donate H⁺ ions (protons)\n- Taste sour\n- Turn litmus paper red\n- pH < 7\n- Examples: HCl (hydrochloric), H₂SO₄ (sulfuric), citric acid\n\n**Bases:**\n- Accept H⁺ ions / donate OH⁻ ions\n- Taste bitter, feel slippery\n- Turn litmus paper blue\n- pH > 7\n- Examples: NaOH (sodium hydroxide), NH₃ (ammonia)\n\n**Neutralization:**\nAcid + Base → Salt + Water\nExample: HCl + NaOH → NaCl + H₂O\n\n**Strength:** Strong (fully dissociate) vs weak (partially dissociate)', 'domain': 'chemistry'},
        
        {'prompt': 'What is an element?', 'response': 'An element is a pure substance made of only one type of atom.\n\n**Cannot be broken down** into simpler substances by chemical means\n\n**Examples:**\n- Hydrogen (H) - lightest element\n- Carbon (C) - basis of life\n- Oxygen (O) - we breathe it\n- Gold (Au) - precious metal\n- Iron (Fe) - common metal\n\n**Elements vs Compounds:**\n- Element: One type of atom (H, O, C)\n- Compound: Multiple elements bonded (H₂O, CO₂, NaCl)\n\n**Total:** 118 known elements (92 naturally occurring, rest synthetic)', 'domain': 'chemistry'},
        
        {'prompt': 'What is oxygen?', 'response': 'Oxygen is a chemical element essential for life.\n\n**Symbol:** O\n**Atomic Number:** 8\n**Atomic Mass:** 16\n\n**Properties:**\n- Colorless, odorless gas (at room temp)\n- Makes up 21% of atmosphere\n- Highly reactive (supports combustion)\n- Forms O₂ molecules (diatomic)\n\n**Uses:**\n- Cellular respiration (energy production)\n- Combustion (burning)\n- Medical oxygen therapy\n- Welding and cutting\n- Water treatment\n\n**Production:**\n- Plants via photosynthesis\n- Ocean phytoplankton (70%)\n\n**Fun Fact:** 65% of human body is oxygen!', 'domain': 'chemistry'},
        
        {'prompt': 'What is carbon?', 'response': 'Carbon is the foundation of all organic life.\n\n**Symbol:** C\n**Atomic Number:** 6\n**Atomic Mass:** 12\n\n**Unique Property:** Forms 4 bonds → millions of compounds\n\n**Forms:**\n- Diamond (hardest natural material)\n- Graphite (soft, conducts electricity)\n- Graphene (single layer, super strong)\n- Carbon nanotubes\n- Coal\n\n**Importance:**\n- Basis of organic chemistry\n- In all living things (proteins, DNA, carbs, fats)\n- Carbon cycle regulates Earth\'s climate\n- 18% of human body\n\n**Compounds:** Organic (with H, O, N) and inorganic (CO₂, carbonates)', 'domain': 'chemistry'}
    ]

def extract_biology_complete() -> List[Dict]:
    """Complete biology dataset from templates"""
    return [
        # Cells & Biology Basics
        {'prompt': 'What is a cell?', 'response': 'A cell is the basic unit of life.\n\n**Two Main Types:**\n\n**1. Prokaryotic** (bacteria, archaea)\n- No nucleus\n- No membrane-bound organelles\n- DNA in nucleoid region\n- Smaller, simpler\n\n**2. Eukaryotic** (animals, plants, fungi, protists)\n- Has nucleus\n- Membrane-bound organelles\n- DNA in chromosomes\n- Larger, more complex\n\n**All Cells Have:**\n- Cell membrane (boundary)\n- Cytoplasm (jelly-like substance)\n- DNA (genetic material)\n- Ribosomes (make proteins)\n\n**Cell Theory:**\n1. All living things made of cells\n2. Cells are basic unit of life\n3. All cells come from pre-existing cells', 'domain': 'biology'},
        
        {'prompt': 'What is DNA?', 'response': 'DNA (Deoxyribonucleic Acid) is the molecule that stores genetic information.\n\n**Structure:**\n- Double helix (twisted ladder)\n- Two strands of nucleotides\n- Held together by base pairs\n\n**Bases (4):**\n- Adenine (A) pairs with Thymine (T)\n- Guanine (G) pairs with Cytosine (C)\n\n**Function:**\n- Stores instructions for making proteins\n- Passes traits from parents to offspring\n- Controls cell function\n\n**Location:**\n- Nucleus (eukaryotes)\n- Nucleoid (prokaryotes)\n- Mitochondria (small amount)\n\n**Discovery:** Watson & Crick (1953)\n\n**Fun Fact:** If uncoiled, DNA from one cell would be ~6 feet long!', 'domain': 'biology'},
        
        {'prompt': 'What is photosynthesis?', 'response': 'Photosynthesis converts light energy into chemical energy (glucose).\n\n**Equation:** 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂\n\n**Where:** Chloroplasts (in plant cells)\n\n**Process:**\n\n**1. Light Reactions (in thylakoids)**\n- Chlorophyll absorbs sunlight\n- Water splits → releases O₂\n- Produces ATP + NADPH\n\n**2. Dark Reactions / Calvin Cycle (in stroma)**\n- Uses ATP + NADPH\n- CO₂ converts to glucose\n\n**Importance:**\n- Produces oxygen we breathe\n- Creates food for plants (base of food chain)\n- Removes CO₂ from atmosphere', 'domain': 'biology'},
        
        {'prompt': 'What is evolution?', 'response': 'Evolution is the change in species over time through natural selection.\n\n**Key Mechanisms:**\n\n**1. Natural Selection**\n- Variation exists in populations\n- Some traits help survival/reproduction\n- Those individuals reproduce more\n- Beneficial traits become more common\n\n**2. Mutation**\n- Random DNA changes\n- Creates new variations\n\n**3. Genetic Drift**\n- Random changes in small populations\n\n**4. Gene Flow**\n- Migration between populations\n\n**Evidence:**\n- Fossils (show gradual changes)\n- DNA similarities (common ancestry)\n- Anatomical structures (homologous)\n- Biogeography (species distribution)\n- Observable evolution (bacteria, moths)\n\n**"Survival of the fittest"** = best adapted to environment', 'domain': 'biology'},
        
        {'prompt': 'What is an ecosystem?', 'response': 'An ecosystem is a community of living things interacting with their environment.\n\n**Components:**\n\n**Biotic (Living):**\n- Producers (plants, algae)\n- Consumers (herbivores, carnivores, omnivores)\n- Decomposers (bacteria, fungi)\n\n**Abiotic (Non-living):**\n- Water, air, sunlight\n- Temperature, soil\n- Rocks, minerals\n\n**Energy Flow:**\nSun → Producers → Primary consumers → Secondary consumers → Decomposers\n\n**Matter Cycles:**\n- Water cycle\n- Carbon cycle\n- Nitrogen cycle\n\n**Examples:**\n- Forest, ocean, desert, pond, coral reef\n\n**Balance:** Changes to one part affect the whole system', 'domain': 'biology'},
        
        {'prompt': 'What are the main organelles in a cell?', 'response': 'Cell organelles are specialized structures with specific functions:\n\n**1. Nucleus** - Control center, contains DNA\n\n**2. Mitochondria** - Powerhouse, produces ATP (energy)\n\n**3. Ribosomes** - Make proteins\n\n**4. Endoplasmic Reticulum (ER)**\n- Rough ER: Has ribosomes, makes proteins\n- Smooth ER: No ribosomes, makes lipids\n\n**5. Golgi Apparatus** - Modifies & packages proteins\n\n**6. Lysosomes** - Digestive system, breaks down waste\n\n**7. Cell Membrane** - Boundary, controls what enters/exits\n\n**Plant Cells Only:**\n- Cell Wall (rigid support)\n- Chloroplasts (photosynthesis)\n- Large Vacuole (storage)\n\n**Analogy:** Like organs in body, each has a job', 'domain': 'biology'},
        
        {'prompt': 'What is the difference between mitosis and meiosis?', 'response': '**Mitosis** (Body Cell Division):\n- Purpose: Growth, repair, asexual reproduction\n- 1 cell → 2 identical cells\n- Same # chromosomes as parent (diploid → diploid)\n- Happens in somatic (body) cells\n- Example: Skin cell divides to heal wound\n\n**Meiosis** (Sex Cell Division):\n- Purpose: Sexual reproduction\n- 1 cell → 4 unique cells\n- Half # chromosomes (diploid → haploid)\n- Happens in reproductive organs\n- Creates: Sperm, eggs, pollen, ovules\n- Increases genetic diversity (crossing over, independent assortment)\n\n**Key Difference:**\n- Mitosis: Clones (identical)\n- Meiosis: Variety (different)\n\n**Both:** Copy DNA first, then divide', 'domain': 'biology'},
        
        {'prompt': 'What is genetics?', 'response': 'Genetics is the study of heredity and variation in living organisms.\n\n**Key Concepts:**\n\n**Gene:** Unit of heredity, segment of DNA\n\n**Allele:** Different versions of a gene\n- Dominant: Expressed if present (uppercase: A)\n- Recessive: Only expressed if two copies (lowercase: a)\n\n**Genotype:** Genetic makeup (AA, Aa, aa)\n**Phenotype:** Physical appearance (brown eyes)\n\n**Inheritance:**\n- Mendel\'s Laws (pea plants)\n- Punnett Squares predict offspring\n\n**Examples:**\n- Eye color, height, blood type\n- Genetic disorders (sickle cell, cystic fibrosis)\n\n**Modern Genetics:**\n- DNA sequencing\n- Gene therapy\n- CRISPR gene editing', 'domain': 'biology'},
        
        {'prompt': 'What is the human body made of?', 'response': 'The human body is made of trillions of cells organized into systems.\n\n**Major Systems:**\n\n1. **Skeletal:** 206 bones, support & protection\n2. **Muscular:** 600+ muscles, movement\n3. **Circulatory:** Heart, blood vessels, transport\n4. **Respiratory:** Lungs, gas exchange\n5. **Digestive:** Break down food, absorb nutrients\n6. **Nervous:** Brain, spinal cord, control center\n7. **Endocrine:** Hormones, regulation\n8. **Immune:** Defense against disease\n9. **Excretory:** Kidneys, remove waste\n10. **Reproductive:** Create offspring\n\n**Organization:** Cells → Tissues → Organs → Organ Systems → Organism\n\n**Composition:**\n- 60% water\n- 16% protein\n- 16% fat\n- 6% minerals\n- 1% carbohydrates\n- <1% nucleic acids', 'domain': 'biology'},
        
        {'prompt': 'What is cellular respiration?', 'response': 'Cellular respiration converts glucose into usable energy (ATP).\n\n**Equation:** C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP\n\n**Stages:**\n\n**1. Glycolysis** (cytoplasm)\n- Glucose → 2 Pyruvate\n- Produces 2 ATP (small amount)\n\n**2. Krebs Cycle** (mitochondrial matrix)\n- Pyruvate broken down\n- Releases CO₂\n- Produces electron carriers\n\n**3. Electron Transport Chain** (inner mitochondrial membrane)\n- Uses O₂\n- Produces ~34 ATP (most energy!)\n- Releases H₂O\n\n**Total:** ~36-38 ATP per glucose\n\n**Location:** Mitochondria (powerhouse of cell)\n\n**Note:** Opposite of photosynthesis!', 'domain': 'biology'}
    ]

def extract_space_complete() -> List[Dict]:
    """Complete space/astronomy dataset from templates"""
    return [
        # Solar System & Planets
        {'prompt': 'What are the planets in our solar system?', 'response': 'Our solar system has 8 planets (in order from Sun):\n\n**Inner/Rocky Planets:**\n1. **Mercury** - Smallest, closest to Sun, no atmosphere\n2. **Venus** - Hottest planet, thick CO₂ atmosphere\n3. **Earth** - Only planet with life (that we know!)\n4. **Mars** - Red planet, has ice caps\n\n**Outer/Gas Giants:**\n5. **Jupiter** - Largest, Great Red Spot storm\n6. **Saturn** - Famous rings, many moons\n7. **Uranus** - Tilted on side, blue-green color\n8. **Neptune** - Farthest, fastest winds\n\n**Mnemonic:** "My Very Educated Mother Just Served Us Nachos"\n\n**Note:** Pluto was reclassified as a "dwarf planet" in 2006', 'domain': 'space_astronomy'},
        
        {'prompt': 'What is the Sun?', 'response': 'The Sun is a star at the center of our solar system.\n\n**Type:** Yellow dwarf star (G-type main sequence)\n\n**Size:**\n- Diameter: 1.4 million km (~109 Earths)\n- Mass: 99.86% of solar system mass\n- Could fit 1.3 million Earths inside!\n\n**Composition:**\n- 73% Hydrogen\n- 25% Helium\n- 2% Other elements\n\n**Energy Production:**\n- Nuclear fusion (H → He)\n- Core temp: 15 million °C\n- Surface temp: 5,500 °C\n\n**Properties:**\n- Light reaches Earth in 8 minutes\n- Age: 4.6 billion years\n- Will shine for 5 billion more years\n\n**Importance:** Powers all life on Earth', 'domain': 'space_astronomy'},
        
        {'prompt': 'What is a galaxy?', 'response': 'A galaxy is a massive system of stars, gas, dust, and dark matter held together by gravity.\n\n**Types:**\n\n**1. Spiral** (like Milky Way)\n- Disk with spiral arms\n- Active star formation\n- Examples: Andromeda, Milky Way\n\n**2. Elliptical**\n- Oval/sphere shape\n- Older stars, little gas\n- Range from small to giant\n\n**3. Irregular**\n- No defined shape\n- Often result of collisions\n\n**Milky Way Facts:**\n- Our galaxy\n- ~200-400 billion stars\n- ~100,000 light-years across\n- Sun is 26,000 light-years from center\n\n**Observable Universe:** ~2 trillion galaxies!\n\n**Galactic Address:** Earth → Solar System → Orion Arm → Milky Way → Local Group → Virgo Supercluster', 'domain': 'space_astronomy'},
        
        {'prompt': 'What is a black hole?', 'response': 'A black hole is a region where gravity is so strong that nothing, not even light, can escape.\n\n**Formation:**\n- Massive star dies (>20 solar masses)\n- Core collapses\n- Gravity becomes infinite at singularity\n\n**Parts:**\n- **Singularity:** Center point, infinite density\n- **Event Horizon:** Point of no return\n- **Accretion Disk:** Swirling matter around it\n\n**Types:**\n1. **Stellar** - From star collapse (3-100 solar masses)\n2. **Supermassive** - Center of galaxies (millions-billions solar masses)\n3. **Intermediate** - Between stellar & supermassive\n4. **Primordial** - Theoretical, from Big Bang\n\n**Properties:**\n- Bends spacetime\n- Slows time near horizon\n- Can\'t see directly (observe effects on nearby matter)\n\n**Note:** Won\'t "suck up" everything - need to be very close', 'domain': 'space_astronomy'},
        
        {'prompt': 'What is the Moon?', 'response': 'The Moon is Earth\'s only natural satellite.\n\n**Size & Distance:**\n- Diameter: 3,474 km (~1/4 Earth\'s)\n- Distance: 384,400 km from Earth\n- Takes 27.3 days to orbit Earth\n\n**Phases:** New, Crescent, Quarter, Gibbous, Full (repeat)\n- Caused by changing sunlight angles\n- Same side always faces Earth (tidal locking)\n\n**Surface:**\n- Covered in craters (no atmosphere to burn meteors)\n- Maria (dark "seas" - ancient lava flows)\n- Temperature: -173°C to 127°C\n\n**Effects on Earth:**\n- Tides (gravity pulls ocean water)\n- Stabilizes Earth\'s tilt (seasons)\n- Slows Earth\'s rotation (slightly)\n\n**Formation:** Giant impact theory (Mars-sized object hit early Earth)\n\n**Humans landed:** 1969 (Apollo 11)', 'domain': 'space_astronomy'},
        
        {'prompt': 'What is the universe?', 'response': 'The universe is everything that exists - all matter, energy, space, and time.\n\n**Scale:**\n- Observable universe: 93 billion light-years across\n- Contains ~2 trillion galaxies\n- ~10²⁴ stars\n\n**Composition:**\n- 68% Dark Energy (mysterious force)\n- 27% Dark Matter (invisible matter)\n- 5% Normal Matter (stars, planets, us!)\n\n**Age:** 13.8 billion years\n\n**Origin:** Big Bang Theory\n1. Universe began as tiny, hot, dense point\n2. Rapidly expanded (inflation)\n3. Cooled, formed particles\n4. Hydrogen/helium formed\n5. First stars/galaxies formed\n6. Continues expanding today (accelerating!)\n\n**Shape:** Likely flat or slightly curved\n\n**Fate:** Uncertain - Big Freeze, Big Rip, or Big Crunch', 'domain': 'space_astronomy'},
        
        {'prompt': 'What are stars made of?', 'response': 'Stars are giant balls of hot gas (plasma) that produce energy through nuclear fusion.\n\n**Composition:**\n- ~73% Hydrogen\n- ~25% Helium\n- ~2% Other elements (C, O, N, Fe, etc.)\n\n**Energy Production:**\n1. Gravity compresses core\n2. Core gets extremely hot (millions °C)\n3. Hydrogen fuses into Helium\n4. Releases enormous energy\n5. Energy travels to surface → light!\n\n**Life Cycle:**\n1. Nebula (gas cloud)\n2. Protostar (collapse begins)\n3. Main Sequence (stable burning - Sun here)\n4. Red Giant/Supergiant (fuel running out)\n5. Death:\n   - Small stars: White Dwarf → Black Dwarf\n   - Massive stars: Supernova → Neutron Star or Black Hole\n\n**Colors indicate temperature:**\n- Blue/White: Hottest (>10,000 K)\n- Yellow: Medium (5,000-7,000 K)\n- Red: Coolest (<3,500 K)', 'domain': 'space_astronomy'},
        
        {'prompt': 'What is a comet?', 'response': 'A comet is a cosmic snowball of frozen gases, rock, and dust.\n\n**Composition:**\n- Ice (water, CO₂, methane, ammonia)\n- Dust and rocky material\n- Organic compounds\n\n**Structure:**\n- **Nucleus:** Solid center (few km wide)\n- **Coma:** Gas/dust cloud when near Sun\n- **Tails:** Two types (always point away from Sun)\n  - Ion tail (gas, straight, blue)\n  - Dust tail (curved, yellowish)\n\n**Orbit:**\n- Highly elliptical (oval)\n- Some take thousands of years\n- Halley\'s Comet: Returns every 76 years (last seen 1986)\n\n**Origin:**\n- Kuiper Belt (beyond Neptune)\n- Oort Cloud (very distant)\n\n**Famous:** Halley, Hale-Bopp, NEOWISE\n\n**"Dirty snowball"** - Fred Whipple (1950)', 'domain': 'space_astronomy'},
        
        {'prompt': 'What is a light-year?', 'response': 'A light-year is the distance light travels in one year.\n\n**Distance:** ~9.46 trillion kilometers (5.88 trillion miles)\n\n**Why use it?**\n- Space distances are HUGE\n- Regular units (km/miles) are too small\n- Easier to say "4 light-years" than "37.8 trillion km"\n\n**Examples:**\n- Sun to Earth: 8 light-minutes\n- Nearest star (Proxima Centauri): 4.2 light-years\n- Milky Way width: 100,000 light-years\n- Andromeda Galaxy: 2.5 million light-years\n- Observable universe: 93 billion light-years\n\n**Time Machine:**\nWhen you see distant objects, you see their PAST!\n- See Sun as it was 8 min ago\n- See Andromeda as it was 2.5 million years ago\n\n**Note:** Measures DISTANCE, not time (confusing name!)', 'domain': 'space_astronomy'},
        
        {'prompt': 'What causes day and night?', 'response': 'Day and night are caused by Earth\'s rotation on its axis.\n\n**How it works:**\n1. Earth spins counterclockwise (viewed from North Pole)\n2. One complete rotation = 24 hours\n3. Side facing Sun = Daytime (lit up)\n4. Side away from Sun = Nighttime (dark)\n\n**Sunrise/Sunset:**\n- East side enters sunlight first → sunrise\n- West side leaves sunlight last → sunset\n- "Sun rises in East, sets in West"\n\n**Variations:**\n- **Equator:** ~12 hours day, 12 hours night (consistent)\n- **Poles:** Extreme\n  - Summer: 24-hour daylight ("midnight sun")\n  - Winter: 24-hour darkness ("polar night")\n\n**NOT caused by:** Earth orbiting Sun (that causes seasons)\n\n**Speed:** Earth\'s surface at equator moves ~1,670 km/h!', 'domain': 'space_astronomy'}
    ]

def extract_physics_advanced() -> List[Dict]:
    """Advanced physics examples from templates"""
    return [
        {'prompt': 'What is Newton\'s First Law?', 'response': 'Newton\'s First Law of Motion (Law of Inertia):\n\n**"An object at rest stays at rest, and an object in motion stays in motion with the same speed and direction, unless acted upon by an unbalanced force."**\n\n**In Simple Terms:**\n- Things don\'t move unless pushed/pulled\n- Moving things don\'t stop unless something stops them\n\n**Inertia:** Resistance to change in motion\n- More mass = more inertia\n\n**Examples:**\n- Ball on ground stays there until kicked\n- Hockey puck slides until friction stops it\n- You jerk forward when car brakes suddenly (your body wants to keep moving!)\n\n**Key:** "Unbalanced force" means net force ≠ 0', 'domain': 'physics'},
        
        {'prompt': 'What is Newton\'s Second Law?', 'response': 'Newton\'s Second Law of Motion:\n\n**F = ma**\n- Force = mass × acceleration\n\n**Meaning:**\n- Force causes acceleration\n- More force = more acceleration\n- More mass = less acceleration (for same force)\n\n**Units:**\n- Force: Newtons (N)\n- Mass: kilograms (kg)\n- Acceleration: m/s²\n\n**Examples:**\n- Push shopping cart: Easy when empty (low mass), hard when full (high mass)\n- Same force on car vs bicycle: Bicycle accelerates more (less mass)\n- Stronger push = faster acceleration\n\n**Rearrange:**\n- a = F/m (acceleration = force/mass)\n- m = F/a (mass = force/acceleration)', 'domain': 'physics'},
        
        {'prompt': 'What is Newton\'s Third Law?', 'response': 'Newton\'s Third Law of Motion:\n\n**"For every action, there is an equal and opposite reaction."**\n\n**Key Points:**\n- Forces come in pairs\n- Equal strength\n- Opposite direction\n- Act on DIFFERENT objects\n\n**Examples:**\n- Jump up: You push down on ground, ground pushes up on you\n- Rocket: Gases push down, rocket pushes up\n- Swimming: Push water back, water pushes you forward\n- Bird flying: Wings push air down, air pushes bird up\n- Gun recoil: Bullet goes forward, gun goes back\n\n**Important:** Action and reaction act on different objects, so they don\'t cancel out', 'domain': 'physics'},
        
        {'prompt': 'What is energy?', 'response': 'Energy is the ability to do work or cause change.\n\n**Forms of Energy:**\n\n**1. Kinetic** - Energy of motion\n- Moving car, flowing water, flying baseball\n- KE = ½mv²\n\n**2. Potential** - Stored energy\n- Gravitational (height): Ball on shelf\n- Elastic: Stretched rubber band\n- Chemical: Food, batteries, gasoline\n- Nuclear: Atom\'s nucleus\n\n**3. Thermal** - Heat energy (moving molecules)\n\n**4. Light** - Electromagnetic radiation\n\n**5. Sound** - Vibration energy\n\n**6. Electrical** - Moving electrons\n\n**Law of Conservation:**\nEnergy cannot be created or destroyed, only transformed\n\n**Energy Transfers:**\n- Chemical → Thermal + Light (burning)\n- Gravitational Potential → Kinetic (falling)\n- Electrical → Light + Thermal (light bulb)', 'domain': 'physics'},
        
        {'prompt': 'What is gravity?', 'response': 'Gravity is a force that attracts objects with mass toward each other.\n\n**Newton\'s Law of Gravitation:**\n- Every mass attracts every other mass\n- Larger masses = stronger pull\n- Closer distance = stronger pull\n\n**On Earth:**\n- Gravity pulls everything toward center\n- Acceleration: 9.8 m/s² (at surface)\n- Gives objects weight: W = mg\n\n**Examples:**\n- Keeps us on ground\n- Makes things fall\n- Holds Moon in orbit\n- Keeps planets around Sun\n\n**Einstein\'s View:**\nGravity is curvature of spacetime caused by mass\n- Massive objects bend space\n- Objects follow curved paths\n\n**Weightlessness in space:** Not "no gravity", but continuous free-fall!', 'domain': 'physics'}
    ]

def save_final_comprehensive():
    """Save all final comprehensive datasets"""
    print("\n" + "="*80)
    print("🎯 FINAL COMPREHENSIVE TEMPLATE EXTRACTION")
    print("="*80)
    print("\nExtracting ALL remaining examples from your templates...\n")
    
    datasets = {
        'chemistry': extract_chemistry_complete(),
        'biology': extract_biology_complete(),
        'space_astronomy': extract_space_complete(),
        'physics': extract_physics_advanced()
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
    print(f"🎉 FINAL EXTRACTION COMPLETE!")
    print(f"💰 Total added: {total_new} examples at $0.00 cost")
    print(f"✨ All template examples integrated!")
    print(f"{'='*80}")
    
    return total_new

if __name__ == "__main__":
    save_final_comprehensive()
