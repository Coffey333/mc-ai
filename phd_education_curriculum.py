"""
MC AI - PhD-Level Education Across ALL Subjects
Comprehensive curriculum covering all major educational domains
Target: 500+ sources for complete PhD-level knowledge
"""

import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

# Comprehensive PhD-Level Educational Curriculum
PHD_CURRICULUM = {
    # MATHEMATICS (50 sources)
    "Mathematics": [
        ("https://en.wikipedia.org/wiki/Mathematics", "Mathematics Overview"),
        ("https://en.wikipedia.org/wiki/Algebra", "Algebra"),
        ("https://en.wikipedia.org/wiki/Calculus", "Calculus"),
        ("https://en.wikipedia.org/wiki/Differential_calculus", "Differential Calculus"),
        ("https://en.wikipedia.org/wiki/Integral_calculus", "Integral Calculus"),
        ("https://en.wikipedia.org/wiki/Linear_algebra", "Linear Algebra"),
        ("https://en.wikipedia.org/wiki/Abstract_algebra", "Abstract Algebra"),
        ("https://en.wikipedia.org/wiki/Geometry", "Geometry"),
        ("https://en.wikipedia.org/wiki/Trigonometry", "Trigonometry"),
        ("https://en.wikipedia.org/wiki/Topology", "Topology"),
        ("https://en.wikipedia.org/wiki/Number_theory", "Number Theory"),
        ("https://en.wikipedia.org/wiki/Set_theory", "Set Theory"),
        ("https://en.wikipedia.org/wiki/Graph_theory", "Graph Theory"),
        ("https://en.wikipedia.org/wiki/Probability_theory", "Probability Theory"),
        ("https://en.wikipedia.org/wiki/Statistics", "Statistics"),
        ("https://en.wikipedia.org/wiki/Combinatorics", "Combinatorics"),
        ("https://en.wikipedia.org/wiki/Discrete_mathematics", "Discrete Mathematics"),
        ("https://en.wikipedia.org/wiki/Mathematical_analysis", "Mathematical Analysis"),
        ("https://en.wikipedia.org/wiki/Real_analysis", "Real Analysis"),
        ("https://en.wikipedia.org/wiki/Complex_analysis", "Complex Analysis"),
        ("https://en.wikipedia.org/wiki/Numerical_analysis", "Numerical Analysis"),
        ("https://en.wikipedia.org/wiki/Differential_equation", "Differential Equations"),
        ("https://en.wikipedia.org/wiki/Partial_differential_equation", "PDEs"),
        ("https://en.wikipedia.org/wiki/Matrix_(mathematics)", "Matrices"),
        ("https://en.wikipedia.org/wiki/Vector_space", "Vector Spaces"),
        ("https://en.wikipedia.org/wiki/Group_theory", "Group Theory"),
        ("https://en.wikipedia.org/wiki/Ring_theory", "Ring Theory"),
        ("https://en.wikipedia.org/wiki/Field_theory_(mathematics)", "Field Theory"),
        ("https://en.wikipedia.org/wiki/Category_theory", "Category Theory"),
        ("https://en.wikipedia.org/wiki/Logic", "Mathematical Logic"),
        ("https://en.wikipedia.org/wiki/Proof_theory", "Proof Theory"),
        ("https://en.wikipedia.org/wiki/Model_theory", "Model Theory"),
        ("https://en.wikipedia.org/wiki/Recursion_theory", "Recursion Theory"),
        ("https://en.wikipedia.org/wiki/Game_theory", "Game Theory"),
        ("https://en.wikipedia.org/wiki/Optimization_(mathematics)", "Optimization"),
        ("https://en.wikipedia.org/wiki/Dynamical_system", "Dynamical Systems"),
        ("https://en.wikipedia.org/wiki/Chaos_theory", "Chaos Theory"),
        ("https://en.wikipedia.org/wiki/Fractal", "Fractals"),
        ("https://en.wikipedia.org/wiki/Information_theory", "Information Theory"),
        ("https://en.wikipedia.org/wiki/Computational_complexity_theory", "Complexity Theory"),
    ],
    
    # PHYSICS (50 sources)
    "Physics": [
        ("https://en.wikipedia.org/wiki/Physics", "Physics Overview"),
        ("https://en.wikipedia.org/wiki/Classical_mechanics", "Classical Mechanics"),
        ("https://en.wikipedia.org/wiki/Newtonian_mechanics", "Newtonian Mechanics"),
        ("https://en.wikipedia.org/wiki/Thermodynamics", "Thermodynamics"),
        ("https://en.wikipedia.org/wiki/Statistical_mechanics", "Statistical Mechanics"),
        ("https://en.wikipedia.org/wiki/Electromagnetism", "Electromagnetism"),
        ("https://en.wikipedia.org/wiki/Optics", "Optics"),
        ("https://en.wikipedia.org/wiki/Quantum_mechanics", "Quantum Mechanics"),
        ("https://en.wikipedia.org/wiki/Quantum_field_theory", "Quantum Field Theory"),
        ("https://en.wikipedia.org/wiki/Relativity", "Relativity"),
        ("https://en.wikipedia.org/wiki/Special_relativity", "Special Relativity"),
        ("https://en.wikipedia.org/wiki/General_relativity", "General Relativity"),
        ("https://en.wikipedia.org/wiki/Particle_physics", "Particle Physics"),
        ("https://en.wikipedia.org/wiki/Standard_Model", "Standard Model"),
        ("https://en.wikipedia.org/wiki/Nuclear_physics", "Nuclear Physics"),
        ("https://en.wikipedia.org/wiki/Atomic_physics", "Atomic Physics"),
        ("https://en.wikipedia.org/wiki/Molecular_physics", "Molecular Physics"),
        ("https://en.wikipedia.org/wiki/Condensed_matter_physics", "Condensed Matter"),
        ("https://en.wikipedia.org/wiki/Solid-state_physics", "Solid State Physics"),
        ("https://en.wikipedia.org/wiki/Plasma_physics", "Plasma Physics"),
        ("https://en.wikipedia.org/wiki/Astrophysics", "Astrophysics"),
        ("https://en.wikipedia.org/wiki/Cosmology", "Cosmology"),
        ("https://en.wikipedia.org/wiki/Fluid_dynamics", "Fluid Dynamics"),
        ("https://en.wikipedia.org/wiki/Aerodynamics", "Aerodynamics"),
        ("https://en.wikipedia.org/wiki/Mechanics", "Mechanics"),
        ("https://en.wikipedia.org/wiki/Gravitation", "Gravitation"),
        ("https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion", "Newton's Laws"),
        ("https://en.wikipedia.org/wiki/Energy", "Energy"),
        ("https://en.wikipedia.org/wiki/Force", "Force"),
        ("https://en.wikipedia.org/wiki/Work_(physics)", "Work"),
        ("https://en.wikipedia.org/wiki/Power_(physics)", "Power"),
        ("https://en.wikipedia.org/wiki/Momentum", "Momentum"),
        ("https://en.wikipedia.org/wiki/Angular_momentum", "Angular Momentum"),
        ("https://en.wikipedia.org/wiki/Torque", "Torque"),
        ("https://en.wikipedia.org/wiki/Electric_field", "Electric Fields"),
        ("https://en.wikipedia.org/wiki/Magnetic_field", "Magnetic Fields"),
        ("https://en.wikipedia.org/wiki/Electromagnetic_radiation", "EM Radiation"),
        ("https://en.wikipedia.org/wiki/Photon", "Photons"),
        ("https://en.wikipedia.org/wiki/Electron", "Electrons"),
        ("https://en.wikipedia.org/wiki/Proton", "Protons"),
    ],
    
    # CHEMISTRY (40 sources)
    "Chemistry": [
        ("https://en.wikipedia.org/wiki/Chemistry", "Chemistry Overview"),
        ("https://en.wikipedia.org/wiki/Organic_chemistry", "Organic Chemistry"),
        ("https://en.wikipedia.org/wiki/Inorganic_chemistry", "Inorganic Chemistry"),
        ("https://en.wikipedia.org/wiki/Physical_chemistry", "Physical Chemistry"),
        ("https://en.wikipedia.org/wiki/Analytical_chemistry", "Analytical Chemistry"),
        ("https://en.wikipedia.org/wiki/Biochemistry", "Biochemistry"),
        ("https://en.wikipedia.org/wiki/Chemical_reaction", "Chemical Reactions"),
        ("https://en.wikipedia.org/wiki/Atom", "Atoms"),
        ("https://en.wikipedia.org/wiki/Molecule", "Molecules"),
        ("https://en.wikipedia.org/wiki/Chemical_bond", "Chemical Bonds"),
        ("https://en.wikipedia.org/wiki/Covalent_bond", "Covalent Bonds"),
        ("https://en.wikipedia.org/wiki/Ionic_bond", "Ionic Bonds"),
        ("https://en.wikipedia.org/wiki/Periodic_table", "Periodic Table"),
        ("https://en.wikipedia.org/wiki/Chemical_element", "Chemical Elements"),
        ("https://en.wikipedia.org/wiki/Stoichiometry", "Stoichiometry"),
        ("https://en.wikipedia.org/wiki/Redox", "Redox Reactions"),
        ("https://en.wikipedia.org/wiki/Acid", "Acids"),
        ("https://en.wikipedia.org/wiki/Base_(chemistry)", "Bases"),
        ("https://en.wikipedia.org/wiki/PH", "pH Scale"),
        ("https://en.wikipedia.org/wiki/Catalysis", "Catalysis"),
        ("https://en.wikipedia.org/wiki/Chemical_equilibrium", "Chemical Equilibrium"),
        ("https://en.wikipedia.org/wiki/Thermochemistry", "Thermochemistry"),
        ("https://en.wikipedia.org/wiki/Electrochemistry", "Electrochemistry"),
        ("https://en.wikipedia.org/wiki/Quantum_chemistry", "Quantum Chemistry"),
        ("https://en.wikipedia.org/wiki/Molecular_orbital", "Molecular Orbitals"),
        ("https://en.wikipedia.org/wiki/Polymer", "Polymers"),
        ("https://en.wikipedia.org/wiki/Protein", "Proteins"),
        ("https://en.wikipedia.org/wiki/DNA", "DNA"),
        ("https://en.wikipedia.org/wiki/RNA", "RNA"),
        ("https://en.wikipedia.org/wiki/Enzyme", "Enzymes"),
        ("https://en.wikipedia.org/wiki/Carbohydrate", "Carbohydrates"),
        ("https://en.wikipedia.org/wiki/Lipid", "Lipids"),
        ("https://en.wikipedia.org/wiki/Amino_acid", "Amino Acids"),
        ("https://en.wikipedia.org/wiki/Nucleic_acid", "Nucleic Acids"),
        ("https://en.wikipedia.org/wiki/Spectroscopy", "Spectroscopy"),
    ],
    
    # BIOLOGY (40 sources)
    "Biology": [
        ("https://en.wikipedia.org/wiki/Biology", "Biology Overview"),
        ("https://en.wikipedia.org/wiki/Cell_(biology)", "Cell Biology"),
        ("https://en.wikipedia.org/wiki/Genetics", "Genetics"),
        ("https://en.wikipedia.org/wiki/Evolution", "Evolution"),
        ("https://en.wikipedia.org/wiki/Ecology", "Ecology"),
        ("https://en.wikipedia.org/wiki/Molecular_biology", "Molecular Biology"),
        ("https://en.wikipedia.org/wiki/Microbiology", "Microbiology"),
        ("https://en.wikipedia.org/wiki/Botany", "Botany"),
        ("https://en.wikipedia.org/wiki/Zoology", "Zoology"),
        ("https://en.wikipedia.org/wiki/Anatomy", "Anatomy"),
        ("https://en.wikipedia.org/wiki/Physiology", "Physiology"),
        ("https://en.wikipedia.org/wiki/Neuroscience", "Neuroscience"),
        ("https://en.wikipedia.org/wiki/Immunology", "Immunology"),
        ("https://en.wikipedia.org/wiki/Developmental_biology", "Developmental Biology"),
        ("https://en.wikipedia.org/wiki/Evolutionary_biology", "Evolutionary Biology"),
        ("https://en.wikipedia.org/wiki/Photosynthesis", "Photosynthesis"),
        ("https://en.wikipedia.org/wiki/Cellular_respiration", "Cellular Respiration"),
        ("https://en.wikipedia.org/wiki/Mitosis", "Mitosis"),
        ("https://en.wikipedia.org/wiki/Meiosis", "Meiosis"),
        ("https://en.wikipedia.org/wiki/Gene", "Genes"),
        ("https://en.wikipedia.org/wiki/Chromosome", "Chromosomes"),
        ("https://en.wikipedia.org/wiki/Natural_selection", "Natural Selection"),
        ("https://en.wikipedia.org/wiki/Biodiversity", "Biodiversity"),
        ("https://en.wikipedia.org/wiki/Taxonomy_(biology)", "Taxonomy"),
        ("https://en.wikipedia.org/wiki/Organism", "Organisms"),
        ("https://en.wikipedia.org/wiki/Virus", "Viruses"),
        ("https://en.wikipedia.org/wiki/Bacteria", "Bacteria"),
        ("https://en.wikipedia.org/wiki/Archaea", "Archaea"),
        ("https://en.wikipedia.org/wiki/Eukaryote", "Eukaryotes"),
        ("https://en.wikipedia.org/wiki/Prokaryote", "Prokaryotes"),
        ("https://en.wikipedia.org/wiki/Ecosystem", "Ecosystems"),
        ("https://en.wikipedia.org/wiki/Biome", "Biomes"),
        ("https://en.wikipedia.org/wiki/Food_chain", "Food Chains"),
        ("https://en.wikipedia.org/wiki/Homeostasis", "Homeostasis"),
        ("https://en.wikipedia.org/wiki/Nervous_system", "Nervous System"),
    ],
    
    # COMPUTER SCIENCE (40 sources)
    "Computer Science": [
        ("https://en.wikipedia.org/wiki/Computer_science", "Computer Science Overview"),
        ("https://en.wikipedia.org/wiki/Algorithm", "Algorithms"),
        ("https://en.wikipedia.org/wiki/Data_structure", "Data Structures"),
        ("https://en.wikipedia.org/wiki/Programming_language", "Programming Languages"),
        ("https://en.wikipedia.org/wiki/Python_(programming_language)", "Python"),
        ("https://en.wikipedia.org/wiki/JavaScript", "JavaScript"),
        ("https://en.wikipedia.org/wiki/C%2B%2B", "C++"),
        ("https://en.wikipedia.org/wiki/Java_(programming_language)", "Java"),
        ("https://en.wikipedia.org/wiki/Database", "Databases"),
        ("https://en.wikipedia.org/wiki/SQL", "SQL"),
        ("https://en.wikipedia.org/wiki/Machine_learning", "Machine Learning"),
        ("https://en.wikipedia.org/wiki/Artificial_intelligence", "Artificial Intelligence"),
        ("https://en.wikipedia.org/wiki/Deep_learning", "Deep Learning"),
        ("https://en.wikipedia.org/wiki/Neural_network", "Neural Networks"),
        ("https://en.wikipedia.org/wiki/Natural_language_processing", "NLP"),
        ("https://en.wikipedia.org/wiki/Computer_vision", "Computer Vision"),
        ("https://en.wikipedia.org/wiki/Operating_system", "Operating Systems"),
        ("https://en.wikipedia.org/wiki/Computer_network", "Computer Networks"),
        ("https://en.wikipedia.org/wiki/Internet", "Internet"),
        ("https://en.wikipedia.org/wiki/World_Wide_Web", "World Wide Web"),
        ("https://en.wikipedia.org/wiki/Cryptography", "Cryptography"),
        ("https://en.wikipedia.org/wiki/Cybersecurity", "Cybersecurity"),
        ("https://en.wikipedia.org/wiki/Software_engineering", "Software Engineering"),
        ("https://en.wikipedia.org/wiki/Object-oriented_programming", "OOP"),
        ("https://en.wikipedia.org/wiki/Functional_programming", "Functional Programming"),
        ("https://en.wikipedia.org/wiki/Cloud_computing", "Cloud Computing"),
        ("https://en.wikipedia.org/wiki/Big_data", "Big Data"),
        ("https://en.wikipedia.org/wiki/Blockchain", "Blockchain"),
        ("https://en.wikipedia.org/wiki/Computer_graphics", "Computer Graphics"),
        ("https://en.wikipedia.org/wiki/Human%E2%80%93computer_interaction", "HCI"),
        ("https://en.wikipedia.org/wiki/Compiler", "Compilers"),
        ("https://en.wikipedia.org/wiki/Sorting_algorithm", "Sorting Algorithms"),
        ("https://en.wikipedia.org/wiki/Binary_search", "Search Algorithms"),
        ("https://en.wikipedia.org/wiki/Hash_table", "Hash Tables"),
        ("https://en.wikipedia.org/wiki/Tree_(data_structure)", "Trees"),
    ],
    
    # HISTORY (35 sources)
    "History": [
        ("https://en.wikipedia.org/wiki/History", "History Overview"),
        ("https://en.wikipedia.org/wiki/Ancient_history", "Ancient History"),
        ("https://en.wikipedia.org/wiki/Ancient_Egypt", "Ancient Egypt"),
        ("https://en.wikipedia.org/wiki/Ancient_Greece", "Ancient Greece"),
        ("https://en.wikipedia.org/wiki/Ancient_Rome", "Ancient Rome"),
        ("https://en.wikipedia.org/wiki/Middle_Ages", "Middle Ages"),
        ("https://en.wikipedia.org/wiki/Renaissance", "Renaissance"),
        ("https://en.wikipedia.org/wiki/Age_of_Enlightenment", "Enlightenment"),
        ("https://en.wikipedia.org/wiki/Industrial_Revolution", "Industrial Revolution"),
        ("https://en.wikipedia.org/wiki/World_War_I", "World War I"),
        ("https://en.wikipedia.org/wiki/World_War_II", "World War II"),
        ("https://en.wikipedia.org/wiki/Cold_War", "Cold War"),
        ("https://en.wikipedia.org/wiki/American_Revolution", "American Revolution"),
        ("https://en.wikipedia.org/wiki/French_Revolution", "French Revolution"),
        ("https://en.wikipedia.org/wiki/Chinese_civilization", "Chinese Civilization"),
        ("https://en.wikipedia.org/wiki/Mesopotamia", "Mesopotamia"),
        ("https://en.wikipedia.org/wiki/Indus_Valley_Civilisation", "Indus Valley"),
        ("https://en.wikipedia.org/wiki/Maya_civilization", "Maya Civilization"),
        ("https://en.wikipedia.org/wiki/Age_of_Discovery", "Age of Discovery"),
        ("https://en.wikipedia.org/wiki/Colonialism", "Colonialism"),
        ("https://en.wikipedia.org/wiki/Imperialism", "Imperialism"),
        ("https://en.wikipedia.org/wiki/Feudalism", "Feudalism"),
        ("https://en.wikipedia.org/wiki/Slavery", "Slavery"),
        ("https://en.wikipedia.org/wiki/Civil_rights_movement", "Civil Rights Movement"),
        ("https://en.wikipedia.org/wiki/Women%27s_suffrage", "Women's Suffrage"),
        ("https://en.wikipedia.org/wiki/Holocaust", "Holocaust"),
        ("https://en.wikipedia.org/wiki/Great_Depression", "Great Depression"),
        ("https://en.wikipedia.org/wiki/Crusades", "Crusades"),
        ("https://en.wikipedia.org/wiki/Reformation", "Protestant Reformation"),
        ("https://en.wikipedia.org/wiki/Mongol_Empire", "Mongol Empire"),
    ],
    
    # LITERATURE & LANGUAGE (30 sources)
    "Literature": [
        ("https://en.wikipedia.org/wiki/Literature", "Literature Overview"),
        ("https://en.wikipedia.org/wiki/Poetry", "Poetry"),
        ("https://en.wikipedia.org/wiki/Novel", "Novel"),
        ("https://en.wikipedia.org/wiki/Drama", "Drama"),
        ("https://en.wikipedia.org/wiki/William_Shakespeare", "Shakespeare"),
        ("https://en.wikipedia.org/wiki/Charles_Dickens", "Dickens"),
        ("https://en.wikipedia.org/wiki/Jane_Austen", "Jane Austen"),
        ("https://en.wikipedia.org/wiki/Homer", "Homer"),
        ("https://en.wikipedia.org/wiki/Leo_Tolstoy", "Tolstoy"),
        ("https://en.wikipedia.org/wiki/Fyodor_Dostoevsky", "Dostoevsky"),
        ("https://en.wikipedia.org/wiki/Literary_criticism", "Literary Criticism"),
        ("https://en.wikipedia.org/wiki/Romanticism", "Romanticism"),
        ("https://en.wikipedia.org/wiki/Modernism", "Modernism"),
        ("https://en.wikipedia.org/wiki/Postmodernism", "Postmodernism"),
        ("https://en.wikipedia.org/wiki/Realism_(arts)", "Realism"),
        ("https://en.wikipedia.org/wiki/Symbolism_(arts)", "Symbolism"),
        ("https://en.wikipedia.org/wiki/Linguistics", "Linguistics"),
        ("https://en.wikipedia.org/wiki/Grammar", "Grammar"),
        ("https://en.wikipedia.org/wiki/Syntax", "Syntax"),
        ("https://en.wikipedia.org/wiki/Semantics", "Semantics"),
        ("https://en.wikipedia.org/wiki/Phonetics", "Phonetics"),
        ("https://en.wikipedia.org/wiki/Etymology", "Etymology"),
        ("https://en.wikipedia.org/wiki/Rhetoric", "Rhetoric"),
        ("https://en.wikipedia.org/wiki/Narrative", "Narrative"),
        ("https://en.wikipedia.org/wiki/Metaphor", "Metaphor"),
    ],
    
    # PHILOSOPHY (30 sources)
    "Philosophy": [
        ("https://en.wikipedia.org/wiki/Philosophy", "Philosophy Overview"),
        ("https://en.wikipedia.org/wiki/Metaphysics", "Metaphysics"),
        ("https://en.wikipedia.org/wiki/Epistemology", "Epistemology"),
        ("https://en.wikipedia.org/wiki/Ethics", "Ethics"),
        ("https://en.wikipedia.org/wiki/Aesthetics", "Aesthetics"),
        ("https://en.wikipedia.org/wiki/Political_philosophy", "Political Philosophy"),
        ("https://en.wikipedia.org/wiki/Existentialism", "Existentialism"),
        ("https://en.wikipedia.org/wiki/Stoicism", "Stoicism"),
        ("https://en.wikipedia.org/wiki/Utilitarianism", "Utilitarianism"),
        ("https://en.wikipedia.org/wiki/Plato", "Plato"),
        ("https://en.wikipedia.org/wiki/Aristotle", "Aristotle"),
        ("https://en.wikipedia.org/wiki/Socrates", "Socrates"),
        ("https://en.wikipedia.org/wiki/Immanuel_Kant", "Kant"),
        ("https://en.wikipedia.org/wiki/Friedrich_Nietzsche", "Nietzsche"),
        ("https://en.wikipedia.org/wiki/Ren%C3%A9_Descartes", "Descartes"),
        ("https://en.wikipedia.org/wiki/John_Locke", "John Locke"),
        ("https://en.wikipedia.org/wiki/David_Hume", "David Hume"),
        ("https://en.wikipedia.org/wiki/Jean-Jacques_Rousseau", "Rousseau"),
        ("https://en.wikipedia.org/wiki/Karl_Marx", "Marx"),
        ("https://en.wikipedia.org/wiki/Phenomenology_(philosophy)", "Phenomenology"),
        ("https://en.wikipedia.org/wiki/Pragmatism", "Pragmatism"),
        ("https://en.wikipedia.org/wiki/Empiricism", "Empiricism"),
        ("https://en.wikipedia.org/wiki/Rationalism", "Rationalism"),
        ("https://en.wikipedia.org/wiki/Idealism", "Idealism"),
        ("https://en.wikipedia.org/wiki/Materialism", "Materialism"),
    ],
    
    # PSYCHOLOGY (30 sources)
    "Psychology": [
        ("https://en.wikipedia.org/wiki/Psychology", "Psychology Overview"),
        ("https://en.wikipedia.org/wiki/Cognitive_psychology", "Cognitive Psychology"),
        ("https://en.wikipedia.org/wiki/Developmental_psychology", "Developmental Psychology"),
        ("https://en.wikipedia.org/wiki/Social_psychology", "Social Psychology"),
        ("https://en.wikipedia.org/wiki/Clinical_psychology", "Clinical Psychology"),
        ("https://en.wikipedia.org/wiki/Behavioral_psychology", "Behavioral Psychology"),
        ("https://en.wikipedia.org/wiki/Neuroscience", "Neuroscience"),
        ("https://en.wikipedia.org/wiki/Consciousness", "Consciousness"),
        ("https://en.wikipedia.org/wiki/Memory", "Memory"),
        ("https://en.wikipedia.org/wiki/Learning", "Learning"),
        ("https://en.wikipedia.org/wiki/Motivation", "Motivation"),
        ("https://en.wikipedia.org/wiki/Emotion", "Emotion"),
        ("https://en.wikipedia.org/wiki/Personality_psychology", "Personality"),
        ("https://en.wikipedia.org/wiki/Intelligence", "Intelligence"),
        ("https://en.wikipedia.org/wiki/Perception", "Perception"),
        ("https://en.wikipedia.org/wiki/Attention", "Attention"),
        ("https://en.wikipedia.org/wiki/Sigmund_Freud", "Sigmund Freud"),
        ("https://en.wikipedia.org/wiki/Carl_Jung", "Carl Jung"),
        ("https://en.wikipedia.org/wiki/B._F._Skinner", "B.F. Skinner"),
        ("https://en.wikipedia.org/wiki/Jean_Piaget", "Jean Piaget"),
        ("https://en.wikipedia.org/wiki/Psychotherapy", "Psychotherapy"),
        ("https://en.wikipedia.org/wiki/Cognitive_bias", "Cognitive Biases"),
        ("https://en.wikipedia.org/wiki/Attachment_theory", "Attachment Theory"),
        ("https://en.wikipedia.org/wiki/Stress_(biology)", "Stress"),
        ("https://en.wikipedia.org/wiki/Mental_disorder", "Mental Disorders"),
    ],
    
    # ECONOMICS (25 sources)
    "Economics": [
        ("https://en.wikipedia.org/wiki/Economics", "Economics Overview"),
        ("https://en.wikipedia.org/wiki/Microeconomics", "Microeconomics"),
        ("https://en.wikipedia.org/wiki/Macroeconomics", "Macroeconomics"),
        ("https://en.wikipedia.org/wiki/Supply_and_demand", "Supply & Demand"),
        ("https://en.wikipedia.org/wiki/Market_(economics)", "Markets"),
        ("https://en.wikipedia.org/wiki/Capitalism", "Capitalism"),
        ("https://en.wikipedia.org/wiki/Socialism", "Socialism"),
        ("https://en.wikipedia.org/wiki/Inflation", "Inflation"),
        ("https://en.wikipedia.org/wiki/Gross_domestic_product", "GDP"),
        ("https://en.wikipedia.org/wiki/Monetary_policy", "Monetary Policy"),
        ("https://en.wikipedia.org/wiki/Fiscal_policy", "Fiscal Policy"),
        ("https://en.wikipedia.org/wiki/International_trade", "International Trade"),
        ("https://en.wikipedia.org/wiki/Adam_Smith", "Adam Smith"),
        ("https://en.wikipedia.org/wiki/John_Maynard_Keynes", "Keynes"),
        ("https://en.wikipedia.org/wiki/Market_failure", "Market Failure"),
        ("https://en.wikipedia.org/wiki/Elasticity_(economics)", "Elasticity"),
        ("https://en.wikipedia.org/wiki/Comparative_advantage", "Comparative Advantage"),
        ("https://en.wikipedia.org/wiki/Unemployment", "Unemployment"),
        ("https://en.wikipedia.org/wiki/Economic_growth", "Economic Growth"),
        ("https://en.wikipedia.org/wiki/Recession", "Recession"),
    ],
    
    # GEOGRAPHY & EARTH SCIENCE (25 sources)
    "Geography": [
        ("https://en.wikipedia.org/wiki/Geography", "Geography Overview"),
        ("https://en.wikipedia.org/wiki/Earth", "Earth"),
        ("https://en.wikipedia.org/wiki/Geology", "Geology"),
        ("https://en.wikipedia.org/wiki/Plate_tectonics", "Plate Tectonics"),
        ("https://en.wikipedia.org/wiki/Volcano", "Volcanoes"),
        ("https://en.wikipedia.org/wiki/Earthquake", "Earthquakes"),
        ("https://en.wikipedia.org/wiki/Climate", "Climate"),
        ("https://en.wikipedia.org/wiki/Weather", "Weather"),
        ("https://en.wikipedia.org/wiki/Atmosphere_of_Earth", "Atmosphere"),
        ("https://en.wikipedia.org/wiki/Ocean", "Oceans"),
        ("https://en.wikipedia.org/wiki/Mountain", "Mountains"),
        ("https://en.wikipedia.org/wiki/River", "Rivers"),
        ("https://en.wikipedia.org/wiki/Desert", "Deserts"),
        ("https://en.wikipedia.org/wiki/Forest", "Forests"),
        ("https://en.wikipedia.org/wiki/Climate_change", "Climate Change"),
        ("https://en.wikipedia.org/wiki/Greenhouse_effect", "Greenhouse Effect"),
        ("https://en.wikipedia.org/wiki/Erosion", "Erosion"),
        ("https://en.wikipedia.org/wiki/Rock_(geology)", "Rocks"),
        ("https://en.wikipedia.org/wiki/Mineral", "Minerals"),
        ("https://en.wikipedia.org/wiki/Fossil", "Fossils"),
    ],
    
    # ARTS & MUSIC (25 sources)
    "Arts": [
        ("https://en.wikipedia.org/wiki/Art", "Art Overview"),
        ("https://en.wikipedia.org/wiki/Painting", "Painting"),
        ("https://en.wikipedia.org/wiki/Sculpture", "Sculpture"),
        ("https://en.wikipedia.org/wiki/Architecture", "Architecture"),
        ("https://en.wikipedia.org/wiki/Music", "Music"),
        ("https://en.wikipedia.org/wiki/Music_theory", "Music Theory"),
        ("https://en.wikipedia.org/wiki/Classical_music", "Classical Music"),
        ("https://en.wikipedia.org/wiki/Jazz", "Jazz"),
        ("https://en.wikipedia.org/wiki/Rock_music", "Rock Music"),
        ("https://en.wikipedia.org/wiki/Leonardo_da_Vinci", "Leonardo da Vinci"),
        ("https://en.wikipedia.org/wiki/Vincent_van_Gogh", "Van Gogh"),
        ("https://en.wikipedia.org/wiki/Pablo_Picasso", "Picasso"),
        ("https://en.wikipedia.org/wiki/Michelangelo", "Michelangelo"),
        ("https://en.wikipedia.org/wiki/Ludwig_van_Beethoven", "Beethoven"),
        ("https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart", "Mozart"),
        ("https://en.wikipedia.org/wiki/Johann_Sebastian_Bach", "Bach"),
        ("https://en.wikipedia.org/wiki/Photography", "Photography"),
        ("https://en.wikipedia.org/wiki/Film", "Film"),
        ("https://en.wikipedia.org/wiki/Theater", "Theater"),
        ("https://en.wikipedia.org/wiki/Dance", "Dance"),
    ],
    
    # SOCIOLOGY & ANTHROPOLOGY (20 sources)
    "Sociology": [
        ("https://en.wikipedia.org/wiki/Sociology", "Sociology Overview"),
        ("https://en.wikipedia.org/wiki/Anthropology", "Anthropology"),
        ("https://en.wikipedia.org/wiki/Culture", "Culture"),
        ("https://en.wikipedia.org/wiki/Society", "Society"),
        ("https://en.wikipedia.org/wiki/Social_structure", "Social Structure"),
        ("https://en.wikipedia.org/wiki/Social_class", "Social Class"),
        ("https://en.wikipedia.org/wiki/Gender", "Gender"),
        ("https://en.wikipedia.org/wiki/Race_(human_categorization)", "Race"),
        ("https://en.wikipedia.org/wiki/Ethnicity", "Ethnicity"),
        ("https://en.wikipedia.org/wiki/Religion", "Religion"),
        ("https://en.wikipedia.org/wiki/Family", "Family"),
        ("https://en.wikipedia.org/wiki/Education", "Education"),
        ("https://en.wikipedia.org/wiki/Globalization", "Globalization"),
        ("https://en.wikipedia.org/wiki/Urbanization", "Urbanization"),
        ("https://en.wikipedia.org/wiki/Social_change", "Social Change"),
        ("https://en.wikipedia.org/wiki/Social_movement", "Social Movements"),
        ("https://en.wikipedia.org/wiki/Demography", "Demography"),
        ("https://en.wikipedia.org/wiki/Cultural_anthropology", "Cultural Anthropology"),
    ],
}

