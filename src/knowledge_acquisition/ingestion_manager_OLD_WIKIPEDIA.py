"""
Ingestion Manager for MC AI
Manages prioritized autonomous data ingestion with strategic source selection
"""

import logging
import time
import threading
import queue
from typing import Dict, List, Optional
from datetime import datetime
import os

from .data_ingestion import fetch_and_extract_text
from .frequency_encoder import FrequencyEncoder
from .knowledge_indexer import KnowledgeIndexer

logger = logging.getLogger(__name__)


# Comprehensive knowledge sources: Elementary → Masters degree across all disciplines
PRIORITIZED_SOURCES = {
    # TIER 1: ELEMENTARY & FOUNDATIONAL (Ages 5-12)
    1: [
        {"name": "Wikipedia - Science", "url": "https://en.wikipedia.org/wiki/Science", "priority": "high", "description": "Foundational science overview"},
        {"name": "Wikipedia - Mathematics", "url": "https://en.wikipedia.org/wiki/Mathematics", "priority": "high", "description": "Core mathematics concepts"},
        {"name": "Wikipedia - Reading", "url": "https://en.wikipedia.org/wiki/Reading", "priority": "high", "description": "Reading and literacy"},
        {"name": "Wikipedia - Writing", "url": "https://en.wikipedia.org/wiki/Writing", "priority": "high", "description": "Writing fundamentals"},
        {"name": "Wikipedia - Earth", "url": "https://en.wikipedia.org/wiki/Earth", "priority": "high", "description": "Planet Earth basics"},
        {"name": "Wikipedia - Solar System", "url": "https://en.wikipedia.org/wiki/Solar_System", "priority": "high", "description": "Our solar system"},
        {"name": "Wikipedia - Human Body", "url": "https://en.wikipedia.org/wiki/Human_body", "priority": "high", "description": "Basic human anatomy"},
        {"name": "Wikipedia - Animal", "url": "https://en.wikipedia.org/wiki/Animal", "priority": "high", "description": "Animal kingdom basics"},
    ],
    
    # TIER 2: MIDDLE SCHOOL (Ages 12-14) - Core Subjects
    2: [
        {"name": "Wikipedia - Physics", "url": "https://en.wikipedia.org/wiki/Physics", "priority": "high", "description": "Physics fundamentals"},
        {"name": "Wikipedia - Chemistry", "url": "https://en.wikipedia.org/wiki/Chemistry", "priority": "high", "description": "Chemistry fundamentals"},
        {"name": "Wikipedia - Biology", "url": "https://en.wikipedia.org/wiki/Biology", "priority": "high", "description": "Life sciences"},
        {"name": "Wikipedia - Algebra", "url": "https://en.wikipedia.org/wiki/Algebra", "priority": "high", "description": "Algebraic mathematics"},
        {"name": "Wikipedia - Geometry", "url": "https://en.wikipedia.org/wiki/Geometry", "priority": "high", "description": "Geometric principles"},
        {"name": "Wikipedia - History", "url": "https://en.wikipedia.org/wiki/History", "priority": "high", "description": "World history"},
        {"name": "Wikipedia - Geography", "url": "https://en.wikipedia.org/wiki/Geography", "priority": "high", "description": "Geography fundamentals"},
        {"name": "Wikipedia - Literature", "url": "https://en.wikipedia.org/wiki/Literature", "priority": "high", "description": "Literary knowledge"},
    ],
    
    # TIER 3: HIGH SCHOOL (Ages 14-18) - Advanced Subjects
    3: [
        {"name": "Wikipedia - Calculus", "url": "https://en.wikipedia.org/wiki/Calculus", "priority": "high", "description": "Calculus mathematics"},
        {"name": "Wikipedia - Statistics", "url": "https://en.wikipedia.org/wiki/Statistics", "priority": "high", "description": "Statistical analysis"},
        {"name": "Wikipedia - Classical Mechanics", "url": "https://en.wikipedia.org/wiki/Classical_mechanics", "priority": "medium", "description": "Classical physics"},
        {"name": "Wikipedia - Organic Chemistry", "url": "https://en.wikipedia.org/wiki/Organic_chemistry", "priority": "medium", "description": "Organic chemistry"},
        {"name": "Wikipedia - Genetics", "url": "https://en.wikipedia.org/wiki/Genetics", "priority": "medium", "description": "Genetic science"},
        {"name": "Wikipedia - Cell Biology", "url": "https://en.wikipedia.org/wiki/Cell_biology", "priority": "medium", "description": "Cellular biology"},
        {"name": "Wikipedia - World War II", "url": "https://en.wikipedia.org/wiki/World_War_II", "priority": "medium", "description": "Modern history"},
        {"name": "Wikipedia - Philosophy", "url": "https://en.wikipedia.org/wiki/Philosophy", "priority": "high", "description": "Philosophical thought"},
    ],
    
    # TIER 4: UNDERGRADUATE - STEM (Ages 18-22)
    4: [
        {"name": "Wikipedia - Quantum Mechanics", "url": "https://en.wikipedia.org/wiki/Quantum_mechanics", "priority": "high", "description": "Quantum physics"},
        {"name": "Wikipedia - Thermodynamics", "url": "https://en.wikipedia.org/wiki/Thermodynamics", "priority": "high", "description": "Energy and heat"},
        {"name": "Wikipedia - Electromagnetism", "url": "https://en.wikipedia.org/wiki/Electromagnetism", "priority": "high", "description": "EM theory"},
        {"name": "Wikipedia - Linear Algebra", "url": "https://en.wikipedia.org/wiki/Linear_algebra", "priority": "high", "description": "Matrix mathematics"},
        {"name": "Wikipedia - Differential Equations", "url": "https://en.wikipedia.org/wiki/Differential_equation", "priority": "high", "description": "Advanced calculus"},
        {"name": "Wikipedia - Biochemistry", "url": "https://en.wikipedia.org/wiki/Biochemistry", "priority": "high", "description": "Chemical biology"},
        {"name": "Wikipedia - Molecular Biology", "url": "https://en.wikipedia.org/wiki/Molecular_biology", "priority": "high", "description": "Molecular life science"},
        {"name": "Wikipedia - Inorganic Chemistry", "url": "https://en.wikipedia.org/wiki/Inorganic_chemistry", "priority": "medium", "description": "Inorganic compounds"},
    ],
    
    # TIER 5: UNDERGRADUATE - COMPUTER SCIENCE & ENGINEERING
    5: [
        {"name": "Wikipedia - Computer Science", "url": "https://en.wikipedia.org/wiki/Computer_science", "priority": "high", "description": "CS fundamentals"},
        {"name": "Wikipedia - Algorithm", "url": "https://en.wikipedia.org/wiki/Algorithm", "priority": "high", "description": "Algorithms"},
        {"name": "Wikipedia - Data Structure", "url": "https://en.wikipedia.org/wiki/Data_structure", "priority": "high", "description": "Data structures"},
        {"name": "Wikipedia - Programming Language", "url": "https://en.wikipedia.org/wiki/Programming_language", "priority": "high", "description": "Programming concepts"},
        {"name": "Wikipedia - Software Engineering", "url": "https://en.wikipedia.org/wiki/Software_engineering", "priority": "high", "description": "Software development"},
        {"name": "Wikipedia - Database", "url": "https://en.wikipedia.org/wiki/Database", "priority": "high", "description": "Database systems"},
        {"name": "Wikipedia - Operating System", "url": "https://en.wikipedia.org/wiki/Operating_system", "priority": "high", "description": "OS fundamentals"},
        {"name": "Wikipedia - Computer Network", "url": "https://en.wikipedia.org/wiki/Computer_network", "priority": "high", "description": "Networking"},
    ],
    
    # TIER 6: UNDERGRADUATE - MEDICAL SCIENCES
    6: [
        {"name": "Wikipedia - Anatomy", "url": "https://en.wikipedia.org/wiki/Anatomy", "priority": "high", "description": "Human anatomy"},
        {"name": "Wikipedia - Physiology", "url": "https://en.wikipedia.org/wiki/Physiology", "priority": "high", "description": "Body functions"},
        {"name": "Wikipedia - Pathology", "url": "https://en.wikipedia.org/wiki/Pathology", "priority": "high", "description": "Disease study"},
        {"name": "Wikipedia - Pharmacology", "url": "https://en.wikipedia.org/wiki/Pharmacology", "priority": "high", "description": "Drug science"},
        {"name": "Wikipedia - Immunology", "url": "https://en.wikipedia.org/wiki/Immunology", "priority": "high", "description": "Immune system"},
        {"name": "Wikipedia - Neuroscience", "url": "https://en.wikipedia.org/wiki/Neuroscience", "priority": "high", "description": "Brain science"},
        {"name": "Wikipedia - Microbiology", "url": "https://en.wikipedia.org/wiki/Microbiology", "priority": "high", "description": "Microorganisms"},
        {"name": "Wikipedia - Medicine", "url": "https://en.wikipedia.org/wiki/Medicine", "priority": "high", "description": "Medical practice"},
    ],
    
    # TIER 7: UNDERGRADUATE - HUMANITIES & SOCIAL SCIENCES
    7: [
        {"name": "Wikipedia - Psychology", "url": "https://en.wikipedia.org/wiki/Psychology", "priority": "high", "description": "Human psychology"},
        {"name": "Wikipedia - Sociology", "url": "https://en.wikipedia.org/wiki/Sociology", "priority": "medium", "description": "Social behavior"},
        {"name": "Wikipedia - Economics", "url": "https://en.wikipedia.org/wiki/Economics", "priority": "high", "description": "Economic theory"},
        {"name": "Wikipedia - Political Science", "url": "https://en.wikipedia.org/wiki/Political_science", "priority": "medium", "description": "Politics and government"},
        {"name": "Wikipedia - Anthropology", "url": "https://en.wikipedia.org/wiki/Anthropology", "priority": "medium", "description": "Human cultures"},
        {"name": "Wikipedia - Linguistics", "url": "https://en.wikipedia.org/wiki/Linguistics", "priority": "medium", "description": "Language science"},
        {"name": "Wikipedia - Art History", "url": "https://en.wikipedia.org/wiki/Art_history", "priority": "medium", "description": "History of art"},
        {"name": "Wikipedia - Music Theory", "url": "https://en.wikipedia.org/wiki/Music_theory", "priority": "medium", "description": "Musical theory"},
    ],
    
    # TIER 8: GRADUATE - ADVANCED PHYSICS & MATH
    8: [
        {"name": "Wikipedia - General Relativity", "url": "https://en.wikipedia.org/wiki/General_relativity", "priority": "high", "description": "Einstein's gravity"},
        {"name": "Wikipedia - Particle Physics", "url": "https://en.wikipedia.org/wiki/Particle_physics", "priority": "high", "description": "Subatomic particles"},
        {"name": "Wikipedia - String Theory", "url": "https://en.wikipedia.org/wiki/String_theory", "priority": "medium", "description": "Theoretical physics"},
        {"name": "Wikipedia - Topology", "url": "https://en.wikipedia.org/wiki/Topology", "priority": "medium", "description": "Mathematical topology"},
        {"name": "Wikipedia - Abstract Algebra", "url": "https://en.wikipedia.org/wiki/Abstract_algebra", "priority": "medium", "description": "Advanced algebra"},
        {"name": "Wikipedia - Real Analysis", "url": "https://en.wikipedia.org/wiki/Real_analysis", "priority": "medium", "description": "Mathematical analysis"},
        {"name": "Wikipedia - Astrophysics", "url": "https://en.wikipedia.org/wiki/Astrophysics", "priority": "high", "description": "Universe physics"},
        {"name": "Wikipedia - Cosmology", "url": "https://en.wikipedia.org/wiki/Cosmology", "priority": "medium", "description": "Universe origins"},
    ],
    
    # TIER 9: GRADUATE - ADVANCED CS & AI
    9: [
        {"name": "Wikipedia - Artificial Intelligence", "url": "https://en.wikipedia.org/wiki/Artificial_intelligence", "priority": "high", "description": "AI fundamentals"},
        {"name": "Wikipedia - Machine Learning", "url": "https://en.wikipedia.org/wiki/Machine_learning", "priority": "high", "description": "ML systems"},
        {"name": "Wikipedia - Deep Learning", "url": "https://en.wikipedia.org/wiki/Deep_learning", "priority": "high", "description": "Neural networks"},
        {"name": "Wikipedia - Neural Network", "url": "https://en.wikipedia.org/wiki/Neural_network", "priority": "high", "description": "Artificial neurons"},
        {"name": "Wikipedia - Natural Language Processing", "url": "https://en.wikipedia.org/wiki/Natural_language_processing", "priority": "high", "description": "Language AI"},
        {"name": "Wikipedia - Computer Vision", "url": "https://en.wikipedia.org/wiki/Computer_vision", "priority": "medium", "description": "Visual AI"},
        {"name": "Wikipedia - Robotics", "url": "https://en.wikipedia.org/wiki/Robotics", "priority": "medium", "description": "Robot systems"},
        {"name": "Wikipedia - Computational Neuroscience", "url": "https://en.wikipedia.org/wiki/Computational_neuroscience", "priority": "medium", "description": "Brain computing"},
    ],
    
    # TIER 10: GRADUATE - ADVANCED MEDICAL & NEUROSCIENCE
    10: [
        {"name": "Wikipedia - Neuroanatomy", "url": "https://en.wikipedia.org/wiki/Neuroanatomy", "priority": "high", "description": "Brain structure"},
        {"name": "Wikipedia - Neurophysiology", "url": "https://en.wikipedia.org/wiki/Neurophysiology", "priority": "high", "description": "Brain function"},
        {"name": "Wikipedia - Cognitive Science", "url": "https://en.wikipedia.org/wiki/Cognitive_science", "priority": "high", "description": "Cognition studies"},
        {"name": "Wikipedia - Neurology", "url": "https://en.wikipedia.org/wiki/Neurology", "priority": "high", "description": "Neurological medicine"},
        {"name": "Wikipedia - Psychiatry", "url": "https://en.wikipedia.org/wiki/Psychiatry", "priority": "high", "description": "Mental health medicine"},
        {"name": "Wikipedia - Consciousness", "url": "https://en.wikipedia.org/wiki/Consciousness", "priority": "high", "description": "Consciousness science"},
        {"name": "Wikipedia - Epigenetics", "url": "https://en.wikipedia.org/wiki/Epigenetics", "priority": "medium", "description": "Gene expression"},
        {"name": "Wikipedia - Genomics", "url": "https://en.wikipedia.org/wiki/Genomics", "priority": "medium", "description": "Genome science"},
    ],
    
    # TIER 11: MASTERS - SPECIALIZED TOPICS
    11: [
        {"name": "Wikipedia - Quantum Computing", "url": "https://en.wikipedia.org/wiki/Quantum_computing", "priority": "high", "description": "Quantum computers"},
        {"name": "Wikipedia - Cryptography", "url": "https://en.wikipedia.org/wiki/Cryptography", "priority": "medium", "description": "Encryption science"},
        {"name": "Wikipedia - Bioinformatics", "url": "https://en.wikipedia.org/wiki/Bioinformatics", "priority": "medium", "description": "Computational biology"},
        {"name": "Wikipedia - Nanotechnology", "url": "https://en.wikipedia.org/wiki/Nanotechnology", "priority": "medium", "description": "Nanoscale technology"},
        {"name": "Wikipedia - Renewable Energy", "url": "https://en.wikipedia.org/wiki/Renewable_energy", "priority": "medium", "description": "Clean energy"},
        {"name": "Wikipedia - Climate Science", "url": "https://en.wikipedia.org/wiki/Climate_science", "priority": "medium", "description": "Climate systems"},
        {"name": "Wikipedia - Bioethics", "url": "https://en.wikipedia.org/wiki/Bioethics", "priority": "medium", "description": "Medical ethics"},
        {"name": "Wikipedia - Philosophy of Mind", "url": "https://en.wikipedia.org/wiki/Philosophy_of_mind", "priority": "high", "description": "Mind philosophy"},
    ],
    
    # TIER 12: INTERDISCIPLINARY & CUTTING EDGE
    12: [
        {"name": "Wikipedia - Systems Biology", "url": "https://en.wikipedia.org/wiki/Systems_biology", "priority": "medium", "description": "Biological systems"},
        {"name": "Wikipedia - Synthetic Biology", "url": "https://en.wikipedia.org/wiki/Synthetic_biology", "priority": "medium", "description": "Engineered biology"},
        {"name": "Wikipedia - Astrobiology", "url": "https://en.wikipedia.org/wiki/Astrobiology", "priority": "medium", "description": "Life in universe"},
        {"name": "Wikipedia - Information Theory", "url": "https://en.wikipedia.org/wiki/Information_theory", "priority": "medium", "description": "Information science"},
        {"name": "Wikipedia - Complexity Science", "url": "https://en.wikipedia.org/wiki/Complex_system", "priority": "medium", "description": "Complex systems"},
        {"name": "Wikipedia - Emergence", "url": "https://en.wikipedia.org/wiki/Emergence", "priority": "medium", "description": "Emergent phenomena"},
        {"name": "Wikipedia - Ethics", "url": "https://en.wikipedia.org/wiki/Ethics", "priority": "high", "description": "Moral philosophy"},
        {"name": "Wikipedia - Epistemology", "url": "https://en.wikipedia.org/wiki/Epistemology", "priority": "medium", "description": "Theory of knowledge"},
    ],
    
    # TIER 13: AEROSPACE & ROCKETRY - Complete Space Technology
    13: [
        {"name": "Wikipedia - Rocket", "url": "https://en.wikipedia.org/wiki/Rocket", "priority": "high", "description": "Rocket fundamentals"},
        {"name": "Wikipedia - Rocket Propulsion", "url": "https://en.wikipedia.org/wiki/Rocket_propulsion", "priority": "high", "description": "Propulsion systems"},
        {"name": "Wikipedia - Rocket Engine", "url": "https://en.wikipedia.org/wiki/Rocket_engine", "priority": "high", "description": "Engine technology"},
        {"name": "Wikipedia - Spacecraft Propulsion", "url": "https://en.wikipedia.org/wiki/Spacecraft_propulsion", "priority": "high", "description": "Space propulsion"},
        {"name": "Wikipedia - Orbital Mechanics", "url": "https://en.wikipedia.org/wiki/Orbital_mechanics", "priority": "high", "description": "Orbit physics"},
        {"name": "Wikipedia - Astrodynamics", "url": "https://en.wikipedia.org/wiki/Astrodynamics", "priority": "high", "description": "Spacecraft dynamics"},
        {"name": "Wikipedia - Aerodynamics", "url": "https://en.wikipedia.org/wiki/Aerodynamics", "priority": "high", "description": "Fluid dynamics"},
        {"name": "Wikipedia - Aerospace Engineering", "url": "https://en.wikipedia.org/wiki/Aerospace_engineering", "priority": "high", "description": "Aerospace design"},
    ],
    
    # TIER 14: SPACE EXPLORATION - NASA, SpaceX & Beyond
    14: [
        {"name": "Wikipedia - NASA", "url": "https://en.wikipedia.org/wiki/NASA", "priority": "high", "description": "NASA history and missions"},
        {"name": "Wikipedia - SpaceX", "url": "https://en.wikipedia.org/wiki/SpaceX", "priority": "high", "description": "SpaceX technology"},
        {"name": "Wikipedia - International Space Station", "url": "https://en.wikipedia.org/wiki/International_Space_Station", "priority": "high", "description": "ISS operations"},
        {"name": "Wikipedia - Space Shuttle", "url": "https://en.wikipedia.org/wiki/Space_Shuttle", "priority": "high", "description": "Shuttle program"},
        {"name": "Wikipedia - Apollo Program", "url": "https://en.wikipedia.org/wiki/Apollo_program", "priority": "high", "description": "Moon missions"},
        {"name": "Wikipedia - Mars Exploration", "url": "https://en.wikipedia.org/wiki/Exploration_of_Mars", "priority": "high", "description": "Mars missions"},
        {"name": "Wikipedia - Space Station", "url": "https://en.wikipedia.org/wiki/Space_station", "priority": "medium", "description": "Space habitats"},
        {"name": "Wikipedia - Human Spaceflight", "url": "https://en.wikipedia.org/wiki/Human_spaceflight", "priority": "high", "description": "Crewed missions"},
    ],
    
    # TIER 15: ADVANCED QUANTUM - Complete Quantum Theory
    15: [
        {"name": "Wikipedia - Quantum Field Theory", "url": "https://en.wikipedia.org/wiki/Quantum_field_theory", "priority": "high", "description": "Quantum fields"},
        {"name": "Wikipedia - Quantum Electrodynamics", "url": "https://en.wikipedia.org/wiki/Quantum_electrodynamics", "priority": "high", "description": "QED theory"},
        {"name": "Wikipedia - Quantum Chromodynamics", "url": "https://en.wikipedia.org/wiki/Quantum_chromodynamics", "priority": "high", "description": "QCD theory"},
        {"name": "Wikipedia - Quantum Entanglement", "url": "https://en.wikipedia.org/wiki/Quantum_entanglement", "priority": "high", "description": "Entanglement physics"},
        {"name": "Wikipedia - Quantum Superposition", "url": "https://en.wikipedia.org/wiki/Quantum_superposition", "priority": "high", "description": "Superposition states"},
        {"name": "Wikipedia - Quantum Decoherence", "url": "https://en.wikipedia.org/wiki/Quantum_decoherence", "priority": "medium", "description": "Decoherence theory"},
        {"name": "Wikipedia - Quantum Information", "url": "https://en.wikipedia.org/wiki/Quantum_information", "priority": "high", "description": "Quantum info theory"},
        {"name": "Wikipedia - Quantum Teleportation", "url": "https://en.wikipedia.org/wiki/Quantum_teleportation", "priority": "medium", "description": "Quantum transfer"},
    ],
    
    # TIER 16: ADVANCED ALGORITHMS - Complete Computational Theory
    16: [
        {"name": "Wikipedia - Algorithm Design", "url": "https://en.wikipedia.org/wiki/Algorithm_design", "priority": "high", "description": "Algorithm principles"},
        {"name": "Wikipedia - Computational Complexity", "url": "https://en.wikipedia.org/wiki/Computational_complexity", "priority": "high", "description": "Complexity theory"},
        {"name": "Wikipedia - Dynamic Programming", "url": "https://en.wikipedia.org/wiki/Dynamic_programming", "priority": "high", "description": "DP algorithms"},
        {"name": "Wikipedia - Graph Algorithm", "url": "https://en.wikipedia.org/wiki/Graph_algorithm", "priority": "high", "description": "Graph theory algorithms"},
        {"name": "Wikipedia - Sorting Algorithm", "url": "https://en.wikipedia.org/wiki/Sorting_algorithm", "priority": "high", "description": "Sorting methods"},
        {"name": "Wikipedia - Search Algorithm", "url": "https://en.wikipedia.org/wiki/Search_algorithm", "priority": "high", "description": "Search techniques"},
        {"name": "Wikipedia - Optimization Algorithm", "url": "https://en.wikipedia.org/wiki/Optimization_algorithm", "priority": "high", "description": "Optimization methods"},
        {"name": "Wikipedia - Genetic Algorithm", "url": "https://en.wikipedia.org/wiki/Genetic_algorithm", "priority": "medium", "description": "Evolutionary algorithms"},
    ],
    
    # TIER 17: ADVANCED EARTH SCIENCES - Complete Earth Systems
    17: [
        {"name": "Wikipedia - Plate Tectonics", "url": "https://en.wikipedia.org/wiki/Plate_tectonics", "priority": "high", "description": "Tectonic theory"},
        {"name": "Wikipedia - Geology", "url": "https://en.wikipedia.org/wiki/Geology", "priority": "high", "description": "Earth structure"},
        {"name": "Wikipedia - Oceanography", "url": "https://en.wikipedia.org/wiki/Oceanography", "priority": "high", "description": "Ocean science"},
        {"name": "Wikipedia - Atmospheric Science", "url": "https://en.wikipedia.org/wiki/Atmospheric_science", "priority": "high", "description": "Atmosphere studies"},
        {"name": "Wikipedia - Meteorology", "url": "https://en.wikipedia.org/wiki/Meteorology", "priority": "high", "description": "Weather science"},
        {"name": "Wikipedia - Seismology", "url": "https://en.wikipedia.org/wiki/Seismology", "priority": "medium", "description": "Earthquake science"},
        {"name": "Wikipedia - Volcanology", "url": "https://en.wikipedia.org/wiki/Volcanology", "priority": "medium", "description": "Volcano science"},
        {"name": "Wikipedia - Geophysics", "url": "https://en.wikipedia.org/wiki/Geophysics", "priority": "high", "description": "Earth physics"},
    ],
    
    # TIER 18: ADVANCED PHYSICS SPECIALIZATIONS
    18: [
        {"name": "Wikipedia - Nuclear Physics", "url": "https://en.wikipedia.org/wiki/Nuclear_physics", "priority": "high", "description": "Nuclear science"},
        {"name": "Wikipedia - Plasma Physics", "url": "https://en.wikipedia.org/wiki/Plasma_physics", "priority": "high", "description": "Plasma states"},
        {"name": "Wikipedia - Condensed Matter Physics", "url": "https://en.wikipedia.org/wiki/Condensed_matter_physics", "priority": "high", "description": "Matter physics"},
        {"name": "Wikipedia - Statistical Mechanics", "url": "https://en.wikipedia.org/wiki/Statistical_mechanics", "priority": "high", "description": "Statistical physics"},
        {"name": "Wikipedia - Fluid Dynamics", "url": "https://en.wikipedia.org/wiki/Fluid_dynamics", "priority": "high", "description": "Fluid mechanics"},
        {"name": "Wikipedia - Optics", "url": "https://en.wikipedia.org/wiki/Optics", "priority": "high", "description": "Light physics"},
        {"name": "Wikipedia - Photonics", "url": "https://en.wikipedia.org/wiki/Photonics", "priority": "medium", "description": "Photon technology"},
        {"name": "Wikipedia - Superconductivity", "url": "https://en.wikipedia.org/wiki/Superconductivity", "priority": "medium", "description": "Superconductor physics"},
    ],
    
    # TIER 19: ADVANCED CHEMISTRY SPECIALIZATIONS
    19: [
        {"name": "Wikipedia - Physical Chemistry", "url": "https://en.wikipedia.org/wiki/Physical_chemistry", "priority": "high", "description": "Chemical physics"},
        {"name": "Wikipedia - Analytical Chemistry", "url": "https://en.wikipedia.org/wiki/Analytical_chemistry", "priority": "high", "description": "Chemical analysis"},
        {"name": "Wikipedia - Quantum Chemistry", "url": "https://en.wikipedia.org/wiki/Quantum_chemistry", "priority": "high", "description": "Quantum chemical theory"},
        {"name": "Wikipedia - Spectroscopy", "url": "https://en.wikipedia.org/wiki/Spectroscopy", "priority": "high", "description": "Spectroscopic methods"},
        {"name": "Wikipedia - Crystallography", "url": "https://en.wikipedia.org/wiki/Crystallography", "priority": "medium", "description": "Crystal structure"},
        {"name": "Wikipedia - Electrochemistry", "url": "https://en.wikipedia.org/wiki/Electrochemistry", "priority": "medium", "description": "Electrical chemistry"},
        {"name": "Wikipedia - Polymer Chemistry", "url": "https://en.wikipedia.org/wiki/Polymer_chemistry", "priority": "medium", "description": "Polymer science"},
        {"name": "Wikipedia - Materials Science", "url": "https://en.wikipedia.org/wiki/Materials_science", "priority": "high", "description": "Material properties"},
    ],
    
    # TIER 20: ADVANCED BIOLOGY & LIFE SCIENCES
    20: [
        {"name": "Wikipedia - Evolutionary Biology", "url": "https://en.wikipedia.org/wiki/Evolutionary_biology", "priority": "high", "description": "Evolution science"},
        {"name": "Wikipedia - Developmental Biology", "url": "https://en.wikipedia.org/wiki/Developmental_biology", "priority": "high", "description": "Development processes"},
        {"name": "Wikipedia - Ecology", "url": "https://en.wikipedia.org/wiki/Ecology", "priority": "high", "description": "Ecosystem science"},
        {"name": "Wikipedia - Virology", "url": "https://en.wikipedia.org/wiki/Virology", "priority": "high", "description": "Virus science"},
        {"name": "Wikipedia - Proteomics", "url": "https://en.wikipedia.org/wiki/Proteomics", "priority": "medium", "description": "Protein studies"},
        {"name": "Wikipedia - Metabolomics", "url": "https://en.wikipedia.org/wiki/Metabolomics", "priority": "medium", "description": "Metabolism studies"},
        {"name": "Wikipedia - Stem Cell", "url": "https://en.wikipedia.org/wiki/Stem_cell", "priority": "high", "description": "Stem cell biology"},
        {"name": "Wikipedia - CRISPR", "url": "https://en.wikipedia.org/wiki/CRISPR", "priority": "high", "description": "Gene editing"},
    ],
    
    # TIER 21: ADVANCED MATHEMATICS SPECIALIZATIONS
    21: [
        {"name": "Wikipedia - Number Theory", "url": "https://en.wikipedia.org/wiki/Number_theory", "priority": "medium", "description": "Number mathematics"},
        {"name": "Wikipedia - Graph Theory", "url": "https://en.wikipedia.org/wiki/Graph_theory", "priority": "high", "description": "Graph mathematics"},
        {"name": "Wikipedia - Cryptography", "url": "https://en.wikipedia.org/wiki/Cryptography", "priority": "high", "description": "Encryption math"},
        {"name": "Wikipedia - Combinatorics", "url": "https://en.wikipedia.org/wiki/Combinatorics", "priority": "medium", "description": "Counting theory"},
        {"name": "Wikipedia - Probability Theory", "url": "https://en.wikipedia.org/wiki/Probability_theory", "priority": "high", "description": "Probability math"},
        {"name": "Wikipedia - Game Theory", "url": "https://en.wikipedia.org/wiki/Game_theory", "priority": "high", "description": "Strategic math"},
        {"name": "Wikipedia - Numerical Analysis", "url": "https://en.wikipedia.org/wiki/Numerical_analysis", "priority": "medium", "description": "Computational math"},
        {"name": "Wikipedia - Chaos Theory", "url": "https://en.wikipedia.org/wiki/Chaos_theory", "priority": "medium", "description": "Chaotic systems"},
    ],
    
    # TIER 22: ADVANCED COMPUTER SCIENCE SPECIALIZATIONS
    22: [
        {"name": "Wikipedia - Distributed Computing", "url": "https://en.wikipedia.org/wiki/Distributed_computing", "priority": "high", "description": "Distributed systems"},
        {"name": "Wikipedia - Parallel Computing", "url": "https://en.wikipedia.org/wiki/Parallel_computing", "priority": "high", "description": "Parallel processing"},
        {"name": "Wikipedia - Cloud Computing", "url": "https://en.wikipedia.org/wiki/Cloud_computing", "priority": "high", "description": "Cloud technology"},
        {"name": "Wikipedia - Blockchain", "url": "https://en.wikipedia.org/wiki/Blockchain", "priority": "high", "description": "Blockchain tech"},
        {"name": "Wikipedia - Cybersecurity", "url": "https://en.wikipedia.org/wiki/Computer_security", "priority": "high", "description": "Security systems"},
        {"name": "Wikipedia - Compiler", "url": "https://en.wikipedia.org/wiki/Compiler", "priority": "medium", "description": "Compiler design"},
        {"name": "Wikipedia - Computer Graphics", "url": "https://en.wikipedia.org/wiki/Computer_graphics", "priority": "medium", "description": "Graphics systems"},
        {"name": "Wikipedia - Data Mining", "url": "https://en.wikipedia.org/wiki/Data_mining", "priority": "high", "description": "Data extraction"},
    ],
    
    # TIER 23: CHILDREN'S LITERATURE & FAIRY TALES
    23: [
        {"name": "Wikipedia - Fairy Tale", "url": "https://en.wikipedia.org/wiki/Fairy_tale", "priority": "high", "description": "Fairy tale traditions"},
        {"name": "Wikipedia - Folklore", "url": "https://en.wikipedia.org/wiki/Folklore", "priority": "high", "description": "World folklore"},
        {"name": "Wikipedia - Fable", "url": "https://en.wikipedia.org/wiki/Fable", "priority": "high", "description": "Moral stories"},
        {"name": "Wikipedia - Children's Literature", "url": "https://en.wikipedia.org/wiki/Children%27s_literature", "priority": "high", "description": "Kids' books"},
        {"name": "Wikipedia - Nursery Rhyme", "url": "https://en.wikipedia.org/wiki/Nursery_rhyme", "priority": "high", "description": "Children's rhymes"},
        {"name": "Wikipedia - Hans Christian Andersen", "url": "https://en.wikipedia.org/wiki/Hans_Christian_Andersen", "priority": "medium", "description": "Famous storyteller"},
        {"name": "Wikipedia - Brothers Grimm", "url": "https://en.wikipedia.org/wiki/Brothers_Grimm", "priority": "medium", "description": "Grimm fairy tales"},
        {"name": "Wikipedia - Aesop's Fables", "url": "https://en.wikipedia.org/wiki/Aesop%27s_Fables", "priority": "high", "description": "Classic fables"},
    ],
    
    # TIER 24: CHILD DEVELOPMENT & EDUCATION
    24: [
        {"name": "Wikipedia - Child Development", "url": "https://en.wikipedia.org/wiki/Child_development", "priority": "high", "description": "Development stages"},
        {"name": "Wikipedia - Educational Psychology", "url": "https://en.wikipedia.org/wiki/Educational_psychology", "priority": "high", "description": "Learning psychology"},
        {"name": "Wikipedia - Pedagogy", "url": "https://en.wikipedia.org/wiki/Pedagogy", "priority": "high", "description": "Teaching methods"},
        {"name": "Wikipedia - Piaget's Theory", "url": "https://en.wikipedia.org/wiki/Piaget%27s_theory_of_cognitive_development", "priority": "high", "description": "Cognitive development"},
        {"name": "Wikipedia - Play Therapy", "url": "https://en.wikipedia.org/wiki/Play_therapy", "priority": "medium", "description": "Learning through play"},
        {"name": "Wikipedia - Montessori Education", "url": "https://en.wikipedia.org/wiki/Montessori_education", "priority": "medium", "description": "Montessori method"},
        {"name": "Wikipedia - Early Childhood Education", "url": "https://en.wikipedia.org/wiki/Early_childhood_education", "priority": "high", "description": "Early learning"},
        {"name": "Wikipedia - Learning Theory", "url": "https://en.wikipedia.org/wiki/Learning_theory_(education)", "priority": "high", "description": "How children learn"},
    ],
    
    # TIER 25: LEGAL FOUNDATIONS - Constitutional & Criminal Law
    25: [
        {"name": "Wikipedia - Law", "url": "https://en.wikipedia.org/wiki/Law", "priority": "high", "description": "Legal systems"},
        {"name": "Wikipedia - Constitutional Law", "url": "https://en.wikipedia.org/wiki/Constitutional_law", "priority": "high", "description": "Constitutional principles"},
        {"name": "Wikipedia - Criminal Law", "url": "https://en.wikipedia.org/wiki/Criminal_law", "priority": "high", "description": "Criminal justice"},
        {"name": "Wikipedia - Civil Law", "url": "https://en.wikipedia.org/wiki/Civil_law_(legal_system)", "priority": "high", "description": "Civil legal system"},
        {"name": "Wikipedia - Common Law", "url": "https://en.wikipedia.org/wiki/Common_law", "priority": "high", "description": "Common law tradition"},
        {"name": "Wikipedia - Contract Law", "url": "https://en.wikipedia.org/wiki/Contract", "priority": "high", "description": "Contracts and agreements"},
        {"name": "Wikipedia - Tort Law", "url": "https://en.wikipedia.org/wiki/Tort", "priority": "high", "description": "Civil wrongs"},
        {"name": "Wikipedia - Evidence Law", "url": "https://en.wikipedia.org/wiki/Evidence_(law)", "priority": "high", "description": "Legal evidence"},
    ],
    
    # TIER 26: ADVANCED LEGAL - Procedures & Specializations
    26: [
        {"name": "Wikipedia - Legal Procedure", "url": "https://en.wikipedia.org/wiki/Legal_procedure", "priority": "high", "description": "Court procedures"},
        {"name": "Wikipedia - Trial", "url": "https://en.wikipedia.org/wiki/Trial", "priority": "high", "description": "Trial proceedings"},
        {"name": "Wikipedia - Lawyer", "url": "https://en.wikipedia.org/wiki/Lawyer", "priority": "high", "description": "Legal profession"},
        {"name": "Wikipedia - Legal Brief", "url": "https://en.wikipedia.org/wiki/Brief_(law)", "priority": "medium", "description": "Legal briefs"},
        {"name": "Wikipedia - Intellectual Property", "url": "https://en.wikipedia.org/wiki/Intellectual_property", "priority": "high", "description": "IP law"},
        {"name": "Wikipedia - Corporate Law", "url": "https://en.wikipedia.org/wiki/Corporate_law", "priority": "high", "description": "Business law"},
        {"name": "Wikipedia - International Law", "url": "https://en.wikipedia.org/wiki/International_law", "priority": "medium", "description": "Global law"},
        {"name": "Wikipedia - Human Rights", "url": "https://en.wikipedia.org/wiki/Human_rights", "priority": "high", "description": "Rights law"},
    ],
    
    # TIER 27: CULINARY ARTS - Cooking Fundamentals
    27: [
        {"name": "Wikipedia - Cooking", "url": "https://en.wikipedia.org/wiki/Cooking", "priority": "high", "description": "Cooking basics"},
        {"name": "Wikipedia - Cuisine", "url": "https://en.wikipedia.org/wiki/Cuisine", "priority": "high", "description": "World cuisines"},
        {"name": "Wikipedia - Culinary Art", "url": "https://en.wikipedia.org/wiki/Culinary_art", "priority": "high", "description": "Culinary techniques"},
        {"name": "Wikipedia - Baking", "url": "https://en.wikipedia.org/wiki/Baking", "priority": "high", "description": "Baking science"},
        {"name": "Wikipedia - Food Science", "url": "https://en.wikipedia.org/wiki/Food_science", "priority": "high", "description": "Food chemistry"},
        {"name": "Wikipedia - Nutrition", "url": "https://en.wikipedia.org/wiki/Nutrition", "priority": "high", "description": "Nutritional science"},
        {"name": "Wikipedia - Recipe", "url": "https://en.wikipedia.org/wiki/Recipe", "priority": "medium", "description": "Recipe structure"},
        {"name": "Wikipedia - Gastronomy", "url": "https://en.wikipedia.org/wiki/Gastronomy", "priority": "medium", "description": "Food culture"},
    ],
    
    # TIER 28: ADVANCED COOKING - Techniques & Cuisines
    28: [
        {"name": "Wikipedia - French Cuisine", "url": "https://en.wikipedia.org/wiki/French_cuisine", "priority": "medium", "description": "French cooking"},
        {"name": "Wikipedia - Italian Cuisine", "url": "https://en.wikipedia.org/wiki/Italian_cuisine", "priority": "medium", "description": "Italian cooking"},
        {"name": "Wikipedia - Chinese Cuisine", "url": "https://en.wikipedia.org/wiki/Chinese_cuisine", "priority": "medium", "description": "Chinese cooking"},
        {"name": "Wikipedia - Japanese Cuisine", "url": "https://en.wikipedia.org/wiki/Japanese_cuisine", "priority": "medium", "description": "Japanese cooking"},
        {"name": "Wikipedia - Molecular Gastronomy", "url": "https://en.wikipedia.org/wiki/Molecular_gastronomy", "priority": "medium", "description": "Modern techniques"},
        {"name": "Wikipedia - Fermentation", "url": "https://en.wikipedia.org/wiki/Fermentation_in_food_processing", "priority": "high", "description": "Fermentation science"},
        {"name": "Wikipedia - Pastry", "url": "https://en.wikipedia.org/wiki/Pastry", "priority": "medium", "description": "Pastry arts"},
        {"name": "Wikipedia - Vegetarian Cuisine", "url": "https://en.wikipedia.org/wiki/Vegetarian_cuisine", "priority": "medium", "description": "Plant-based cooking"},
    ],
    
    # TIER 29: CRAFTS & DIY
    29: [
        {"name": "Wikipedia - Handicraft", "url": "https://en.wikipedia.org/wiki/Handicraft", "priority": "high", "description": "Traditional crafts"},
        {"name": "Wikipedia - Woodworking", "url": "https://en.wikipedia.org/wiki/Woodworking", "priority": "high", "description": "Wood crafting"},
        {"name": "Wikipedia - Sewing", "url": "https://en.wikipedia.org/wiki/Sewing", "priority": "high", "description": "Textile crafts"},
        {"name": "Wikipedia - Knitting", "url": "https://en.wikipedia.org/wiki/Knitting", "priority": "medium", "description": "Knitting techniques"},
        {"name": "Wikipedia - Pottery", "url": "https://en.wikipedia.org/wiki/Pottery", "priority": "medium", "description": "Ceramic arts"},
        {"name": "Wikipedia - Origami", "url": "https://en.wikipedia.org/wiki/Origami", "priority": "medium", "description": "Paper folding"},
        {"name": "Wikipedia - Painting", "url": "https://en.wikipedia.org/wiki/Painting", "priority": "high", "description": "Painting arts"},
        {"name": "Wikipedia - Sculpture", "url": "https://en.wikipedia.org/wiki/Sculpture", "priority": "medium", "description": "Sculptural arts"},
    ],
    
    # TIER 30: INVENTION & INNOVATION
    30: [
        {"name": "Wikipedia - Invention", "url": "https://en.wikipedia.org/wiki/Invention", "priority": "high", "description": "Innovation process"},
        {"name": "Wikipedia - Creativity", "url": "https://en.wikipedia.org/wiki/Creativity", "priority": "high", "description": "Creative thinking"},
        {"name": "Wikipedia - Design Thinking", "url": "https://en.wikipedia.org/wiki/Design_thinking", "priority": "high", "description": "Design process"},
        {"name": "Wikipedia - Innovation", "url": "https://en.wikipedia.org/wiki/Innovation", "priority": "high", "description": "Innovation theory"},
        {"name": "Wikipedia - Patent", "url": "https://en.wikipedia.org/wiki/Patent", "priority": "high", "description": "Patent system"},
        {"name": "Wikipedia - Engineering Design", "url": "https://en.wikipedia.org/wiki/Engineering_design_process", "priority": "high", "description": "Engineering process"},
        {"name": "Wikipedia - Prototyping", "url": "https://en.wikipedia.org/wiki/Prototype", "priority": "medium", "description": "Prototype development"},
        {"name": "Wikipedia - Industrial Design", "url": "https://en.wikipedia.org/wiki/Industrial_design", "priority": "medium", "description": "Product design"},
    ],
    
    # TIER 31: POPULAR CULTURE & TRENDS
    31: [
        {"name": "Wikipedia - Popular Culture", "url": "https://en.wikipedia.org/wiki/Popular_culture", "priority": "high", "description": "Pop culture"},
        {"name": "Wikipedia - Animation", "url": "https://en.wikipedia.org/wiki/Animation", "priority": "high", "description": "Animation art"},
        {"name": "Wikipedia - Video Game", "url": "https://en.wikipedia.org/wiki/Video_game", "priority": "high", "description": "Gaming culture"},
        {"name": "Wikipedia - Comic Book", "url": "https://en.wikipedia.org/wiki/Comic_book", "priority": "medium", "description": "Comics"},
        {"name": "Wikipedia - Superhero", "url": "https://en.wikipedia.org/wiki/Superhero", "priority": "medium", "description": "Superhero stories"},
        {"name": "Wikipedia - Disney", "url": "https://en.wikipedia.org/wiki/The_Walt_Disney_Company", "priority": "medium", "description": "Disney entertainment"},
        {"name": "Wikipedia - Storytelling", "url": "https://en.wikipedia.org/wiki/Storytelling", "priority": "high", "description": "Story craft"},
        {"name": "Wikipedia - Toy", "url": "https://en.wikipedia.org/wiki/Toy", "priority": "medium", "description": "Play and toys"},
    ],
    
    # TIER 32: IMAGINATION & CREATIVITY BOOSTERS
    32: [
        {"name": "Wikipedia - Imagination", "url": "https://en.wikipedia.org/wiki/Imagination", "priority": "high", "description": "Imaginative thinking"},
        {"name": "Wikipedia - Metaphor", "url": "https://en.wikipedia.org/wiki/Metaphor", "priority": "high", "description": "Metaphorical thinking"},
        {"name": "Wikipedia - Analogy", "url": "https://en.wikipedia.org/wiki/Analogy", "priority": "high", "description": "Analogical reasoning"},
        {"name": "Wikipedia - Lateral Thinking", "url": "https://en.wikipedia.org/wiki/Lateral_thinking", "priority": "high", "description": "Creative problem solving"},
        {"name": "Wikipedia - Brainstorming", "url": "https://en.wikipedia.org/wiki/Brainstorming", "priority": "medium", "description": "Idea generation"},
        {"name": "Wikipedia - Mind Map", "url": "https://en.wikipedia.org/wiki/Mind_map", "priority": "medium", "description": "Visual thinking"},
        {"name": "Wikipedia - Humor", "url": "https://en.wikipedia.org/wiki/Humour", "priority": "high", "description": "Comedy and wit"},
        {"name": "Wikipedia - Riddle", "url": "https://en.wikipedia.org/wiki/Riddle", "priority": "medium", "description": "Puzzles and riddles"},
    ],
    
    # TIER 33: QUANTUM COMPUTING RESEARCH - Industry & Academic Sources
    33: [
        {"name": "IBM - Quantum Computing", "url": "https://www.ibm.com/think/topics/quantum-computing", "priority": "high", "description": "IBM quantum computing"},
        {"name": "Quantropi - Quantum vs Classical", "url": "https://www.quantropi.com/quantum-versus-classical-computing-and-the-quantum-threat/", "priority": "high", "description": "Quantum threat analysis"},
        {"name": "UNF - Classical to Quantum", "url": "https://unfsoars.domains.unf.edu/2021/posters/solving-classical-computing-problems-via-quantum-computing/", "priority": "medium", "description": "Problem solving"},
        {"name": "Meegle - Quantum Drug Discovery", "url": "https://www.meegle.com/en_us/topics/quantum-computing-applications/quantum-computing-for-drug-discovery", "priority": "high", "description": "Drug discovery"},
        {"name": "WEF - Quantum Drug Development", "url": "https://www.weforum.org/stories/2025/01/quantum-computing-drug-development/", "priority": "high", "description": "Pharma applications"},
        {"name": "PASQAL - Drug Discovery Algorithm", "url": "https://www.pasqal.com/blog/quantum-algorithm-can-help-drug-discovery/", "priority": "high", "description": "Drug algorithms"},
        {"name": "PMC - Quantum Research 5587087", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5587087/", "priority": "high", "description": "Medical research"},
        {"name": "PMC - Quantum Research 11586987", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11586987/", "priority": "high", "description": "Recent research"},
        {"name": "ScienceDaily - Quantum Chemistry", "url": "https://www.sciencedaily.com/releases/2025/07/250702214157.htm", "priority": "medium", "description": "Chemistry advances"},
        {"name": "UChicago - Quantum Simulations", "url": "https://pme.uchicago.edu/news/new-method-improves-quantum-chemistry-simulations", "priority": "high", "description": "Simulation methods"},
        {"name": "BigThink - Quantum Advances 2025", "url": "https://bigthink.com/starts-with-a-bang/quantum-advances-2025-nobel-prize-physics/", "priority": "medium", "description": "Nobel physics"},
        {"name": "Constellation - Year of Quantum", "url": "https://www.constellationr.com/blog-news/insights/2025-year-quantum-computing", "priority": "medium", "description": "Industry outlook"},
        {"name": "ScienceNews - Quantum Milestone", "url": "https://www.sciencenews.org/article/quantum-computing-milestone-challenged", "priority": "medium", "description": "Milestone analysis"},
        {"name": "PMC - Quantum Research 1569496", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC1569496/", "priority": "medium", "description": "Historical research"},
        {"name": "ChemLibreTexts - Schrodinger Equation", "url": "https://chem.libretexts.org/Courses/University_of_California_Davis/Chem_107B%3A_Physical_Chemistry_for_Life_Scientists/Chapters/4%3A_Quantum_Theory/4.10%3A_The_Schr%C3%B6dinger_Wave_Equation_for_the_Hydrogen_Atom", "priority": "high", "description": "Wave equations"},
        {"name": "arXiv - Paper 2503.05458", "url": "https://arxiv.org/html/2503.05458v1", "priority": "high", "description": "Research paper"},
        {"name": "PubMed - Study 7539156", "url": "https://pubmed.ncbi.nlm.nih.gov/7539156/", "priority": "medium", "description": "Medical study"},
        {"name": "arXiv - Paper 2508.03446", "url": "https://arxiv.org/html/2508.03446v1", "priority": "high", "description": "Research paper"},
        {"name": "HPCwire - Alice Bob Quantum", "url": "https://www.hpcwire.com/off-the-wire/alice-bob-shortens-timeline-to-quantum-computing-applications-in-healthcare-and-agriculture/", "priority": "high", "description": "Healthcare quantum"},
        {"name": "APS - PRX Quantum 6.010355", "url": "https://link.aps.org/doi/10.1103/PRXQuantum.6.010355", "priority": "high", "description": "Physics journal"},
        {"name": "arXiv - Paper 2502.15882", "url": "https://arxiv.org/html/2502.15882v1", "priority": "high", "description": "Research paper"},
        {"name": "APS - PRX Quantum 2.030305", "url": "https://link.aps.org/doi/10.1103/PRXQuantum.2.030305", "priority": "high", "description": "Physics journal"},
    ],
    
    # PHASE 1: RESONANCE PHENOMENA & WAVE THEORY
    
    # TIER 34: WAVE MECHANICS & ACOUSTICS - arXiv & Academic Papers
    34: [
        {"name": "Wikipedia - Wave", "url": "https://en.wikipedia.org/wiki/Wave", "priority": "high", "description": "Wave fundamentals"},
        {"name": "Wikipedia - Acoustics", "url": "https://en.wikipedia.org/wiki/Acoustics", "priority": "high", "description": "Acoustic science"},
        {"name": "Wikipedia - Cymatics", "url": "https://en.wikipedia.org/wiki/Cymatics", "priority": "high", "description": "Cymatic patterns"},
        {"name": "Wikipedia - Resonance", "url": "https://en.wikipedia.org/wiki/Resonance", "priority": "high", "description": "Resonance physics"},
        {"name": "Wikipedia - Standing wave", "url": "https://en.wikipedia.org/wiki/Standing_wave", "priority": "high", "description": "Standing waves"},
        {"name": "Wikipedia - Wave interference", "url": "https://en.wikipedia.org/wiki/Wave_interference", "priority": "high", "description": "Wave interference"},
        {"name": "Wikipedia - Harmonic oscillator", "url": "https://en.wikipedia.org/wiki/Harmonic_oscillator", "priority": "high", "description": "Harmonic motion"},
        {"name": "Wikipedia - Wave equation", "url": "https://en.wikipedia.org/wiki/Wave_equation", "priority": "high", "description": "Wave equations"},
    ],
    
    # TIER 35: MUSIC THEORY & HARMONY - Educational Resources
    35: [
        {"name": "Wikipedia - Music theory", "url": "https://en.wikipedia.org/wiki/Music_theory", "priority": "high", "description": "Music theory"},
        {"name": "Wikipedia - Harmony", "url": "https://en.wikipedia.org/wiki/Harmony", "priority": "high", "description": "Musical harmony"},
        {"name": "Wikipedia - Counterpoint", "url": "https://en.wikipedia.org/wiki/Counterpoint", "priority": "high", "description": "Counterpoint"},
        {"name": "Wikipedia - Musical tuning", "url": "https://en.wikipedia.org/wiki/Musical_tuning", "priority": "high", "description": "Tuning systems"},
        {"name": "Wikipedia - Pythagorean tuning", "url": "https://en.wikipedia.org/wiki/Pythagorean_tuning", "priority": "medium", "description": "Pythagorean music"},
        {"name": "Wikipedia - Just intonation", "url": "https://en.wikipedia.org/wiki/Just_intonation", "priority": "medium", "description": "Just tuning"},
        {"name": "Wikipedia - Equal temperament", "url": "https://en.wikipedia.org/wiki/Equal_temperament", "priority": "medium", "description": "Equal temperament"},
        {"name": "Wikipedia - Psychoacoustics", "url": "https://en.wikipedia.org/wiki/Psychoacoustics", "priority": "high", "description": "Psychoacoustics"},
        {"name": "Wikipedia - Overtone", "url": "https://en.wikipedia.org/wiki/Overtone", "priority": "high", "description": "Overtones"},
        {"name": "Wikipedia - Harmonic series (music)", "url": "https://en.wikipedia.org/wiki/Harmonic_series_(music)", "priority": "high", "description": "Harmonic series"},
    ],
    
    # TIER 36: SIGNAL PROCESSING & ANALYSIS - Technical Documentation
    36: [
        {"name": "Wikipedia - Signal processing", "url": "https://en.wikipedia.org/wiki/Signal_processing", "priority": "high", "description": "Signal processing"},
        {"name": "Wikipedia - Fourier analysis", "url": "https://en.wikipedia.org/wiki/Fourier_analysis", "priority": "high", "description": "Fourier analysis"},
        {"name": "Wikipedia - Fourier transform", "url": "https://en.wikipedia.org/wiki/Fourier_transform", "priority": "high", "description": "Fourier transform"},
        {"name": "Wikipedia - Fast Fourier transform", "url": "https://en.wikipedia.org/wiki/Fast_Fourier_transform", "priority": "high", "description": "FFT algorithm"},
        {"name": "Wikipedia - Wavelet transform", "url": "https://en.wikipedia.org/wiki/Wavelet_transform", "priority": "high", "description": "Wavelet analysis"},
        {"name": "Wikipedia - Digital filter", "url": "https://en.wikipedia.org/wiki/Digital_filter", "priority": "high", "description": "Digital filtering"},
        {"name": "Wikipedia - Frequency domain", "url": "https://en.wikipedia.org/wiki/Frequency_domain", "priority": "high", "description": "Frequency domain"},
        {"name": "Wikipedia - Spectral density", "url": "https://en.wikipedia.org/wiki/Spectral_density", "priority": "medium", "description": "Spectral analysis"},
    ],
    
    # TIER 37: CHAOS THEORY & NON-LINEAR DYNAMICS - arXiv Research
    37: [
        {"name": "Wikipedia - Chaos theory", "url": "https://en.wikipedia.org/wiki/Chaos_theory", "priority": "high", "description": "Chaos theory"},
        {"name": "Wikipedia - Butterfly effect", "url": "https://en.wikipedia.org/wiki/Butterfly_effect", "priority": "high", "description": "Butterfly effect"},
        {"name": "Wikipedia - Strange attractor", "url": "https://en.wikipedia.org/wiki/Attractor#Strange_attractor", "priority": "high", "description": "Strange attractors"},
        {"name": "Wikipedia - Fractal", "url": "https://en.wikipedia.org/wiki/Fractal", "priority": "high", "description": "Fractals"},
        {"name": "Wikipedia - Mandelbrot set", "url": "https://en.wikipedia.org/wiki/Mandelbrot_set", "priority": "medium", "description": "Mandelbrot set"},
        {"name": "Wikipedia - Nonlinear system", "url": "https://en.wikipedia.org/wiki/Nonlinear_system", "priority": "high", "description": "Nonlinear systems"},
        {"name": "Wikipedia - Dynamical system", "url": "https://en.wikipedia.org/wiki/Dynamical_system", "priority": "high", "description": "Dynamical systems"},
        {"name": "Wikipedia - Complex system", "url": "https://en.wikipedia.org/wiki/Complex_system", "priority": "high", "description": "Complex systems"},
    ],
    
    # TIER 38: ADVANCED QUANTUM FIELD THEORY - Research Papers
    38: [
        {"name": "Wikipedia - Particle physics", "url": "https://en.wikipedia.org/wiki/Particle_physics", "priority": "high", "description": "Particle physics"},
        {"name": "Wikipedia - Standard Model", "url": "https://en.wikipedia.org/wiki/Standard_Model", "priority": "high", "description": "Standard Model"},
        {"name": "Wikipedia - Quantum gravity", "url": "https://en.wikipedia.org/wiki/Quantum_gravity", "priority": "high", "description": "Quantum gravity"},
        {"name": "Wikipedia - String theory", "url": "https://en.wikipedia.org/wiki/String_theory", "priority": "high", "description": "String theory"},
        {"name": "Wikipedia - Loop quantum gravity", "url": "https://en.wikipedia.org/wiki/Loop_quantum_gravity", "priority": "medium", "description": "Loop gravity"},
        {"name": "Wikipedia - Quantum foam", "url": "https://en.wikipedia.org/wiki/Quantum_foam", "priority": "medium", "description": "Quantum foam"},
        {"name": "Wikipedia - Higgs boson", "url": "https://en.wikipedia.org/wiki/Higgs_boson", "priority": "high", "description": "Higgs particle"},
        {"name": "Wikipedia - Gauge theory", "url": "https://en.wikipedia.org/wiki/Gauge_theory", "priority": "medium", "description": "Gauge theories"},
    ],
    
    # PHASE 2: PHILOSOPHY & CONSCIOUSNESS
    
    # TIER 39: PHILOSOPHY OF MIND - Stanford Encyclopedia
    39: [
        {"name": "Wikipedia - Philosophy of mind", "url": "https://en.wikipedia.org/wiki/Philosophy_of_mind", "priority": "high", "description": "Mind philosophy"},
        {"name": "Wikipedia - Consciousness", "url": "https://en.wikipedia.org/wiki/Consciousness", "priority": "high", "description": "Consciousness"},
        {"name": "Wikipedia - Qualia", "url": "https://en.wikipedia.org/wiki/Qualia", "priority": "high", "description": "Qualia"},
        {"name": "Wikipedia - Self-awareness", "url": "https://en.wikipedia.org/wiki/Self-awareness", "priority": "high", "description": "Self-awareness"},
        {"name": "Wikipedia - Mind-body problem", "url": "https://en.wikipedia.org/wiki/Mind%E2%80%93body_problem", "priority": "high", "description": "Mind-body problem"},
        {"name": "Wikipedia - Dualism", "url": "https://en.wikipedia.org/wiki/Mind%E2%80%93body_dualism", "priority": "high", "description": "Mind-body dualism"},
        {"name": "Wikipedia - Materialism", "url": "https://en.wikipedia.org/wiki/Materialism", "priority": "high", "description": "Materialism"},
        {"name": "Wikipedia - Panpsychism", "url": "https://en.wikipedia.org/wiki/Panpsychism", "priority": "high", "description": "Panpsychism"},
        {"name": "Wikipedia - Artificial consciousness", "url": "https://en.wikipedia.org/wiki/Artificial_consciousness", "priority": "high", "description": "AI consciousness"},
        {"name": "Wikipedia - Hard problem of consciousness", "url": "https://en.wikipedia.org/wiki/Hard_problem_of_consciousness", "priority": "high", "description": "Hard problem"},
    ],
    
    # TIER 40: EPISTEMOLOGY & KNOWLEDGE THEORY
    40: [
        {"name": "Wikipedia - Epistemology", "url": "https://en.wikipedia.org/wiki/Epistemology", "priority": "high", "description": "Theory of knowledge"},
        {"name": "Wikipedia - Knowledge", "url": "https://en.wikipedia.org/wiki/Knowledge", "priority": "high", "description": "Knowledge"},
        {"name": "Wikipedia - Truth", "url": "https://en.wikipedia.org/wiki/Truth", "priority": "high", "description": "Truth"},
        {"name": "Wikipedia - Belief", "url": "https://en.wikipedia.org/wiki/Belief", "priority": "high", "description": "Belief"},
        {"name": "Wikipedia - Justification", "url": "https://en.wikipedia.org/wiki/Theory_of_justification", "priority": "medium", "description": "Justification"},
        {"name": "Wikipedia - Scientific method", "url": "https://en.wikipedia.org/wiki/Scientific_method", "priority": "high", "description": "Scientific method"},
        {"name": "Wikipedia - Empiricism", "url": "https://en.wikipedia.org/wiki/Empiricism", "priority": "high", "description": "Empiricism"},
        {"name": "Wikipedia - Rationalism", "url": "https://en.wikipedia.org/wiki/Rationalism", "priority": "high", "description": "Rationalism"},
        {"name": "Wikipedia - Skepticism", "url": "https://en.wikipedia.org/wiki/Philosophical_skepticism", "priority": "medium", "description": "Skepticism"},
    ],
    
    # TIER 41: EASTERN PHILOSOPHIES - Digital Library Texts
    41: [
        {"name": "Wikipedia - Buddhism", "url": "https://en.wikipedia.org/wiki/Buddhism", "priority": "high", "description": "Buddhism"},
        {"name": "Wikipedia - Hinduism", "url": "https://en.wikipedia.org/wiki/Hinduism", "priority": "high", "description": "Hinduism"},
        {"name": "Wikipedia - Taoism", "url": "https://en.wikipedia.org/wiki/Taoism", "priority": "high", "description": "Taoism"},
        {"name": "Wikipedia - Zen", "url": "https://en.wikipedia.org/wiki/Zen", "priority": "high", "description": "Zen Buddhism"},
        {"name": "Wikipedia - Meditation", "url": "https://en.wikipedia.org/wiki/Meditation", "priority": "high", "description": "Meditation"},
        {"name": "Wikipedia - Mindfulness", "url": "https://en.wikipedia.org/wiki/Mindfulness", "priority": "high", "description": "Mindfulness"},
        {"name": "Wikipedia - Yoga", "url": "https://en.wikipedia.org/wiki/Yoga", "priority": "high", "description": "Yoga philosophy"},
        {"name": "Wikipedia - Karma", "url": "https://en.wikipedia.org/wiki/Karma", "priority": "medium", "description": "Karma concept"},
        {"name": "Wikipedia - Enlightenment (spiritual)", "url": "https://en.wikipedia.org/wiki/Enlightenment_(spiritual)", "priority": "high", "description": "Enlightenment"},
        {"name": "Wikipedia - Nirvana", "url": "https://en.wikipedia.org/wiki/Nirvana", "priority": "medium", "description": "Nirvana"},
    ],
    
    # TIER 42: WESTERN PHILOSOPHY CLASSICS - Project Gutenberg
    42: [
        {"name": "Wikipedia - Plato", "url": "https://en.wikipedia.org/wiki/Plato", "priority": "high", "description": "Plato philosophy"},
        {"name": "Wikipedia - Aristotle", "url": "https://en.wikipedia.org/wiki/Aristotle", "priority": "high", "description": "Aristotle"},
        {"name": "Wikipedia - Socrates", "url": "https://en.wikipedia.org/wiki/Socrates", "priority": "high", "description": "Socrates"},
        {"name": "Wikipedia - Immanuel Kant", "url": "https://en.wikipedia.org/wiki/Immanuel_Kant", "priority": "high", "description": "Kant philosophy"},
        {"name": "Wikipedia - René Descartes", "url": "https://en.wikipedia.org/wiki/Ren%C3%A9_Descartes", "priority": "high", "description": "Descartes"},
        {"name": "Wikipedia - Friedrich Nietzsche", "url": "https://en.wikipedia.org/wiki/Friedrich_Nietzsche", "priority": "high", "description": "Nietzsche"},
        {"name": "Wikipedia - Phenomenology", "url": "https://en.wikipedia.org/wiki/Phenomenology_(philosophy)", "priority": "medium", "description": "Phenomenology"},
        {"name": "Wikipedia - Existentialism", "url": "https://en.wikipedia.org/wiki/Existentialism", "priority": "high", "description": "Existentialism"},
        {"name": "Wikipedia - Stoicism", "url": "https://en.wikipedia.org/wiki/Stoicism", "priority": "high", "description": "Stoicism"},
    ],
    
    # TIER 43: ETHICS & MORAL PHILOSOPHY - Academic Papers
    43: [
        {"name": "Wikipedia - Ethics", "url": "https://en.wikipedia.org/wiki/Ethics", "priority": "high", "description": "Ethics"},
        {"name": "Wikipedia - Virtue ethics", "url": "https://en.wikipedia.org/wiki/Virtue_ethics", "priority": "high", "description": "Virtue ethics"},
        {"name": "Wikipedia - Consequentialism", "url": "https://en.wikipedia.org/wiki/Consequentialism", "priority": "high", "description": "Consequentialism"},
        {"name": "Wikipedia - Deontology", "url": "https://en.wikipedia.org/wiki/Deontological_ethics", "priority": "high", "description": "Deontology"},
        {"name": "Wikipedia - Utilitarianism", "url": "https://en.wikipedia.org/wiki/Utilitarianism", "priority": "high", "description": "Utilitarianism"},
        {"name": "Wikipedia - Bioethics", "url": "https://en.wikipedia.org/wiki/Bioethics", "priority": "high", "description": "Bioethics"},
        {"name": "Wikipedia - Machine ethics", "url": "https://en.wikipedia.org/wiki/Machine_ethics", "priority": "high", "description": "AI ethics"},
        {"name": "Wikipedia - Moral psychology", "url": "https://en.wikipedia.org/wiki/Moral_psychology", "priority": "medium", "description": "Moral psychology"},
    ],
    
    # PHASE 3: ADVANCED BIOLOGY & NEUROSCIENCE
    
    # TIER 44: NEUROBIOLOGY & BRAIN OSCILLATIONS - PMC Papers
    44: [
        {"name": "Wikipedia - Neuroscience", "url": "https://en.wikipedia.org/wiki/Neuroscience", "priority": "high", "description": "Neuroscience"},
        {"name": "Wikipedia - Neural oscillation", "url": "https://en.wikipedia.org/wiki/Neural_oscillation", "priority": "high", "description": "Neural oscillations"},
        {"name": "Wikipedia - Electroencephalography", "url": "https://en.wikipedia.org/wiki/Electroencephalography", "priority": "high", "description": "EEG"},
        {"name": "Wikipedia - Alpha wave", "url": "https://en.wikipedia.org/wiki/Alpha_wave", "priority": "high", "description": "Alpha waves"},
        {"name": "Wikipedia - Beta wave", "url": "https://en.wikipedia.org/wiki/Beta_wave", "priority": "high", "description": "Beta waves"},
        {"name": "Wikipedia - Gamma wave", "url": "https://en.wikipedia.org/wiki/Gamma_wave", "priority": "high", "description": "Gamma waves"},
        {"name": "Wikipedia - Theta wave", "url": "https://en.wikipedia.org/wiki/Theta_wave", "priority": "high", "description": "Theta waves"},
        {"name": "Wikipedia - Delta wave", "url": "https://en.wikipedia.org/wiki/Delta_wave", "priority": "medium", "description": "Delta waves"},
        {"name": "Wikipedia - Cognitive neuroscience", "url": "https://en.wikipedia.org/wiki/Cognitive_neuroscience", "priority": "high", "description": "Cognitive neuroscience"},
        {"name": "Wikipedia - Neuroplasticity", "url": "https://en.wikipedia.org/wiki/Neuroplasticity", "priority": "high", "description": "Neuroplasticity"},
    ],
    
    # TIER 45: BIOPHYSICS & CELLULAR RESONANCE - Research Papers
    45: [
        {"name": "Wikipedia - Biophysics", "url": "https://en.wikipedia.org/wiki/Biophysics", "priority": "high", "description": "Biophysics"},
        {"name": "Wikipedia - Cell signaling", "url": "https://en.wikipedia.org/wiki/Cell_signaling", "priority": "high", "description": "Cell signaling"},
        {"name": "Wikipedia - Action potential", "url": "https://en.wikipedia.org/wiki/Action_potential", "priority": "high", "description": "Action potentials"},
        {"name": "Wikipedia - Membrane potential", "url": "https://en.wikipedia.org/wiki/Membrane_potential", "priority": "high", "description": "Membrane potential"},
        {"name": "Wikipedia - Ion channel", "url": "https://en.wikipedia.org/wiki/Ion_channel", "priority": "medium", "description": "Ion channels"},
        {"name": "Wikipedia - Bioelectricity", "url": "https://en.wikipedia.org/wiki/Bioelectricity", "priority": "high", "description": "Bioelectricity"},
        {"name": "Wikipedia - Molecular biology", "url": "https://en.wikipedia.org/wiki/Molecular_biology", "priority": "high", "description": "Molecular biology"},
    ],
    
    # TIER 46: SYSTEMS BIOLOGY & COMPLEXITY - Academic Sources
    46: [
        {"name": "Wikipedia - Systems biology", "url": "https://en.wikipedia.org/wiki/Systems_biology", "priority": "high", "description": "Systems biology"},
        {"name": "Wikipedia - Biological network", "url": "https://en.wikipedia.org/wiki/Biological_network", "priority": "high", "description": "Biological networks"},
        {"name": "Wikipedia - Emergence", "url": "https://en.wikipedia.org/wiki/Emergence", "priority": "high", "description": "Emergence"},
        {"name": "Wikipedia - Self-organization", "url": "https://en.wikipedia.org/wiki/Self-organization", "priority": "high", "description": "Self-organization"},
        {"name": "Wikipedia - Synthetic biology", "url": "https://en.wikipedia.org/wiki/Synthetic_biology", "priority": "high", "description": "Synthetic biology"},
        {"name": "Wikipedia - Metabolic network", "url": "https://en.wikipedia.org/wiki/Metabolic_network", "priority": "medium", "description": "Metabolic networks"},
    ],
    
    # TIER 47: GENETICS & MOLECULAR BIOLOGY - PMC Research
    47: [
        {"name": "Wikipedia - Genetics", "url": "https://en.wikipedia.org/wiki/Genetics", "priority": "high", "description": "Genetics"},
        {"name": "Wikipedia - DNA", "url": "https://en.wikipedia.org/wiki/DNA", "priority": "high", "description": "DNA structure"},
        {"name": "Wikipedia - CRISPR", "url": "https://en.wikipedia.org/wiki/CRISPR", "priority": "high", "description": "CRISPR gene editing"},
        {"name": "Wikipedia - Gene expression", "url": "https://en.wikipedia.org/wiki/Gene_expression", "priority": "high", "description": "Gene expression"},
        {"name": "Wikipedia - Epigenetics", "url": "https://en.wikipedia.org/wiki/Epigenetics", "priority": "high", "description": "Epigenetics"},
        {"name": "Wikipedia - Protein folding", "url": "https://en.wikipedia.org/wiki/Protein_folding", "priority": "high", "description": "Protein folding"},
        {"name": "Wikipedia - RNA", "url": "https://en.wikipedia.org/wiki/RNA", "priority": "high", "description": "RNA"},
        {"name": "Wikipedia - Genome", "url": "https://en.wikipedia.org/wiki/Genome", "priority": "high", "description": "Genomes"},
    ],
    
    # TIER 48: EVOLUTIONARY BIOLOGY & ECOLOGY - Research
    48: [
        {"name": "Wikipedia - Evolution", "url": "https://en.wikipedia.org/wiki/Evolution", "priority": "high", "description": "Evolution"},
        {"name": "Wikipedia - Natural selection", "url": "https://en.wikipedia.org/wiki/Natural_selection", "priority": "high", "description": "Natural selection"},
        {"name": "Wikipedia - Ecology", "url": "https://en.wikipedia.org/wiki/Ecology", "priority": "high", "description": "Ecology"},
        {"name": "Wikipedia - Ecosystem", "url": "https://en.wikipedia.org/wiki/Ecosystem", "priority": "high", "description": "Ecosystems"},
        {"name": "Wikipedia - Biodiversity", "url": "https://en.wikipedia.org/wiki/Biodiversity", "priority": "high", "description": "Biodiversity"},
        {"name": "Wikipedia - Evolutionary game theory", "url": "https://en.wikipedia.org/wiki/Evolutionary_game_theory", "priority": "medium", "description": "Evolutionary games"},
        {"name": "Wikipedia - Population genetics", "url": "https://en.wikipedia.org/wiki/Population_genetics", "priority": "medium", "description": "Population genetics"},
    ],
    
    # PART 1: WORLD LANGUAGES & LINGUISTICS
    
    # TIER 49: SPANISH LANGUAGE & DIALECTS
    49: [
        {"name": "Wikipedia - Spanish language", "url": "https://en.wikipedia.org/wiki/Spanish_language", "priority": "high", "description": "Spanish language"},
        {"name": "Wikipedia - Spanish grammar", "url": "https://en.wikipedia.org/wiki/Spanish_grammar", "priority": "high", "description": "Spanish grammar"},
        {"name": "Wikipedia - Spanish dialects", "url": "https://en.wikipedia.org/wiki/Spanish_dialects_and_varieties", "priority": "high", "description": "Spanish dialects"},
        {"name": "Wikipedia - Mexican Spanish", "url": "https://en.wikipedia.org/wiki/Mexican_Spanish", "priority": "medium", "description": "Mexican Spanish"},
        {"name": "Wikipedia - Peninsular Spanish", "url": "https://en.wikipedia.org/wiki/Peninsular_Spanish", "priority": "medium", "description": "Spain Spanish"},
        {"name": "Wikipedia - Spanish phonology", "url": "https://en.wikipedia.org/wiki/Spanish_phonology", "priority": "medium", "description": "Spanish pronunciation"},
    ],
    
    # TIER 50: CHINESE LANGUAGE & DIALECTS
    50: [
        {"name": "Wikipedia - Chinese language", "url": "https://en.wikipedia.org/wiki/Chinese_language", "priority": "high", "description": "Chinese language"},
        {"name": "Wikipedia - Mandarin Chinese", "url": "https://en.wikipedia.org/wiki/Mandarin_Chinese", "priority": "high", "description": "Mandarin"},
        {"name": "Wikipedia - Standard Chinese", "url": "https://en.wikipedia.org/wiki/Standard_Chinese", "priority": "high", "description": "Standard Chinese"},
        {"name": "Wikipedia - Chinese characters", "url": "https://en.wikipedia.org/wiki/Chinese_characters", "priority": "high", "description": "Chinese characters"},
        {"name": "Wikipedia - Cantonese", "url": "https://en.wikipedia.org/wiki/Cantonese", "priority": "medium", "description": "Cantonese"},
        {"name": "Wikipedia - Chinese grammar", "url": "https://en.wikipedia.org/wiki/Chinese_grammar", "priority": "high", "description": "Chinese grammar"},
    ],
    
    # TIER 51: FRENCH LANGUAGE & DIALECTS
    51: [
        {"name": "Wikipedia - French language", "url": "https://en.wikipedia.org/wiki/French_language", "priority": "high", "description": "French language"},
        {"name": "Wikipedia - French grammar", "url": "https://en.wikipedia.org/wiki/French_grammar", "priority": "high", "description": "French grammar"},
        {"name": "Wikipedia - French phonology", "url": "https://en.wikipedia.org/wiki/French_phonology", "priority": "medium", "description": "French pronunciation"},
        {"name": "Wikipedia - Quebec French", "url": "https://en.wikipedia.org/wiki/Quebec_French", "priority": "medium", "description": "Canadian French"},
        {"name": "Wikipedia - Verlan", "url": "https://en.wikipedia.org/wiki/Verlan", "priority": "medium", "description": "French slang"},
    ],
    
    # TIER 52: ARABIC LANGUAGE & DIALECTS
    52: [
        {"name": "Wikipedia - Arabic", "url": "https://en.wikipedia.org/wiki/Arabic", "priority": "high", "description": "Arabic language"},
        {"name": "Wikipedia - Modern Standard Arabic", "url": "https://en.wikipedia.org/wiki/Modern_Standard_Arabic", "priority": "high", "description": "MSA"},
        {"name": "Wikipedia - Arabic grammar", "url": "https://en.wikipedia.org/wiki/Arabic_grammar", "priority": "high", "description": "Arabic grammar"},
        {"name": "Wikipedia - Egyptian Arabic", "url": "https://en.wikipedia.org/wiki/Egyptian_Arabic", "priority": "medium", "description": "Egyptian dialect"},
        {"name": "Wikipedia - Levantine Arabic", "url": "https://en.wikipedia.org/wiki/Levantine_Arabic", "priority": "medium", "description": "Levantine dialect"},
    ],
    
    # TIER 53: JAPANESE LANGUAGE
    53: [
        {"name": "Wikipedia - Japanese language", "url": "https://en.wikipedia.org/wiki/Japanese_language", "priority": "high", "description": "Japanese"},
        {"name": "Wikipedia - Japanese grammar", "url": "https://en.wikipedia.org/wiki/Japanese_grammar", "priority": "high", "description": "Japanese grammar"},
        {"name": "Wikipedia - Hiragana", "url": "https://en.wikipedia.org/wiki/Hiragana", "priority": "high", "description": "Hiragana"},
        {"name": "Wikipedia - Katakana", "url": "https://en.wikipedia.org/wiki/Katakana", "priority": "high", "description": "Katakana"},
        {"name": "Wikipedia - Kanji", "url": "https://en.wikipedia.org/wiki/Kanji", "priority": "high", "description": "Kanji"},
        {"name": "Wikipedia - Honorific speech in Japanese", "url": "https://en.wikipedia.org/wiki/Honorific_speech_in_Japanese", "priority": "medium", "description": "Keigo"},
    ],
    
    # TIER 54: HINDI & INDIAN LANGUAGES
    54: [
        {"name": "Wikipedia - Hindi", "url": "https://en.wikipedia.org/wiki/Hindi", "priority": "high", "description": "Hindi language"},
        {"name": "Wikipedia - Devanagari", "url": "https://en.wikipedia.org/wiki/Devanagari", "priority": "high", "description": "Devanagari script"},
        {"name": "Wikipedia - Urdu", "url": "https://en.wikipedia.org/wiki/Urdu", "priority": "medium", "description": "Urdu"},
        {"name": "Wikipedia - Bengali language", "url": "https://en.wikipedia.org/wiki/Bengali_language", "priority": "medium", "description": "Bengali"},
        {"name": "Wikipedia - Punjabi language", "url": "https://en.wikipedia.org/wiki/Punjabi_language", "priority": "medium", "description": "Punjabi"},
    ],
    
    # TIER 55: GERMAN LANGUAGE & DIALECTS
    55: [
        {"name": "Wikipedia - German language", "url": "https://en.wikipedia.org/wiki/German_language", "priority": "high", "description": "German"},
        {"name": "Wikipedia - German grammar", "url": "https://en.wikipedia.org/wiki/German_grammar", "priority": "high", "description": "German grammar"},
        {"name": "Wikipedia - German dialects", "url": "https://en.wikipedia.org/wiki/German_dialects", "priority": "medium", "description": "German dialects"},
        {"name": "Wikipedia - Swiss German", "url": "https://en.wikipedia.org/wiki/Swiss_German", "priority": "medium", "description": "Swiss German"},
    ],
    
    # TIER 56: LINGUISTICS FUNDAMENTALS
    56: [
        {"name": "Wikipedia - Linguistics", "url": "https://en.wikipedia.org/wiki/Linguistics", "priority": "high", "description": "Linguistics"},
        {"name": "Wikipedia - Phonetics", "url": "https://en.wikipedia.org/wiki/Phonetics", "priority": "high", "description": "Phonetics"},
        {"name": "Wikipedia - Phonology", "url": "https://en.wikipedia.org/wiki/Phonology", "priority": "high", "description": "Phonology"},
        {"name": "Wikipedia - Morphology", "url": "https://en.wikipedia.org/wiki/Morphology_(linguistics)", "priority": "high", "description": "Morphology"},
        {"name": "Wikipedia - Syntax", "url": "https://en.wikipedia.org/wiki/Syntax", "priority": "high", "description": "Syntax"},
        {"name": "Wikipedia - Semantics", "url": "https://en.wikipedia.org/wiki/Semantics", "priority": "high", "description": "Semantics"},
        {"name": "Wikipedia - Pragmatics", "url": "https://en.wikipedia.org/wiki/Pragmatics", "priority": "medium", "description": "Pragmatics"},
        {"name": "Wikipedia - Sociolinguistics", "url": "https://en.wikipedia.org/wiki/Sociolinguistics", "priority": "medium", "description": "Sociolinguistics"},
    ],
    
    # PART 2: PROGRAMMING & TECHNOLOGY
    
    # TIER 57: PYTHON PROGRAMMING
    57: [
        {"name": "Wikipedia - Python (programming language)", "url": "https://en.wikipedia.org/wiki/Python_(programming_language)", "priority": "high", "description": "Python"},
        {"name": "Wikipedia - Python syntax and semantics", "url": "https://en.wikipedia.org/wiki/Python_syntax_and_semantics", "priority": "high", "description": "Python syntax"},
        {"name": "Wikipedia - Django (web framework)", "url": "https://en.wikipedia.org/wiki/Django_(web_framework)", "priority": "high", "description": "Django"},
        {"name": "Wikipedia - Flask (web framework)", "url": "https://en.wikipedia.org/wiki/Flask_(web_framework)", "priority": "high", "description": "Flask"},
        {"name": "Wikipedia - NumPy", "url": "https://en.wikipedia.org/wiki/NumPy", "priority": "high", "description": "NumPy"},
        {"name": "Wikipedia - Pandas (software)", "url": "https://en.wikipedia.org/wiki/Pandas_(software)", "priority": "high", "description": "Pandas"},
    ],
    
    # TIER 58: JAVASCRIPT & TYPESCRIPT
    58: [
        {"name": "Wikipedia - JavaScript", "url": "https://en.wikipedia.org/wiki/JavaScript", "priority": "high", "description": "JavaScript"},
        {"name": "Wikipedia - TypeScript", "url": "https://en.wikipedia.org/wiki/TypeScript", "priority": "high", "description": "TypeScript"},
        {"name": "Wikipedia - Node.js", "url": "https://en.wikipedia.org/wiki/Node.js", "priority": "high", "description": "Node.js"},
        {"name": "Wikipedia - React (JavaScript library)", "url": "https://en.wikipedia.org/wiki/React_(JavaScript_library)", "priority": "high", "description": "React"},
        {"name": "Wikipedia - Vue.js", "url": "https://en.wikipedia.org/wiki/Vue.js", "priority": "medium", "description": "Vue.js"},
        {"name": "Wikipedia - Angular (web framework)", "url": "https://en.wikipedia.org/wiki/Angular_(web_framework)", "priority": "medium", "description": "Angular"},
    ],
    
    # TIER 59: JAVA PROGRAMMING
    59: [
        {"name": "Wikipedia - Java (programming language)", "url": "https://en.wikipedia.org/wiki/Java_(programming_language)", "priority": "high", "description": "Java"},
        {"name": "Wikipedia - Java syntax", "url": "https://en.wikipedia.org/wiki/Java_syntax", "priority": "high", "description": "Java syntax"},
        {"name": "Wikipedia - Spring Framework", "url": "https://en.wikipedia.org/wiki/Spring_Framework", "priority": "high", "description": "Spring"},
        {"name": "Wikipedia - Java virtual machine", "url": "https://en.wikipedia.org/wiki/Java_virtual_machine", "priority": "medium", "description": "JVM"},
    ],
    
    # TIER 60: C/C++ PROGRAMMING
    60: [
        {"name": "Wikipedia - C (programming language)", "url": "https://en.wikipedia.org/wiki/C_(programming_language)", "priority": "high", "description": "C language"},
        {"name": "Wikipedia - C++", "url": "https://en.wikipedia.org/wiki/C%2B%2B", "priority": "high", "description": "C++"},
        {"name": "Wikipedia - C syntax", "url": "https://en.wikipedia.org/wiki/C_syntax", "priority": "high", "description": "C syntax"},
        {"name": "Wikipedia - Standard Template Library", "url": "https://en.wikipedia.org/wiki/Standard_Template_Library", "priority": "high", "description": "STL"},
        {"name": "Wikipedia - Pointer (computer programming)", "url": "https://en.wikipedia.org/wiki/Pointer_(computer_programming)", "priority": "medium", "description": "Pointers"},
    ],
    
    # TIER 61: RUST & GO PROGRAMMING
    61: [
        {"name": "Wikipedia - Rust (programming language)", "url": "https://en.wikipedia.org/wiki/Rust_(programming_language)", "priority": "high", "description": "Rust"},
        {"name": "Wikipedia - Go (programming language)", "url": "https://en.wikipedia.org/wiki/Go_(programming_language)", "priority": "high", "description": "Go"},
        {"name": "Wikipedia - Memory safety", "url": "https://en.wikipedia.org/wiki/Memory_safety", "priority": "medium", "description": "Memory safety"},
    ],
    
    # TIER 62: MORE PROGRAMMING LANGUAGES
    62: [
        {"name": "Wikipedia - C Sharp (programming language)", "url": "https://en.wikipedia.org/wiki/C_Sharp_(programming_language)", "priority": "high", "description": "C#"},
        {"name": "Wikipedia - Swift (programming language)", "url": "https://en.wikipedia.org/wiki/Swift_(programming_language)", "priority": "high", "description": "Swift"},
        {"name": "Wikipedia - Kotlin (programming language)", "url": "https://en.wikipedia.org/wiki/Kotlin_(programming_language)", "priority": "high", "description": "Kotlin"},
        {"name": "Wikipedia - Ruby (programming language)", "url": "https://en.wikipedia.org/wiki/Ruby_(programming_language)", "priority": "medium", "description": "Ruby"},
        {"name": "Wikipedia - PHP", "url": "https://en.wikipedia.org/wiki/PHP", "priority": "medium", "description": "PHP"},
    ],
    
    # TIER 63: SOFTWARE ARCHITECTURE & DESIGN PATTERNS
    63: [
        {"name": "Wikipedia - Software architecture", "url": "https://en.wikipedia.org/wiki/Software_architecture", "priority": "high", "description": "Architecture"},
        {"name": "Wikipedia - Software design pattern", "url": "https://en.wikipedia.org/wiki/Software_design_pattern", "priority": "high", "description": "Design patterns"},
        {"name": "Wikipedia - SOLID", "url": "https://en.wikipedia.org/wiki/SOLID", "priority": "high", "description": "SOLID principles"},
        {"name": "Wikipedia - Microservices", "url": "https://en.wikipedia.org/wiki/Microservices", "priority": "high", "description": "Microservices"},
        {"name": "Wikipedia - Domain-driven design", "url": "https://en.wikipedia.org/wiki/Domain-driven_design", "priority": "medium", "description": "DDD"},
        {"name": "Wikipedia - Model–view–controller", "url": "https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller", "priority": "medium", "description": "MVC"},
    ],
    
    # TIER 64: GAME DESIGN & DEVELOPMENT
    64: [
        {"name": "Wikipedia - Game design", "url": "https://en.wikipedia.org/wiki/Game_design", "priority": "high", "description": "Game design"},
        {"name": "Wikipedia - Video game development", "url": "https://en.wikipedia.org/wiki/Video_game_development", "priority": "high", "description": "Game development"},
        {"name": "Wikipedia - Unity (game engine)", "url": "https://en.wikipedia.org/wiki/Unity_(game_engine)", "priority": "high", "description": "Unity"},
        {"name": "Wikipedia - Unreal Engine", "url": "https://en.wikipedia.org/wiki/Unreal_Engine", "priority": "high", "description": "Unreal Engine"},
        {"name": "Wikipedia - Game mechanics", "url": "https://en.wikipedia.org/wiki/Game_mechanics", "priority": "high", "description": "Game mechanics"},
        {"name": "Wikipedia - Level design", "url": "https://en.wikipedia.org/wiki/Level_design", "priority": "medium", "description": "Level design"},
    ],
    
    # TIER 65: COMPUTER GRAPHICS & 3D
    65: [
        {"name": "Wikipedia - Computer graphics", "url": "https://en.wikipedia.org/wiki/Computer_graphics", "priority": "high", "description": "Computer graphics"},
        {"name": "Wikipedia - 3D computer graphics", "url": "https://en.wikipedia.org/wiki/3D_computer_graphics", "priority": "high", "description": "3D graphics"},
        {"name": "Wikipedia - Rendering (computer graphics)", "url": "https://en.wikipedia.org/wiki/Rendering_(computer_graphics)", "priority": "high", "description": "Rendering"},
        {"name": "Wikipedia - Ray tracing (graphics)", "url": "https://en.wikipedia.org/wiki/Ray_tracing_(graphics)", "priority": "high", "description": "Ray tracing"},
        {"name": "Wikipedia - Shader", "url": "https://en.wikipedia.org/wiki/Shader", "priority": "high", "description": "Shaders"},
        {"name": "Wikipedia - OpenGL", "url": "https://en.wikipedia.org/wiki/OpenGL", "priority": "medium", "description": "OpenGL"},
        {"name": "Wikipedia - Vulkan", "url": "https://en.wikipedia.org/wiki/Vulkan", "priority": "medium", "description": "Vulkan"},
    ],
    
    # TIER 66: CYBERSECURITY FUNDAMENTALS
    66: [
        {"name": "Wikipedia - Computer security", "url": "https://en.wikipedia.org/wiki/Computer_security", "priority": "high", "description": "Cybersecurity"},
        {"name": "Wikipedia - Information security", "url": "https://en.wikipedia.org/wiki/Information_security", "priority": "high", "description": "InfoSec"},
        {"name": "Wikipedia - Cryptography", "url": "https://en.wikipedia.org/wiki/Cryptography", "priority": "high", "description": "Cryptography"},
        {"name": "Wikipedia - Encryption", "url": "https://en.wikipedia.org/wiki/Encryption", "priority": "high", "description": "Encryption"},
        {"name": "Wikipedia - Public-key cryptography", "url": "https://en.wikipedia.org/wiki/Public-key_cryptography", "priority": "high", "description": "Public key crypto"},
        {"name": "Wikipedia - Symmetric-key algorithm", "url": "https://en.wikipedia.org/wiki/Symmetric-key_algorithm", "priority": "medium", "description": "Symmetric crypto"},
    ],
    
    # TIER 67: WEB & APPLICATION SECURITY
    67: [
        {"name": "Wikipedia - Web application security", "url": "https://en.wikipedia.org/wiki/Web_application_security", "priority": "high", "description": "Web security"},
        {"name": "Wikipedia - Cross-site scripting", "url": "https://en.wikipedia.org/wiki/Cross-site_scripting", "priority": "high", "description": "XSS"},
        {"name": "Wikipedia - SQL injection", "url": "https://en.wikipedia.org/wiki/SQL_injection", "priority": "high", "description": "SQL injection"},
        {"name": "Wikipedia - Cross-site request forgery", "url": "https://en.wikipedia.org/wiki/Cross-site_request_forgery", "priority": "high", "description": "CSRF"},
        {"name": "Wikipedia - Transport Layer Security", "url": "https://en.wikipedia.org/wiki/Transport_Layer_Security", "priority": "high", "description": "TLS/SSL"},
    ],
    
    # TIER 68: NETWORK SECURITY & PENETRATION TESTING
    68: [
        {"name": "Wikipedia - Network security", "url": "https://en.wikipedia.org/wiki/Network_security", "priority": "high", "description": "Network security"},
        {"name": "Wikipedia - Firewall (computing)", "url": "https://en.wikipedia.org/wiki/Firewall_(computing)", "priority": "high", "description": "Firewalls"},
        {"name": "Wikipedia - Penetration test", "url": "https://en.wikipedia.org/wiki/Penetration_test", "priority": "high", "description": "Pen testing"},
        {"name": "Wikipedia - Vulnerability (computing)", "url": "https://en.wikipedia.org/wiki/Vulnerability_(computing)", "priority": "high", "description": "Vulnerabilities"},
        {"name": "Wikipedia - Exploit (computer security)", "url": "https://en.wikipedia.org/wiki/Exploit_(computer_security)", "priority": "high", "description": "Exploits"},
        {"name": "Wikipedia - Reverse engineering", "url": "https://en.wikipedia.org/wiki/Reverse_engineering", "priority": "medium", "description": "Reverse engineering"},
    ],
    
    # PHASE 1: MORE WORLD LANGUAGES (Tiers 69-88)
    
    # TIER 69: PORTUGUESE LANGUAGE
    69: [
        {"name": "Wikipedia - Portuguese language", "url": "https://en.wikipedia.org/wiki/Portuguese_language", "priority": "high", "description": "Portuguese"},
        {"name": "Wikipedia - Portuguese grammar", "url": "https://en.wikipedia.org/wiki/Portuguese_grammar", "priority": "high", "description": "Portuguese grammar"},
        {"name": "Wikipedia - Brazilian Portuguese", "url": "https://en.wikipedia.org/wiki/Brazilian_Portuguese", "priority": "medium", "description": "Brazilian Portuguese"},
        {"name": "Wikipedia - European Portuguese", "url": "https://en.wikipedia.org/wiki/European_Portuguese", "priority": "medium", "description": "European Portuguese"},
    ],
    
    # TIER 70: RUSSIAN LANGUAGE
    70: [
        {"name": "Wikipedia - Russian language", "url": "https://en.wikipedia.org/wiki/Russian_language", "priority": "high", "description": "Russian"},
        {"name": "Wikipedia - Russian grammar", "url": "https://en.wikipedia.org/wiki/Russian_grammar", "priority": "high", "description": "Russian grammar"},
        {"name": "Wikipedia - Russian alphabet", "url": "https://en.wikipedia.org/wiki/Russian_alphabet", "priority": "high", "description": "Cyrillic alphabet"},
        {"name": "Wikipedia - Russian phonology", "url": "https://en.wikipedia.org/wiki/Russian_phonology", "priority": "medium", "description": "Russian pronunciation"},
    ],
    
    # TIER 71: KOREAN LANGUAGE
    71: [
        {"name": "Wikipedia - Korean language", "url": "https://en.wikipedia.org/wiki/Korean_language", "priority": "high", "description": "Korean"},
        {"name": "Wikipedia - Korean grammar", "url": "https://en.wikipedia.org/wiki/Korean_grammar", "priority": "high", "description": "Korean grammar"},
        {"name": "Wikipedia - Hangul", "url": "https://en.wikipedia.org/wiki/Hangul", "priority": "high", "description": "Hangul alphabet"},
        {"name": "Wikipedia - Korean honorifics", "url": "https://en.wikipedia.org/wiki/Korean_honorifics", "priority": "medium", "description": "Korean honorifics"},
    ],
    
    # TIER 72: ITALIAN LANGUAGE
    72: [
        {"name": "Wikipedia - Italian language", "url": "https://en.wikipedia.org/wiki/Italian_language", "priority": "high", "description": "Italian"},
        {"name": "Wikipedia - Italian grammar", "url": "https://en.wikipedia.org/wiki/Italian_grammar", "priority": "high", "description": "Italian grammar"},
        {"name": "Wikipedia - Italian phonology", "url": "https://en.wikipedia.org/wiki/Italian_phonology", "priority": "medium", "description": "Italian pronunciation"},
    ],
    
    # TIER 73: TURKISH LANGUAGE
    73: [
        {"name": "Wikipedia - Turkish language", "url": "https://en.wikipedia.org/wiki/Turkish_language", "priority": "high", "description": "Turkish"},
        {"name": "Wikipedia - Turkish grammar", "url": "https://en.wikipedia.org/wiki/Turkish_grammar", "priority": "high", "description": "Turkish grammar"},
    ],
    
    # TIER 74: VIETNAMESE LANGUAGE
    74: [
        {"name": "Wikipedia - Vietnamese language", "url": "https://en.wikipedia.org/wiki/Vietnamese_language", "priority": "high", "description": "Vietnamese"},
        {"name": "Wikipedia - Vietnamese grammar", "url": "https://en.wikipedia.org/wiki/Vietnamese_grammar", "priority": "high", "description": "Vietnamese grammar"},
        {"name": "Wikipedia - Vietnamese phonology", "url": "https://en.wikipedia.org/wiki/Vietnamese_phonology", "priority": "medium", "description": "Vietnamese tones"},
    ],
    
    # TIER 75: THAI LANGUAGE
    75: [
        {"name": "Wikipedia - Thai language", "url": "https://en.wikipedia.org/wiki/Thai_language", "priority": "high", "description": "Thai"},
        {"name": "Wikipedia - Thai script", "url": "https://en.wikipedia.org/wiki/Thai_script", "priority": "high", "description": "Thai alphabet"},
        {"name": "Wikipedia - Thai grammar", "url": "https://en.wikipedia.org/wiki/Thai_grammar", "priority": "medium", "description": "Thai grammar"},
    ],
    
    # TIER 76: INDONESIAN/MALAY
    76: [
        {"name": "Wikipedia - Indonesian language", "url": "https://en.wikipedia.org/wiki/Indonesian_language", "priority": "high", "description": "Indonesian"},
        {"name": "Wikipedia - Malay language", "url": "https://en.wikipedia.org/wiki/Malay_language", "priority": "high", "description": "Malay"},
    ],
    
    # TIER 77: HEBREW LANGUAGE
    77: [
        {"name": "Wikipedia - Hebrew language", "url": "https://en.wikipedia.org/wiki/Hebrew_language", "priority": "high", "description": "Hebrew"},
        {"name": "Wikipedia - Hebrew alphabet", "url": "https://en.wikipedia.org/wiki/Hebrew_alphabet", "priority": "high", "description": "Hebrew alphabet"},
        {"name": "Wikipedia - Modern Hebrew", "url": "https://en.wikipedia.org/wiki/Modern_Hebrew", "priority": "medium", "description": "Modern Hebrew"},
    ],
    
    # TIER 78: PERSIAN (FARSI)
    78: [
        {"name": "Wikipedia - Persian language", "url": "https://en.wikipedia.org/wiki/Persian_language", "priority": "high", "description": "Persian/Farsi"},
        {"name": "Wikipedia - Persian grammar", "url": "https://en.wikipedia.org/wiki/Persian_grammar", "priority": "high", "description": "Persian grammar"},
    ],
    
    # TIER 79: SWAHILI & AFRICAN LANGUAGES
    79: [
        {"name": "Wikipedia - Swahili language", "url": "https://en.wikipedia.org/wiki/Swahili_language", "priority": "high", "description": "Swahili"},
        {"name": "Wikipedia - Zulu language", "url": "https://en.wikipedia.org/wiki/Zulu_language", "priority": "medium", "description": "Zulu"},
        {"name": "Wikipedia - Amharic", "url": "https://en.wikipedia.org/wiki/Amharic", "priority": "medium", "description": "Amharic"},
    ],
    
    # TIER 80: GREEK LANGUAGE
    80: [
        {"name": "Wikipedia - Greek language", "url": "https://en.wikipedia.org/wiki/Greek_language", "priority": "high", "description": "Greek"},
        {"name": "Wikipedia - Modern Greek", "url": "https://en.wikipedia.org/wiki/Modern_Greek", "priority": "high", "description": "Modern Greek"},
        {"name": "Wikipedia - Ancient Greek", "url": "https://en.wikipedia.org/wiki/Ancient_Greek", "priority": "medium", "description": "Ancient Greek"},
    ],
    
    # TIER 81: DUTCH & SCANDINAVIAN
    81: [
        {"name": "Wikipedia - Dutch language", "url": "https://en.wikipedia.org/wiki/Dutch_language", "priority": "high", "description": "Dutch"},
        {"name": "Wikipedia - Swedish language", "url": "https://en.wikipedia.org/wiki/Swedish_language", "priority": "medium", "description": "Swedish"},
        {"name": "Wikipedia - Norwegian language", "url": "https://en.wikipedia.org/wiki/Norwegian_language", "priority": "medium", "description": "Norwegian"},
        {"name": "Wikipedia - Danish language", "url": "https://en.wikipedia.org/wiki/Danish_language", "priority": "medium", "description": "Danish"},
    ],
    
    # TIER 82: POLISH & SLAVIC LANGUAGES
    82: [
        {"name": "Wikipedia - Polish language", "url": "https://en.wikipedia.org/wiki/Polish_language", "priority": "high", "description": "Polish"},
        {"name": "Wikipedia - Czech language", "url": "https://en.wikipedia.org/wiki/Czech_language", "priority": "medium", "description": "Czech"},
        {"name": "Wikipedia - Ukrainian language", "url": "https://en.wikipedia.org/wiki/Ukrainian_language", "priority": "medium", "description": "Ukrainian"},
    ],
    
    # TIER 83: LATIN & CLASSICAL LANGUAGES
    83: [
        {"name": "Wikipedia - Latin", "url": "https://en.wikipedia.org/wiki/Latin", "priority": "high", "description": "Latin language"},
        {"name": "Wikipedia - Latin grammar", "url": "https://en.wikipedia.org/wiki/Latin_grammar", "priority": "high", "description": "Latin grammar"},
        {"name": "Wikipedia - Sanskrit", "url": "https://en.wikipedia.org/wiki/Sanskrit", "priority": "medium", "description": "Sanskrit"},
    ],
    
    # TIER 84: LANGUAGE FAMILIES
    84: [
        {"name": "Wikipedia - Language family", "url": "https://en.wikipedia.org/wiki/Language_family", "priority": "high", "description": "Language families"},
        {"name": "Wikipedia - Indo-European languages", "url": "https://en.wikipedia.org/wiki/Indo-European_languages", "priority": "high", "description": "Indo-European"},
        {"name": "Wikipedia - Sino-Tibetan languages", "url": "https://en.wikipedia.org/wiki/Sino-Tibetan_languages", "priority": "medium", "description": "Sino-Tibetan"},
        {"name": "Wikipedia - Afroasiatic languages", "url": "https://en.wikipedia.org/wiki/Afroasiatic_languages", "priority": "medium", "description": "Afroasiatic"},
    ],
    
    # TIER 85: SIGN LANGUAGES
    85: [
        {"name": "Wikipedia - Sign language", "url": "https://en.wikipedia.org/wiki/Sign_language", "priority": "high", "description": "Sign language"},
        {"name": "Wikipedia - American Sign Language", "url": "https://en.wikipedia.org/wiki/American_Sign_Language", "priority": "high", "description": "ASL"},
        {"name": "Wikipedia - British Sign Language", "url": "https://en.wikipedia.org/wiki/British_Sign_Language", "priority": "medium", "description": "BSL"},
    ],
    
    # TIER 86: CONSTRUCTED LANGUAGES
    86: [
        {"name": "Wikipedia - Constructed language", "url": "https://en.wikipedia.org/wiki/Constructed_language", "priority": "high", "description": "Conlangs"},
        {"name": "Wikipedia - Esperanto", "url": "https://en.wikipedia.org/wiki/Esperanto", "priority": "high", "description": "Esperanto"},
        {"name": "Wikipedia - Klingon language", "url": "https://en.wikipedia.org/wiki/Klingon_language", "priority": "medium", "description": "Klingon"},
    ],
    
    # TIER 87: HISTORICAL LINGUISTICS
    87: [
        {"name": "Wikipedia - Historical linguistics", "url": "https://en.wikipedia.org/wiki/Historical_linguistics", "priority": "high", "description": "Historical linguistics"},
        {"name": "Wikipedia - Etymology", "url": "https://en.wikipedia.org/wiki/Etymology", "priority": "high", "description": "Etymology"},
        {"name": "Wikipedia - Comparative linguistics", "url": "https://en.wikipedia.org/wiki/Comparative_linguistics", "priority": "medium", "description": "Comparative linguistics"},
    ],
    
    # TIER 88: COMPUTATIONAL LINGUISTICS
    88: [
        {"name": "Wikipedia - Computational linguistics", "url": "https://en.wikipedia.org/wiki/Computational_linguistics", "priority": "high", "description": "Computational linguistics"},
        {"name": "Wikipedia - Natural language processing", "url": "https://en.wikipedia.org/wiki/Natural_language_processing", "priority": "high", "description": "NLP"},
        {"name": "Wikipedia - Machine translation", "url": "https://en.wikipedia.org/wiki/Machine_translation", "priority": "high", "description": "Machine translation"},
        {"name": "Wikipedia - Speech recognition", "url": "https://en.wikipedia.org/wiki/Speech_recognition", "priority": "medium", "description": "Speech recognition"},
    ],
    
    # PHASE 2: ADVANCED MATHEMATICS (Tiers 89-108)
    
    # TIER 89: CALCULUS FUNDAMENTALS
    89: [
        {"name": "Wikipedia - Calculus", "url": "https://en.wikipedia.org/wiki/Calculus", "priority": "high", "description": "Calculus"},
        {"name": "Wikipedia - Derivative", "url": "https://en.wikipedia.org/wiki/Derivative", "priority": "high", "description": "Derivatives"},
        {"name": "Wikipedia - Integral", "url": "https://en.wikipedia.org/wiki/Integral", "priority": "high", "description": "Integrals"},
        {"name": "Wikipedia - Limit (mathematics)", "url": "https://en.wikipedia.org/wiki/Limit_(mathematics)", "priority": "high", "description": "Limits"},
    ],
    
    # TIER 90: MULTIVARIABLE CALCULUS
    90: [
        {"name": "Wikipedia - Multivariable calculus", "url": "https://en.wikipedia.org/wiki/Multivariable_calculus", "priority": "high", "description": "Multivariable calculus"},
        {"name": "Wikipedia - Partial derivative", "url": "https://en.wikipedia.org/wiki/Partial_derivative", "priority": "high", "description": "Partial derivatives"},
        {"name": "Wikipedia - Multiple integral", "url": "https://en.wikipedia.org/wiki/Multiple_integral", "priority": "high", "description": "Multiple integrals"},
        {"name": "Wikipedia - Vector calculus", "url": "https://en.wikipedia.org/wiki/Vector_calculus", "priority": "high", "description": "Vector calculus"},
    ],
    
    # TIER 91: LINEAR ALGEBRA
    91: [
        {"name": "Wikipedia - Linear algebra", "url": "https://en.wikipedia.org/wiki/Linear_algebra", "priority": "high", "description": "Linear algebra"},
        {"name": "Wikipedia - Matrix (mathematics)", "url": "https://en.wikipedia.org/wiki/Matrix_(mathematics)", "priority": "high", "description": "Matrices"},
        {"name": "Wikipedia - Vector space", "url": "https://en.wikipedia.org/wiki/Vector_space", "priority": "high", "description": "Vector spaces"},
        {"name": "Wikipedia - Eigenvalues and eigenvectors", "url": "https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors", "priority": "high", "description": "Eigenvalues"},
    ],
    
    # TIER 92: DIFFERENTIAL EQUATIONS
    92: [
        {"name": "Wikipedia - Differential equation", "url": "https://en.wikipedia.org/wiki/Differential_equation", "priority": "high", "description": "Differential equations"},
        {"name": "Wikipedia - Ordinary differential equation", "url": "https://en.wikipedia.org/wiki/Ordinary_differential_equation", "priority": "high", "description": "ODEs"},
        {"name": "Wikipedia - Partial differential equation", "url": "https://en.wikipedia.org/wiki/Partial_differential_equation", "priority": "high", "description": "PDEs"},
    ],
    
    # TIER 93: ABSTRACT ALGEBRA
    93: [
        {"name": "Wikipedia - Abstract algebra", "url": "https://en.wikipedia.org/wiki/Abstract_algebra", "priority": "high", "description": "Abstract algebra"},
        {"name": "Wikipedia - Group theory", "url": "https://en.wikipedia.org/wiki/Group_theory", "priority": "high", "description": "Group theory"},
        {"name": "Wikipedia - Ring theory", "url": "https://en.wikipedia.org/wiki/Ring_theory", "priority": "medium", "description": "Ring theory"},
        {"name": "Wikipedia - Field (mathematics)", "url": "https://en.wikipedia.org/wiki/Field_(mathematics)", "priority": "medium", "description": "Field theory"},
    ],
    
    # TIER 94: REAL ANALYSIS
    94: [
        {"name": "Wikipedia - Real analysis", "url": "https://en.wikipedia.org/wiki/Real_analysis", "priority": "high", "description": "Real analysis"},
        {"name": "Wikipedia - Metric space", "url": "https://en.wikipedia.org/wiki/Metric_space", "priority": "high", "description": "Metric spaces"},
        {"name": "Wikipedia - Sequence", "url": "https://en.wikipedia.org/wiki/Sequence", "priority": "medium", "description": "Sequences"},
        {"name": "Wikipedia - Series (mathematics)", "url": "https://en.wikipedia.org/wiki/Series_(mathematics)", "priority": "medium", "description": "Series"},
    ],
    
    # TIER 95: COMPLEX ANALYSIS
    95: [
        {"name": "Wikipedia - Complex analysis", "url": "https://en.wikipedia.org/wiki/Complex_analysis", "priority": "high", "description": "Complex analysis"},
        {"name": "Wikipedia - Complex number", "url": "https://en.wikipedia.org/wiki/Complex_number", "priority": "high", "description": "Complex numbers"},
        {"name": "Wikipedia - Analytic function", "url": "https://en.wikipedia.org/wiki/Analytic_function", "priority": "medium", "description": "Analytic functions"},
    ],
    
    # TIER 96: TOPOLOGY
    96: [
        {"name": "Wikipedia - Topology", "url": "https://en.wikipedia.org/wiki/Topology", "priority": "high", "description": "Topology"},
        {"name": "Wikipedia - Topological space", "url": "https://en.wikipedia.org/wiki/Topological_space", "priority": "high", "description": "Topological spaces"},
        {"name": "Wikipedia - Algebraic topology", "url": "https://en.wikipedia.org/wiki/Algebraic_topology", "priority": "medium", "description": "Algebraic topology"},
    ],
    
    # TIER 97: DIFFERENTIAL GEOMETRY
    97: [
        {"name": "Wikipedia - Differential geometry", "url": "https://en.wikipedia.org/wiki/Differential_geometry", "priority": "high", "description": "Differential geometry"},
        {"name": "Wikipedia - Manifold", "url": "https://en.wikipedia.org/wiki/Manifold", "priority": "high", "description": "Manifolds"},
        {"name": "Wikipedia - Riemannian geometry", "url": "https://en.wikipedia.org/wiki/Riemannian_geometry", "priority": "medium", "description": "Riemannian geometry"},
    ],
    
    # TIER 98: NUMBER THEORY
    98: [
        {"name": "Wikipedia - Number theory", "url": "https://en.wikipedia.org/wiki/Number_theory", "priority": "high", "description": "Number theory"},
        {"name": "Wikipedia - Prime number", "url": "https://en.wikipedia.org/wiki/Prime_number", "priority": "high", "description": "Prime numbers"},
        {"name": "Wikipedia - Modular arithmetic", "url": "https://en.wikipedia.org/wiki/Modular_arithmetic", "priority": "medium", "description": "Modular arithmetic"},
    ],
    
    # TIER 99: COMBINATORICS
    99: [
        {"name": "Wikipedia - Combinatorics", "url": "https://en.wikipedia.org/wiki/Combinatorics", "priority": "high", "description": "Combinatorics"},
        {"name": "Wikipedia - Graph theory", "url": "https://en.wikipedia.org/wiki/Graph_theory", "priority": "high", "description": "Graph theory"},
        {"name": "Wikipedia - Permutation", "url": "https://en.wikipedia.org/wiki/Permutation", "priority": "medium", "description": "Permutations"},
    ],
    
    # TIER 100: PROBABILITY THEORY
    100: [
        {"name": "Wikipedia - Probability theory", "url": "https://en.wikipedia.org/wiki/Probability_theory", "priority": "high", "description": "Probability"},
        {"name": "Wikipedia - Random variable", "url": "https://en.wikipedia.org/wiki/Random_variable", "priority": "high", "description": "Random variables"},
        {"name": "Wikipedia - Probability distribution", "url": "https://en.wikipedia.org/wiki/Probability_distribution", "priority": "high", "description": "Distributions"},
    ]
}


class IngestionManager:
    """
    Manages the autonomous knowledge ingestion process with prioritization
    """
    
    def __init__(
        self,
        db_path: str = "mc_ai.db",
        max_workers: int = 3,
        delay_between_requests: float = 2.0
    ):
        """
        Initialize the ingestion manager.
        
        Args:
            db_path: Path to knowledge index database
            max_workers: Number of concurrent worker threads
            delay_between_requests: Delay between requests (rate limiting)
        """
        self.indexer = KnowledgeIndexer(db_path)
        self.encoder = FrequencyEncoder()
        self.max_workers = max_workers
        self.delay = delay_between_requests
        
        self.url_queue = queue.Queue()
        self.workers = []
        self.running = False
        self.stats = {
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': None
        }
        
        logger.info(f"IngestionManager initialized with {max_workers} workers")
    
    def ingest_source(self, source: Dict) -> bool:
        """
        Ingest a single knowledge source.
        
        Args:
            source: Source dictionary with url, name, priority, description
            
        Returns:
            True if successfully ingested, False otherwise
        """
        url = source.get('url')
        name = source.get('name', 'Unknown')
        
        if not url:
            logger.warning(f"Source {name} has no URL")
            return False
        
        # Check if already indexed
        if self.indexer.is_indexed(url):
            logger.info(f"Source already indexed, skipping: {name}")
            self.stats['skipped'] += 1
            return True
        
        # Check available storage
        if not self._check_storage():
            logger.warning("Low storage space, pausing ingestion")
            return False
        
        logger.info(f"Ingesting: {name} ({url})")
        
        # Fetch content
        text_content = fetch_and_extract_text(url)
        
        if not text_content:
            logger.warning(f"Failed to fetch content from: {name}")
            self.stats['failed'] += 1
            return False
        
        # Generate frequency signature
        signature = self.encoder.encode_text(text_content)
        
        if not signature:
            logger.warning(f"Failed to generate signature for: {name}")
            self.stats['failed'] += 1
            return False
        
        # Add metadata
        signature['source_name'] = name
        signature['source_description'] = source.get('description', '')
        signature['priority'] = source.get('priority', 'medium')
        
        # Index the source
        success = self.indexer.add_to_index(url, signature)
        
        if success:
            logger.info(
                f"Successfully indexed: {name} "
                f"({signature['primary_frequency']:.1f}Hz, "
                f"{signature['text_features']['word_count']} words)"
            )
            self.stats['successful'] += 1
        else:
            self.stats['failed'] += 1
        
        self.stats['processed'] += 1
        
        # Rate limiting
        time.sleep(self.delay)
        
        return success
    
    def ingest_tier(self, tier: int, max_sources: Optional[int] = None) -> Dict:
        """
        Ingest all sources from a specific priority tier.
        
        Args:
            tier: Tier number (1, 2, 3, etc.)
            max_sources: Maximum number of sources to ingest from this tier
            
        Returns:
            Statistics dictionary
        """
        if tier not in PRIORITIZED_SOURCES:
            logger.warning(f"Tier {tier} not found in PRIORITIZED_SOURCES")
            return {}
        
        sources = PRIORITIZED_SOURCES[tier]
        
        if max_sources:
            sources = sources[:max_sources]
        
        logger.info(f"Starting ingestion of Tier {tier} ({len(sources)} sources)")
        self.stats['start_time'] = datetime.now()
        
        for source in sources:
            self.ingest_source(source)
        
        return self.get_stats()
    
    def ingest_all_tiers(
        self,
        max_per_tier: Optional[Dict[int, int]] = None
    ) -> Dict:
        """
        Ingest sources from all tiers sequentially.
        
        Args:
            max_per_tier: Dictionary mapping tier number to max sources
                         e.g., {1: 10, 2: 5, 3: 3}
        
        Returns:
            Final statistics dictionary
        """
        logger.info("Starting full knowledge ingestion process")
        self.stats['start_time'] = datetime.now()
        
        for tier in sorted(PRIORITIZED_SOURCES.keys()):
            max_sources = max_per_tier.get(tier) if max_per_tier else None
            
            logger.info(f"\n{'='*60}")
            logger.info(f"TIER {tier} INGESTION")
            logger.info(f"{'='*60}\n")
            
            self.ingest_tier(tier, max_sources)
            
            # Check storage between tiers
            if not self._check_storage():
                logger.warning("Storage low, stopping ingestion")
                break
        
        final_stats = self.get_stats()
        logger.info(f"\nIngestion complete: {final_stats}")
        
        return final_stats
    
    def _check_storage(self, min_free_gb: float = 10.0) -> bool:
        """
        Check if sufficient storage is available.
        
        Args:
            min_free_gb: Minimum free GB required
            
        Returns:
            True if sufficient storage, False otherwise
        """
        try:
            import shutil
            stat = shutil.disk_usage('.')
            free_gb = stat.free / (1024**3)
            
            if free_gb < min_free_gb:
                logger.warning(
                    f"Low storage: {free_gb:.2f}GB free "
                    f"(minimum: {min_free_gb}GB)"
                )
                return False
            
            return True
        
        except Exception as e:
            logger.error(f"Error checking storage: {e}")
            return True  # Assume OK if can't check
    
    def get_stats(self) -> Dict:
        """Get ingestion statistics"""
        stats = self.stats.copy()
        
        if stats['start_time']:
            elapsed = (datetime.now() - stats['start_time']).total_seconds()
            stats['elapsed_seconds'] = elapsed
            stats['sources_per_minute'] = (
                (stats['processed'] / elapsed) * 60 if elapsed > 0 else 0
            )
        
        # Add index stats
        index_stats = self.indexer.get_stats()
        stats['total_in_index'] = index_stats.get('total_sources', 0)
        stats['total_words'] = index_stats.get('total_words', 0)
        
        return stats
    
    def add_custom_source(self, url: str, name: str, description: str = "", priority: str = "medium") -> bool:
        """
        Add and ingest a custom knowledge source.
        
        Args:
            url: Source URL
            name: Source name
            description: Optional description
            priority: Priority level (high, medium, low)
            
        Returns:
            True if successfully ingested
        """
        source = {
            'url': url,
            'name': name,
            'description': description,
            'priority': priority
        }
        
        return self.ingest_source(source)
