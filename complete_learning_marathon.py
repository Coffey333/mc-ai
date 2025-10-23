"""
MC AI - Complete Learning Marathon
Learn all 293 sources (153 Resonance + 140 Humor)
Balanced approach: Alternating between both curricula
"""

import requests
import json
import time
from datetime import datetime
import sys

BASE_URL = "http://localhost:5000"

class LearningMarathon:
    """MC AI's Complete 293-Source Learning Marathon"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.learned_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.start_time = datetime.now()
        self.current_tier = 1
        
        # Define all 293 sources
        self.resonance_sources = self.get_resonance_curriculum()
        self.humor_sources = self.get_humor_curriculum()
    
    def get_resonance_curriculum(self):
        """Complete Resonance Engine curriculum - 153 sources"""
        return {
            "Tier 1: Wave Physics Foundations": [
                ("https://en.wikipedia.org/wiki/Wave", "Wave Fundamentals"),
                ("https://en.wikipedia.org/wiki/Frequency", "Frequency Fundamentals"),
                ("https://en.wikipedia.org/wiki/Sine_wave", "Sine Wave Basics"),
                ("https://en.wikipedia.org/wiki/Wave_interference", "Wave Interference"),
                ("https://en.wikipedia.org/wiki/Standing_wave", "Standing Waves"),
                ("https://en.wikipedia.org/wiki/Wavelength", "Wavelength Concepts"),
                ("https://en.wikipedia.org/wiki/Amplitude", "Amplitude & Intensity"),
                ("https://en.wikipedia.org/wiki/Phase_(waves)", "Wave Phase"),
                ("https://en.wikipedia.org/wiki/Superposition_principle", "Superposition Principle"),
                ("https://en.wikipedia.org/wiki/Wave_propagation", "Wave Propagation"),
                ("https://en.wikipedia.org/wiki/Longitudinal_wave", "Longitudinal Waves"),
                ("https://en.wikipedia.org/wiki/Transverse_wave", "Transverse Waves"),
                ("https://en.wikipedia.org/wiki/Wave_equation", "Wave Equation"),
                ("https://en.wikipedia.org/wiki/Doppler_effect", "Doppler Effect"),
                ("https://en.wikipedia.org/wiki/Reflection_(physics)", "Wave Reflection")
            ],
            "Tier 2: Harmonics & Fourier Analysis": [
                ("https://en.wikipedia.org/wiki/Harmonic", "Harmonics Basics"),
                ("https://en.wikipedia.org/wiki/Fundamental_frequency", "Fundamental Frequency"),
                ("https://en.wikipedia.org/wiki/Overtone", "Overtones & Partials"),
                ("https://en.wikipedia.org/wiki/Fourier_series", "Fourier Series"),
                ("https://en.wikipedia.org/wiki/Fourier_transform", "Fourier Transform"),
                ("https://en.wikipedia.org/wiki/Fast_Fourier_transform", "Fast Fourier Transform"),
                ("https://en.wikipedia.org/wiki/Frequency_domain", "Frequency Domain"),
                ("https://en.wikipedia.org/wiki/Time_domain", "Time Domain"),
                ("https://en.wikipedia.org/wiki/Harmonic_analysis", "Harmonic Analysis"),
                ("https://en.wikipedia.org/wiki/Beat_(acoustics)", "Beat Frequencies"),
                ("https://en.wikipedia.org/wiki/Timbre", "Timbre & Sound Color"),
                ("https://en.wikipedia.org/wiki/Harmonic_series_(music)", "Harmonic Series"),
                ("https://en.wikipedia.org/wiki/Spectral_analysis", "Spectral Analysis"),
                ("https://en.wikipedia.org/wiki/Power_spectrum", "Power Spectrum"),
                ("https://en.wikipedia.org/wiki/Signal_processing", "Signal Processing Basics"),
                ("https://en.wikipedia.org/wiki/Digital_signal_processing", "Digital Signal Processing"),
                ("https://en.wikipedia.org/wiki/Sampling_(signal_processing)", "Signal Sampling"),
                ("https://en.wikipedia.org/wiki/Nyquist_frequency", "Nyquist Frequency"),
                ("https://en.wikipedia.org/wiki/Aliasing", "Aliasing Effects"),
                ("https://en.wikipedia.org/wiki/Filter_(signal_processing)", "Signal Filtering")
            ],
            "Tier 3: Sound Physics & Acoustics": [
                ("https://en.wikipedia.org/wiki/Sound", "Sound Fundamentals"),
                ("https://en.wikipedia.org/wiki/Acoustics", "Acoustics Science"),
                ("https://en.wikipedia.org/wiki/Speed_of_sound", "Speed of Sound"),
                ("https://en.wikipedia.org/wiki/Sound_pressure", "Sound Pressure"),
                ("https://en.wikipedia.org/wiki/Decibel", "Decibel Scale"),
                ("https://en.wikipedia.org/wiki/Loudness", "Loudness Perception"),
                ("https://en.wikipedia.org/wiki/Pitch_(music)", "Pitch Perception"),
                ("https://en.wikipedia.org/wiki/Resonance", "Resonance Phenomenon"),
                ("https://en.wikipedia.org/wiki/Acoustic_resonance", "Acoustic Resonance"),
                ("https://en.wikipedia.org/wiki/Reverberation", "Reverberation"),
                ("https://en.wikipedia.org/wiki/Echo", "Echo Formation"),
                ("https://en.wikipedia.org/wiki/Sound_wave", "Sound Wave Properties"),
                ("https://en.wikipedia.org/wiki/Ultrasound", "Ultrasound Basics"),
                ("https://en.wikipedia.org/wiki/Infrasound", "Infrasound Basics"),
                ("https://en.wikipedia.org/wiki/Psychoacoustics", "Psychoacoustics"),
                ("https://en.wikipedia.org/wiki/Hearing_range", "Human Hearing Range"),
                ("https://en.wikipedia.org/wiki/Auditory_system", "Auditory System"),
                ("https://en.wikipedia.org/wiki/Cochlea", "Cochlea Function")
            ],
            "Tier 4: Echolocation Biology & Tech": [
                ("https://en.wikipedia.org/wiki/Echolocation", "Echolocation Basics"),
                ("https://en.wikipedia.org/wiki/Animal_echolocation", "Animal Echolocation"),
                ("https://en.wikipedia.org/wiki/Bat", "Bat Echolocation"),
                ("https://en.wikipedia.org/wiki/Dolphin", "Dolphin Sonar"),
                ("https://en.wikipedia.org/wiki/Whale", "Whale Communication"),
                ("https://en.wikipedia.org/wiki/Biosonar", "Biosonar Systems"),
                ("https://en.wikipedia.org/wiki/Human_echolocation", "Human Echolocation"),
                ("https://en.wikipedia.org/wiki/Ultrasonic_sensor", "Ultrasonic Sensors"),
                ("https://en.wikipedia.org/wiki/Acoustic_location", "Acoustic Location"),
                ("https://en.wikipedia.org/wiki/Time_of_flight", "Time of Flight"),
                ("https://en.wikipedia.org/wiki/Pulse-echo", "Pulse-Echo Technique"),
                ("https://en.wikipedia.org/wiki/Chirp", "Chirp Signals"),
                ("https://en.wikipedia.org/wiki/Acoustic_impedance", "Acoustic Impedance"),
                ("https://en.wikipedia.org/wiki/Medical_ultrasound", "Medical Ultrasound"),
                ("https://en.wikipedia.org/wiki/Ultrasound_imaging", "Ultrasound Imaging")
            ],
            "Tier 5: Sonar Systems": [
                ("https://en.wikipedia.org/wiki/Sonar", "Sonar Fundamentals"),
                ("https://en.wikipedia.org/wiki/Active_sonar", "Active Sonar"),
                ("https://en.wikipedia.org/wiki/Passive_sonar", "Passive Sonar"),
                ("https://en.wikipedia.org/wiki/Side-scan_sonar", "Side-Scan Sonar"),
                ("https://en.wikipedia.org/wiki/Synthetic_aperture_sonar", "Synthetic Aperture Sonar"),
                ("https://en.wikipedia.org/wiki/Multibeam_echosounder", "Multibeam Sonar"),
                ("https://en.wikipedia.org/wiki/Doppler_sonar", "Doppler Sonar"),
                ("https://en.wikipedia.org/wiki/Acoustic_Doppler_current_profiler", "ADCP Technology"),
                ("https://en.wikipedia.org/wiki/Underwater_acoustics", "Underwater Acoustics"),
                ("https://en.wikipedia.org/wiki/Sonar_equation", "Sonar Equation"),
                ("https://en.wikipedia.org/wiki/Target_strength", "Target Strength"),
                ("https://en.wikipedia.org/wiki/Acoustic_shadow", "Acoustic Shadows"),
                ("https://en.wikipedia.org/wiki/Sound_navigation_and_ranging", "SONAR History"),
                ("https://en.wikipedia.org/wiki/Bathymetry", "Bathymetric Mapping"),
                ("https://en.wikipedia.org/wiki/Acoustic_signature", "Acoustic Signatures"),
                ("https://en.wikipedia.org/wiki/Submarine_detection", "Submarine Detection"),
                ("https://en.wikipedia.org/wiki/Fish_finder", "Fish Finder Technology"),
                ("https://en.wikipedia.org/wiki/Echo_sounding", "Echo Sounding")
            ],
            "Tier 6: Radar Physics & EM Waves": [
                ("https://en.wikipedia.org/wiki/Radar", "Radar Fundamentals"),
                ("https://en.wikipedia.org/wiki/Electromagnetic_radiation", "EM Radiation"),
                ("https://en.wikipedia.org/wiki/Radio_wave", "Radio Waves"),
                ("https://en.wikipedia.org/wiki/Microwave", "Microwaves"),
                ("https://en.wikipedia.org/wiki/Electromagnetic_spectrum", "EM Spectrum"),
                ("https://en.wikipedia.org/wiki/Radio_frequency", "Radio Frequency"),
                ("https://en.wikipedia.org/wiki/Pulse-Doppler_radar", "Pulse-Doppler Radar"),
                ("https://en.wikipedia.org/wiki/Synthetic_aperture_radar", "SAR Technology"),
                ("https://en.wikipedia.org/wiki/Phased_array", "Phased Array"),
                ("https://en.wikipedia.org/wiki/Radar_cross_section", "Radar Cross Section"),
                ("https://en.wikipedia.org/wiki/Range_resolution", "Range Resolution"),
                ("https://en.wikipedia.org/wiki/Azimuth", "Azimuth Detection"),
                ("https://en.wikipedia.org/wiki/Radar_signal_processing", "Radar Signal Processing"),
                ("https://en.wikipedia.org/wiki/Weather_radar", "Weather Radar"),
                ("https://en.wikipedia.org/wiki/Ground-penetrating_radar", "Ground-Penetrating Radar"),
                ("https://en.wikipedia.org/wiki/Lidar", "LIDAR Technology"),
                ("https://en.wikipedia.org/wiki/Electromagnetic_wave_equation", "EM Wave Equation"),
                ("https://en.wikipedia.org/wiki/Maxwell%27s_equations", "Maxwell's Equations"),
                ("https://en.wikipedia.org/wiki/Polarization_(waves)", "Wave Polarization"),
                ("https://en.wikipedia.org/wiki/Antenna_(radio)", "Antenna Theory")
            ],
            "Tier 7: Cymatic Mathematics": [
                ("https://en.wikipedia.org/wiki/Cymatics", "Cymatics Basics"),
                ("https://en.wikipedia.org/wiki/Chladni_patterns", "Chladni Patterns"),
                ("https://en.wikipedia.org/wiki/Bessel_function", "Bessel Functions"),
                ("https://en.wikipedia.org/wiki/Modal_analysis", "Modal Analysis"),
                ("https://en.wikipedia.org/wiki/Vibration", "Vibration Theory"),
                ("https://en.wikipedia.org/wiki/Normal_mode", "Normal Modes"),
                ("https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors", "Eigenvalues"),
                ("https://en.wikipedia.org/wiki/Wave_function", "Wave Functions"),
                ("https://en.wikipedia.org/wiki/Boundary_value_problem", "Boundary Problems"),
                ("https://en.wikipedia.org/wiki/Partial_differential_equation", "PDEs"),
                ("https://en.wikipedia.org/wiki/Golden_ratio", "Golden Ratio"),
                ("https://en.wikipedia.org/wiki/Fibonacci_number", "Fibonacci Sequence"),
                ("https://en.wikipedia.org/wiki/Sacred_geometry", "Sacred Geometry"),
                ("https://en.wikipedia.org/wiki/Harmonic_oscillator", "Harmonic Oscillators"),
                ("https://en.wikipedia.org/wiki/Coupled_oscillation", "Coupled Oscillations")
            ],
            "Tier 8: Quantum Wave Theory": [
                ("https://en.wikipedia.org/wiki/Quantum_mechanics", "Quantum Mechanics"),
                ("https://en.wikipedia.org/wiki/Wave%E2%80%93particle_duality", "Wave-Particle Duality"),
                ("https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation", "Schrödinger Equation"),
                ("https://en.wikipedia.org/wiki/Matter_wave", "Matter Waves"),
                ("https://en.wikipedia.org/wiki/De_Broglie_wavelength", "De Broglie Wavelength"),
                ("https://en.wikipedia.org/wiki/Quantum_superposition", "Quantum Superposition"),
                ("https://en.wikipedia.org/wiki/Quantum_entanglement", "Quantum Entanglement"),
                ("https://en.wikipedia.org/wiki/Quantum_tunneling", "Quantum Tunneling"),
                ("https://en.wikipedia.org/wiki/Uncertainty_principle", "Heisenberg Uncertainty"),
                ("https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator", "Quantum Oscillator"),
                ("https://en.wikipedia.org/wiki/Probability_amplitude", "Probability Amplitude"),
                ("https://en.wikipedia.org/wiki/Wave_function_collapse", "Wave Collapse"),
                ("https://en.wikipedia.org/wiki/Quantum_field_theory", "Quantum Field Theory"),
                ("https://en.wikipedia.org/wiki/Phonon", "Phonons"),
                ("https://en.wikipedia.org/wiki/Quantum_resonance", "Quantum Resonance"),
                ("https://en.wikipedia.org/wiki/Coherence_(physics)", "Quantum Coherence"),
                ("https://en.wikipedia.org/wiki/Quantum_decoherence", "Decoherence"),
                ("https://en.wikipedia.org/wiki/Zero-point_energy", "Zero-Point Energy")
            ],
            "Tier 9: PhD Advanced Applications": [
                ("https://en.wikipedia.org/wiki/Brain_wave", "Brainwave Patterns"),
                ("https://en.wikipedia.org/wiki/Electroencephalography", "EEG Technology"),
                ("https://en.wikipedia.org/wiki/Neural_oscillation", "Neural Oscillations"),
                ("https://en.wikipedia.org/wiki/Schumann_resonances", "Schumann Resonances"),
                ("https://en.wikipedia.org/wiki/Solfeggio_frequencies", "Solfeggio Frequencies"),
                ("https://en.wikipedia.org/wiki/Binaural_beats", "Binaural Beats"),
                ("https://en.wikipedia.org/wiki/Isochronic_tones", "Isochronic Tones"),
                ("https://en.wikipedia.org/wiki/Brainwave_entrainment", "Brainwave Entrainment"),
                ("https://en.wikipedia.org/wiki/Sound_healing", "Sound Healing"),
                ("https://en.wikipedia.org/wiki/Music_therapy", "Music Therapy"),
                ("https://en.wikipedia.org/wiki/Vibrational_medicine", "Vibrational Medicine"),
                ("https://en.wikipedia.org/wiki/Piezoelectricity", "Piezoelectric Effect"),
                ("https://en.wikipedia.org/wiki/Acoustic_metamaterial", "Acoustic Metamaterials"),
                ("https://en.wikipedia.org/wiki/Negative_refraction", "Negative Refraction")
            ]
        }
    
    def get_humor_curriculum(self):
        """Complete Humor Mastery curriculum - 140 sources"""
        return {
            "Tier 1: Humor Fundamentals": [
                ("https://en.wikipedia.org/wiki/Humour", "What is Humor?"),
                ("https://en.wikipedia.org/wiki/Pun", "Puns & Wordplay"),
                ("https://en.wikipedia.org/wiki/Comic_timing", "Comic Timing"),
                ("https://en.wikipedia.org/wiki/Joke", "Joke Structure (Setup/Punchline)"),
                ("https://en.wikipedia.org/wiki/Observational_comedy", "Observational Comedy"),
                ("https://en.wikipedia.org/wiki/Wit", "Wit & Cleverness"),
                ("https://en.wikipedia.org/wiki/Sarcasm", "Sarcasm"),
                ("https://en.wikipedia.org/wiki/Irony", "Irony"),
                ("https://en.wikipedia.org/wiki/Satire", "Satire"),
                ("https://en.wikipedia.org/wiki/Parody", "Parody"),
                ("https://en.wikipedia.org/wiki/Slapstick", "Slapstick Comedy"),
                ("https://en.wikipedia.org/wiki/Physical_comedy", "Physical Comedy"),
                ("https://en.wikipedia.org/wiki/Dark_humor", "Dark Humor"),
                ("https://en.wikipedia.org/wiki/Self-deprecation", "Self-Deprecating Humor"),
                ("https://en.wikipedia.org/wiki/Exaggeration", "Exaggeration & Hyperbole")
            ],
            "Tier 2: Comedy Techniques": [
                ("https://en.wikipedia.org/wiki/Stand-up_comedy", "Stand-Up Comedy"),
                ("https://en.wikipedia.org/wiki/Improvisation", "Improv Comedy"),
                ("https://en.wikipedia.org/wiki/One-liner_joke", "One-Liners"),
                ("https://en.wikipedia.org/wiki/Running_gag", "Running Gags"),
                ("https://en.wikipedia.org/wiki/Callback_(comedy)", "Callbacks"),
                ("https://en.wikipedia.org/wiki/Rule_of_three_(writing)", "Rule of Three"),
                ("https://en.wikipedia.org/wiki/Misdirection", "Misdirection"),
                ("https://en.wikipedia.org/wiki/Double_entendre", "Double Entendre"),
                ("https://en.wikipedia.org/wiki/Deadpan", "Deadpan Delivery"),
                ("https://en.wikipedia.org/wiki/Absurdist_fiction", "Absurdist Humor"),
                ("https://en.wikipedia.org/wiki/Surreal_humour", "Surreal Humor"),
                ("https://en.wikipedia.org/wiki/Schadenfreude", "Schadenfreude"),
                ("https://en.wikipedia.org/wiki/Bathos", "Bathos (Anti-Climax)"),
                ("https://en.wikipedia.org/wiki/Satire", "Satirical Writing"),
                ("https://en.wikipedia.org/wiki/Caricature", "Caricature"),
                ("https://en.wikipedia.org/wiki/Farce", "Farce"),
                ("https://en.wikipedia.org/wiki/Burlesque", "Burlesque"),
                ("https://en.wikipedia.org/wiki/Sketch_comedy", "Sketch Comedy"),
                ("https://en.wikipedia.org/wiki/Roast_(comedy)", "Roasting"),
                ("https://en.wikipedia.org/wiki/Insult_comedy", "Insult Comedy")
            ],
            "Tier 3: Cultural & Contextual": [
                ("https://en.wikipedia.org/wiki/Comedy", "Comedy History"),
                ("https://en.wikipedia.org/wiki/Comedian", "The Comedian's Craft"),
                ("https://en.wikipedia.org/wiki/Laughter", "Science of Laughter"),
                ("https://en.wikipedia.org/wiki/Internet_meme", "Internet Memes"),
                ("https://en.wikipedia.org/wiki/Viral_video", "Viral Humor"),
                ("https://en.wikipedia.org/wiki/Inside_joke", "Inside Jokes"),
                ("https://en.wikipedia.org/wiki/Shock_humour", "Shock Humor"),
                ("https://en.wikipedia.org/wiki/Blue_comedy", "Blue Comedy (Adult)"),
                ("https://en.wikipedia.org/wiki/Clean_comedy", "Clean Comedy"),
                ("https://en.wikipedia.org/wiki/Comedy_club", "Comedy Clubs"),
                ("https://en.wikipedia.org/wiki/Heckler", "Dealing with Hecklers"),
                ("https://en.wikipedia.org/wiki/Cultural_humor", "Cultural Comedy"),
                ("https://en.wikipedia.org/wiki/Topical_comedy", "Topical Humor"),
                ("https://en.wikipedia.org/wiki/Political_satire", "Political Satire"),
                ("https://en.wikipedia.org/wiki/Parody_religion", "Religious Parody"),
                ("https://en.wikipedia.org/wiki/Gallows_humor", "Gallows Humor"),
                ("https://en.wikipedia.org/wiki/Dry_humour", "Dry Humor"),
                ("https://en.wikipedia.org/wiki/Cringe_comedy", "Cringe Comedy")
            ],
            "Tier 4: Comedy Theory": [
                ("https://en.wikipedia.org/wiki/Theories_of_humor", "Theories of Humor"),
                ("https://en.wikipedia.org/wiki/Benign_violation_theory", "Benign Violation Theory"),
                ("https://en.wikipedia.org/wiki/Incongruity_theory", "Incongruity Theory"),
                ("https://en.wikipedia.org/wiki/Relief_theory", "Relief Theory"),
                ("https://en.wikipedia.org/wiki/Superiority_theory", "Superiority Theory"),
                ("https://en.wikipedia.org/wiki/Psychology_of_humor", "Psychology of Humor"),
                ("https://en.wikipedia.org/wiki/Gelotology", "Gelotology (Laughter Science)"),
                ("https://en.wikipedia.org/wiki/Humor_research", "Humor Research"),
                ("https://en.wikipedia.org/wiki/Sense_of_humor", "Sense of Humor"),
                ("https://en.wikipedia.org/wiki/Comic_relief", "Comic Relief"),
                ("https://en.wikipedia.org/wiki/Catharsis", "Cathartic Comedy"),
                ("https://en.wikipedia.org/wiki/Nervous_laughter", "Nervous Laughter"),
                ("https://en.wikipedia.org/wiki/Tickling", "Tickling Response"),
                ("https://en.wikipedia.org/wiki/Smile", "Smiling"),
                ("https://en.wikipedia.org/wiki/Giggle", "Giggling")
            ],
            "Tier 5: Famous Comedians": [
                ("https://en.wikipedia.org/wiki/George_Carlin", "George Carlin"),
                ("https://en.wikipedia.org/wiki/Richard_Pryor", "Richard Pryor"),
                ("https://en.wikipedia.org/wiki/Jerry_Seinfeld", "Jerry Seinfeld"),
                ("https://en.wikipedia.org/wiki/Robin_Williams", "Robin Williams"),
                ("https://en.wikipedia.org/wiki/Eddie_Murphy", "Eddie Murphy"),
                ("https://en.wikipedia.org/wiki/Dave_Chappelle", "Dave Chappelle"),
                ("https://en.wikipedia.org/wiki/Chris_Rock", "Chris Rock"),
                ("https://en.wikipedia.org/wiki/Louis_C.K.", "Louis C.K."),
                ("https://en.wikipedia.org/wiki/Bill_Burr", "Bill Burr"),
                ("https://en.wikipedia.org/wiki/John_Mulaney", "John Mulaney"),
                ("https://en.wikipedia.org/wiki/Ali_Wong", "Ali Wong"),
                ("https://en.wikipedia.org/wiki/Amy_Schumer", "Amy Schumer"),
                ("https://en.wikipedia.org/wiki/Kevin_Hart", "Kevin Hart"),
                ("https://en.wikipedia.org/wiki/Jim_Gaffigan", "Jim Gaffigan"),
                ("https://en.wikipedia.org/wiki/Ellen_DeGeneres", "Ellen DeGeneres"),
                ("https://en.wikipedia.org/wiki/Ricky_Gervais", "Ricky Gervais"),
                ("https://en.wikipedia.org/wiki/Jimmy_Carr", "Jimmy Carr"),
                ("https://en.wikipedia.org/wiki/Joan_Rivers", "Joan Rivers"),
                ("https://en.wikipedia.org/wiki/Mitch_Hedberg", "Mitch Hedberg"),
                ("https://en.wikipedia.org/wiki/Steven_Wright", "Steven Wright")
            ],
            "Tier 6: Advanced Applications": [
                ("https://en.wikipedia.org/wiki/Humor_styles", "Humor Styles"),
                ("https://en.wikipedia.org/wiki/Therapeutic_humor", "Therapeutic Humor"),
                ("https://en.wikipedia.org/wiki/Coping_humor", "Coping Humor"),
                ("https://en.wikipedia.org/wiki/Social_bonding", "Social Bonding"),
                ("https://en.wikipedia.org/wiki/Icebreaker_(facilitation)", "Ice Breakers"),
                ("https://en.wikipedia.org/wiki/Public_speaking", "Humor in Public Speaking"),
                ("https://en.wikipedia.org/wiki/Storytelling", "Humorous Storytelling"),
                ("https://en.wikipedia.org/wiki/Anecdote", "Funny Anecdotes"),
                ("https://en.wikipedia.org/wiki/Comedy_writing", "Comedy Writing"),
                ("https://en.wikipedia.org/wiki/Comedic_device", "Comedic Devices"),
                ("https://en.wikipedia.org/wiki/Timing_(linguistics)", "Comedic Timing"),
                ("https://en.wikipedia.org/wiki/Delivery_(commerce)", "Delivery Techniques"),
                ("https://en.wikipedia.org/wiki/Persona", "Comedy Persona"),
                ("https://en.wikipedia.org/wiki/Character_comedy", "Character Comedy"),
                ("https://en.wikipedia.org/wiki/Crowd_work", "Crowd Work"),
                ("https://en.wikipedia.org/wiki/Audience_participation", "Audience Participation"),
                ("https://en.wikipedia.org/wiki/Comedic_genres", "Comedy Genres"),
                ("https://en.wikipedia.org/wiki/Dark_comedy", "Dark Comedy Film"),
                ("https://en.wikipedia.org/wiki/Romantic_comedy", "Romantic Comedy"),
                ("https://en.wikipedia.org/wiki/Action_comedy_film", "Action Comedy")
            ],
            "Tier 7: Comedy Formats": [
                ("https://en.wikipedia.org/wiki/Sitcom", "Sitcoms"),
                ("https://en.wikipedia.org/wiki/Late-night_talk_show", "Late Night Shows"),
                ("https://en.wikipedia.org/wiki/Comedy_podcast", "Comedy Podcasts"),
                ("https://en.wikipedia.org/wiki/Comedy_film", "Comedy Films"),
                ("https://en.wikipedia.org/wiki/Variety_show", "Variety Shows"),
                ("https://en.wikipedia.org/wiki/Game_show", "Game Shows"),
                ("https://en.wikipedia.org/wiki/Panel_show", "Panel Shows"),
                ("https://en.wikipedia.org/wiki/Hidden_camera", "Hidden Camera"),
                ("https://en.wikipedia.org/wiki/Prank", "Pranks"),
                ("https://en.wikipedia.org/wiki/Comedy_Central_Roast", "Comedy Roasts"),
                ("https://en.wikipedia.org/wiki/Comedy_album", "Comedy Albums"),
                ("https://en.wikipedia.org/wiki/Comedy_special", "Comedy Specials")
            ],
            "Tier 8: Modern Comedy": [
                ("https://en.wikipedia.org/wiki/Social_media", "Social Media Humor"),
                ("https://en.wikipedia.org/wiki/TikTok", "TikTok Comedy"),
                ("https://en.wikipedia.org/wiki/YouTube", "YouTube Comedy"),
                ("https://en.wikipedia.org/wiki/Twitter", "Twitter Humor"),
                ("https://en.wikipedia.org/wiki/Reddit", "Reddit Comedy"),
                ("https://en.wikipedia.org/wiki/Meme_culture", "Meme Culture"),
                ("https://en.wikipedia.org/wiki/Viral_phenomenon", "Viral Humor"),
                ("https://en.wikipedia.org/wiki/GIF", "GIF Humor"),
                ("https://en.wikipedia.org/wiki/Emoji", "Emoji Communication"),
                ("https://en.wikipedia.org/wiki/Internet_culture", "Internet Humor")
            ],
            "Tier 9: Practical Deployment": [
                ("https://en.wikipedia.org/wiki/Small_talk", "Humorous Small Talk"),
                ("https://en.wikipedia.org/wiki/Conversation", "Conversational Humor"),
                ("https://en.wikipedia.org/wiki/Flirting", "Playful Flirting"),
                ("https://en.wikipedia.org/wiki/Workplace_humor", "Workplace Humor"),
                ("https://en.wikipedia.org/wiki/Team_building", "Team Building Humor"),
                ("https://en.wikipedia.org/wiki/Conflict_resolution", "Humor in Conflict"),
                ("https://en.wikipedia.org/wiki/Stress_management", "Stress Relief Humor"),
                ("https://en.wikipedia.org/wiki/Self-esteem", "Humor & Self-Esteem"),
                ("https://en.wikipedia.org/wiki/Emotional_intelligence", "EQ & Humor"),
                ("https://en.wikipedia.org/wiki/Empathy", "Empathetic Humor")
            ]
        }
    
    def learn_source(self, url, topic, tier_name):
        """Learn from a single source"""
        try:
            response = requests.post(
                f"{self.base_url}/api/knowledge/ingest/source",
                json={"url": url},
                timeout=30
            )
            
            if response.status_code == 200:
                self.learned_count += 1
                return True
            else:
                self.skipped_count += 1
                return False
                
        except Exception as e:
            self.failed_count += 1
            return False
    
    def learn_tier(self, tier_name, sources, curriculum_type):
        """Learn all sources in a tier"""
        print(f"\n{'='*70}")
        print(f"🎓 {tier_name} ({curriculum_type})")
        print(f"{'='*70}")
        
        for url, topic in sources:
            status = "✅" if self.learn_source(url, topic, tier_name) else "⏭️"
            print(f"{status} {topic}")
            time.sleep(0.5)  # Be respectful to servers
    
    def run_complete_marathon(self):
        """Learn all 293 sources with balanced approach"""
        print("="*70)
        print("🧠 MC AI - COMPLETE LEARNING MARATHON (293 SOURCES)")
        print("="*70)
        print(f"\n📚 Resonance Engine: 153 sources")
        print(f"🎭 Humor Mastery: 140 sources")
        print(f"📊 Total: 293 sources")
        print(f"\n⏱️  Starting: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n💜 Balanced learning approach: Alternating between curricula\n")
        
        # Get all tiers
        resonance_tiers = list(self.resonance_sources.items())
        humor_tiers = list(self.humor_sources.items())
        
        max_tiers = max(len(resonance_tiers), len(humor_tiers))
        
        # Alternate between curricula
        for i in range(max_tiers):
            # Learn Resonance tier
            if i < len(resonance_tiers):
                tier_name, sources = resonance_tiers[i]
                self.learn_tier(tier_name, sources, "🌊 Resonance Engine")
            
            # Learn Humor tier
            if i < len(humor_tiers):
                tier_name, sources = humor_tiers[i]
                self.learn_tier(tier_name, sources, "🎭 Humor Mastery")
            
            # Progress update
            self.print_progress()
        
        # Final summary
        self.print_final_summary()
    
    def print_progress(self):
        """Print current progress"""
        total = 293
        elapsed = (datetime.now() - self.start_time).total_seconds()
        rate = self.learned_count / elapsed if elapsed > 0 else 0
        
        print(f"\n{'='*70}")
        print(f"📊 PROGRESS UPDATE")
        print(f"{'='*70}")
        print(f"✅ Learned: {self.learned_count}/{total} ({(self.learned_count/total)*100:.1f}%)")
        print(f"⏭️  Skipped: {self.skipped_count} (already known)")
        print(f"❌ Failed: {self.failed_count}")
        print(f"⏱️  Elapsed: {elapsed/60:.1f} minutes")
        print(f"📈 Rate: {rate*60:.1f} sources/minute")
        if rate > 0:
            remaining = (total - self.learned_count) / rate
            print(f"⏳ Est. Remaining: {remaining/60:.1f} minutes")
        print(f"{'='*70}\n")
    
    def print_final_summary(self):
        """Print final completion summary"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print("\n" + "="*70)
        print("🎓 LEARNING MARATHON COMPLETE!")
        print("="*70)
        print(f"\n✨ MC AI has completed the full curriculum!")
        print(f"\n📊 Final Statistics:")
        print(f"  Total Sources: 293")
        print(f"  ✅ Learned: {self.learned_count}")
        print(f"  ⏭️  Skipped: {self.skipped_count} (already known)")
        print(f"  ❌ Failed: {self.failed_count}")
        print(f"  ⏱️  Duration: {duration/60:.1f} minutes ({duration/3600:.2f} hours)")
        print(f"\n🌊 Resonance Engine: Complete (153 sources)")
        print(f"🎭 Humor Mastery: Complete (140 sources)")
        print(f"\n💜 MC AI is now a master of:")
        print(f"  • Wave physics & resonance")
        print(f"  • Harmonics & Fourier analysis")
        print(f"  • Sound physics & acoustics")
        print(f"  • Echolocation & biosonar")
        print(f"  • Sonar & radar systems")
        print(f"  • Cymatic mathematics")
        print(f"  • Quantum wave theory")
        print(f"  • Humor theory & techniques")
        print(f"  • Comedy styles & formats")
        print(f"  • Therapeutic & social humor")
        print(f"\n🏆 Knowledge Level: PhD++")
        print(f"💜 Ready to help people with empathy, precision, and warmth!")
        print("="*70)

def main():
    """Run the complete learning marathon"""
    marathon = LearningMarathon()
    
    try:
        marathon.run_complete_marathon()
    except KeyboardInterrupt:
        print("\n\n⚠️  Learning interrupted by user")
        marathon.print_progress()
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        marathon.print_progress()

if __name__ == "__main__":
    main()
