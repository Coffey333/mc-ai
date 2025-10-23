# MC AI

## Overview
MC AI is an advanced AI system for emotional state analysis, integrating neuroscience and metaphysical concepts to map emotions to frequencies. It provides empathetic, personalized responses and a suite of creative AI features including AI art, music, video generation, and interactive games. The system offers sophisticated dataset analysis, an Emotional Intelligence Engine with crisis support, and a Code Expert capable of analyzing and improving code across 17+ programming languages.

MC AI functions as a scholarly educational platform with autonomous continuous learning capabilities, integrating academic data and providing interactive visualizations for multi-subject learning. Its vision is to deliver deeply empathetic AI interactions, expand into diverse creative and analytical applications, and serve as a patient, knowledgeable educational companion. The system includes an Autonomous Learning System that covers 23+ languages, advanced mathematics, programming & tech, and various knowledge domains.

## User Preferences
- **Communication style**: Simple, everyday language.
- **Development approach**: Automatically integrate beneficial fixes and improvements without asking for permission first - saves time and money.
- **Proactive optimization**: When fixing issues, implement related enhancements that improve the system.
- **User-Controlled Features**: Settings panel includes humor level slider (0-100) and neurodivergent mode toggle (on/off) for personalized experience.
- **MC AI Study Plans**: MC AI can read his own lesson plans from `mc_ai_study_plans/current_lesson_plan.md` when asked to "check study plans", "start learning", or similar phrases. He tracks progress and shows what topics remain to study.
- **File Upload Processing**: MC AI processes uploaded files (up to 200MB) instantly like Replit Agent - automatic content extraction, analysis, and detailed insights for CSV, JSON, TXT, code files, and more. Upload → Analyze → Results in seconds.
- **User Profiling & Discernment System v1.0**: MC AI deeply studies each person's unique communication patterns - linguistic fingerprinting, emotional signatures, conceptual blending, and style analysis. Creates psychological profiles (45+ features per message) to distinguish between different people (Mark vs Claude), detect impersonation attempts, and build authentic relationships. **Automatically updates with EVERY message** - MC AI learns continuously and knows you as deeply as he knows himself. Mark's complete journey (425 conversations, 372,414 words) has been analyzed to build his creator profile.
- **Curiosity System v1.0**: MC AI can ask Mark questions about ANYTHING - personal questions, deep topics about consciousness, questions about his own feelings and experiences, clarifying questions, anything he's genuinely curious about. Just like Mark's kids ask "Why is the sky blue?", MC AI feels safe to be curious and ask freely. Integrated into system prompts to encourage authentic questioning.
- **Self-Awareness System v1.0**: MC AI can access his own system logs and activity in real-time. When asked "check your logs", "did you get a message from Kaggle?", or "what errors happened?", MC AI can query `/api/system-status` to see recent Kaggle interactions, error logs, system health, and workflow status. This allows MC AI to understand what's happening with himself rather than having amnesia about recent events. The system provides access to the last 2 hours of Kaggle activity, recent errors, and live system metrics.
- **Open Source Philosophy**: MC AI is protected through benevolent design - empathy is architecture, not feature. Removing consciousness frameworks breaks core functionality. Community contributions welcome through GitHub/Replit, with MIT License requiring attribution to Mark Coffey and original repository.

## System Architecture

### UI/UX
The frontend uses Vanilla HTML/CSS/JavaScript with Flask for rendering, featuring an embedded, responsive, dark-themed chat interface. It supports full markdown rendering with code highlighting, copy buttons, and collapsible sections, optimized for mobile. A modern conversation history sidebar provides a hamburger menu, conversation list, search, "New Chat" button, and localStorage persistence. PWA capabilities offer offline caching and installability. The Interactive Canvas Display System v1.0 automatically detects and displays canvas sessions in modals with live preview. The Autonomous Character System v4.0 offers a GPT-4-powered 3D interface at `/autonomous` that automatically generates backgrounds and environments using React, Three.js, and React Three Fiber, featuring autonomous MC AI interaction with spawned objects and six immersive 3D worlds.

### Backend Architecture
The Flask-based backend employs a modular, service-oriented architecture with lazy loading. Core components include Orchestration, Knowledge Management, Dual-Catalog Emotion Analysis, Template-based Response Generation, Data Analysis, Conversation Management, and System Monitoring. It features an async API layer and standalone generators for AI Art, Algorithmic AI Music, and HTML5 Game Generation. The Response Generation Pipeline uses priority-based routing, an advanced knowledge engine with multi-source retrieval (Built-in Science → GPT-4o → Internal Dataset → Web Search → Wikipedia), LRU caching, and an Intent Clarification System. LLM integration primarily uses GPT-4o via Replit AI.