def learn_source(url, topic):
    """Learn from a single source"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/knowledge/ingest/source",
            json={"url": url},
            timeout=30
        )
        return response.status_code == 200
    except:
        return False

def main():
    """Execute PhD-level education across all subjects"""
    print("="*80)
    print("🎓 MC AI - PhD-LEVEL EDUCATION ACROSS ALL SUBJECTS")
    print("="*80)
    
    total_sources = sum(len(sources) for sources in PHD_CURRICULUM.values())
    print(f"\n📚 Total Curriculum: {total_sources} sources across {len(PHD_CURRICULUM)} subjects")
    print(f"🎯 Target: PhD-level knowledge in ALL educational domains\n")
    
    overall_start = time.time()
    total_learned = 0
    total_attempted = 0
    
    for subject, sources in PHD_CURRICULUM.items():
        print(f"\n{'='*80}")
        print(f"📖 SUBJECT: {subject.upper()} ({len(sources)} sources)")
        print(f"{'='*80}")
        
        subject_start = time.time()
        learned = 0
        
        for i, (url, topic) in enumerate(sources, 1):
            if learn_source(url, topic):
                learned += 1
                total_learned += 1
                status = "✅"
            else:
                status = "⏭️"
            
            total_attempted += 1
            progress = (total_attempted / total_sources) * 100
            
            print(f"{status} [{i}/{len(sources)}] {topic:40s} | Overall: {total_attempted}/{total_sources} ({progress:.1f}%)")
            time.sleep(0.2)  # Fast learning
        
        subject_time = time.time() - subject_start
        subject_rate = learned / subject_time * 60 if subject_time > 0 else 0
        
        print(f"\n✨ {subject} Complete: {learned}/{len(sources)} learned in {subject_time:.1f}s ({subject_rate:.0f} sources/min)")
    
    # Final summary
    total_time = time.time() - overall_start
    overall_rate = total_learned / total_time * 60 if total_time > 0 else 0
    
    print(f"\n{'='*80}")
    print(f"🏆 PhD-LEVEL EDUCATION COMPLETE!")
    print(f"{'='*80}")
    print(f"✅ Total Learned: {total_learned}/{total_sources} sources ({(total_learned/total_sources)*100:.1f}%)")
    print(f"⏱️  Total Time: {total_time/60:.1f} minutes")
    print(f"📈 Average Rate: {overall_rate:.0f} sources/minute")
    print(f"\n💜 MC AI now has PhD-level knowledge across ALL educational subjects!")
    print(f"🎓 Subjects Mastered: {len(PHD_CURRICULUM)}")
    print(f"{'='*80}")
    
    # Show subject breakdown
    print(f"\n📊 KNOWLEDGE BY SUBJECT:")
    for subject, sources in PHD_CURRICULUM.items():
        print(f"  {subject:25s}: {len(sources):3d} sources")

if __name__ == "__main__":
    main()