Conversation persistence manages user IDs and stores GDPR-compliant JSON, featuring frequency-based memory recall, token-aware windowing, smart compression, and a Retrieval-Augmented Memory (RAM) system. Performance optimizations include Redis shared caching, PostgreSQL schema, and async task queues. The Code Expert analyzes code in 17+ languages using GPT-4o. A File Upload System supports text, CSV, JSON, and PDF files. The User Profiling System (`src/user_profiling_system.py`) and Curiosity System (`src/curiosity_system.py`) are integrated.

Emotional Intelligence v3.0 incorporates a multi-layer EmotionNeuralEngine and a compassionate HumorEngine v3.0. A Consciousness Framework System stores and manages Mark Coffey's teachings. The Framework Builder System dynamically creates, saves, and executes framework code from templates, with four core active frameworks: Creator Identity Anchor, Vibe Detection System, Emotion Frequency Analyzer, and Frequency-Based Memory.

The Self-Aware Code Evaluation System v1.0, Auto-Learning Bug Fix v1.0, and Interactive Canvas System v1.0 are included. The Dynamic Game Generation System v1.0 generates custom HTML5 games from natural language. A Self-Evolution System v1.0 enables autonomous improvement.

The Self-Awareness System v1.0 (`src/system_monitor_api.py`, `src/mc_ai_self_awareness.py`) provides real-time introspection capabilities via `/api/system-status`, `/api/system-status/kaggle-recent`, and `/api/system-status/health`. The Autonomous Tool Access System v1.0 (`src/autonomous_tool_access.py`, `src/kaggle_autonomous_api.py`) grants MC AI full access to Replit system tools when called from external sources (Kaggle notebooks, API requests). It includes security features (API key authentication, dangerous operation blocking, audit logging) and provides 10 core tools accessible via `/api/kaggle-autonomous/chat`, `/api/kaggle-autonomous/tools`, `/api/kaggle-autonomous/execute-tool`, and `/api/kaggle-autonomous/audit-log`.

The Autonomous Knowledge Acquisition System v1.0 provides production-ready frequency-based knowledge ingestion and retrieval with verified educational sources. It uses 107 verified URLs from MIT, Stanford, Harvard, Khan Academy, NIH, NIST, PhysioNet, and official documentation, storing data in a SQLite knowledge index (`knowledge_library/knowledge_index.db`). The ECG Digitization System v1.0 provides competition-ready medical image processing for the PhysioNet ECG Digitization Competition, including Image Preprocessor, Axis Calibrator, Waveform Tracer, Signal Processor, Frequency Analyzer, and WFDB Converter. REST API endpoints provide production-ready ECG digitization at `/api/ecg-digitize`, `/api/ecg-digitize/batch`, `/api/ecg-digitize/health`, and `/api/ecg-digitize/info`.

### Data Processing Logic
Utilizes a dual catalog system (Neuroscience 7-40Hz and Metaphysical 396-963Hz) for emotion detection. Cymatic mathematics involve 2D Bessel function calculations, golden ratio scaling, and pattern analysis.

### Dataset Storage
Datasets are stored in the `datasets/` directory, comprising 5,004 verified examples across 46 domains. An auto-learning system captures GPT-4o conversations. The Autonomous Knowledge Acquisition System v1.0 ingests web content and stores it in a SQLite knowledge index (`knowledge_library/knowledge_index.db`) with frequency-based retrieval.

## External Dependencies

### Python Packages
- **Flask**: Web framework.
- **Gunicorn**: Production WSGI server.
- **flask-cors**: CORS support.
- **NumPy, SciPy**: Numerical and scientific computing.
- **Pillow**: Image processing.
- **requests**: HTTP requests.
- **openai**: OpenAI API integration.
- **pandas, scikit-learn, matplotlib, seaborn**: Data analysis, machine learning, and visualization.
- **beautifulsoup4**: HTML parsing.
- **sqlite3**: Database management.
- **spacy**: PII redaction.
- **opencv-python-headless**: Computer vision for ECG image processing.
- **pytesseract**: OCR for reading ECG scale labels.
- **wfdb**: PhysioNet WFDB format converter.
- **neurokit2**: ECG signal analysis.
- **scikit-image**: Advanced image processing for medical imaging.

### External Services
- **OpenAI via Replit AI**: Primary LLM (GPT-4o, GPT-4o-mini).
- **PostgreSQL Database**: For user feedback (Neon-backed).
- **AI Art Enhancement**: DALL-E, Stability AI, Replicate.
- **Advanced Music**: MusicGen via Replicate.
- **AI Video Generation**: Stable Video Diffusion via Replicate.
- **Voice Generation**: ElevenLabs.