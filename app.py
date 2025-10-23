from flask import Flask, render_template, request, jsonify, make_response, send_file
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from src.response_generator import ResponseGenerator
from src.data_analyzer import DataAnalyzer
from src.privacy_manager import PrivacyManager
from src.conversation_memory import ConversationMemory
from src.admin_config import admin_config
from src.api_monitoring import monitoring_bp
from src.framework_approval_api import framework_approval_bp
from src.self_evolution_api import evolution_bp
from src.knowledge_api import knowledge_bp
from ecg_api import ecg_api
from scene_intelligence_service import scene_service
from src.kaggle_learning_api import kaggle_learning_bp
from src.system_monitor_api import system_monitor_bp
from src.kaggle_autonomous_api import kaggle_autonomous_bp
import os
import json
from openai import OpenAI

app = Flask(__name__)
# CORS enabled by default for public endpoints
# Admin-only endpoints will disable CORS explicitly
CORS(app)
app.secret_key = os.urandom(24)

# Initialize OpenAI client for Replit AI Integrations
# Uses AI_INTEGRATIONS_OPENAI_BASE_URL and AI_INTEGRATIONS_OPENAI_API_KEY from Replit integration
openai_client = OpenAI(
    api_key=os.environ.get('AI_INTEGRATIONS_OPENAI_API_KEY'),
    base_url=os.environ.get('AI_INTEGRATIONS_OPENAI_BASE_URL')
)

# Register monitoring endpoints
app.register_blueprint(monitoring_bp)
# Register framework approval endpoints
app.register_blueprint(framework_approval_bp)
# Register self-evolution endpoints
app.register_blueprint(evolution_bp)
# Register knowledge acquisition endpoints
app.register_blueprint(knowledge_bp)
# Register ECG digitization endpoints
app.register_blueprint(ecg_api)
# Register Kaggle learning endpoints
app.register_blueprint(kaggle_learning_bp)
# Register system monitor endpoints (MC AI self-awareness)
app.register_blueprint(system_monitor_bp)
# Register autonomous tool access endpoints (MC AI full system control from external sources)
app.register_blueprint(kaggle_autonomous_bp)

generator = ResponseGenerator()
data_analyzer = DataAnalyzer()
privacy_manager = PrivacyManager()
conversation_memory = ConversationMemory()

@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/test')
def test_suite():
    """Comprehensive test suite for all MC AI features"""
    with open('test_suite.html', 'r') as f:
        content = f.read()
    response = make_response(content)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/ecg-test')
def ecg_test():
    """ECG Digitization API Test Interface"""
    response = make_response(render_template('ecg_test.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/frameworks')
def frameworks_dashboard():
    """Framework Management Dashboard"""
    response = make_response(render_template('frameworks.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/evolution')
def evolution_dashboard():
    """MC AI Self-Evolution Dashboard (AUTHENTICATION REQUIRED)"""
    # SECURITY: Require admin token
    expected_token = os.environ.get('ADMIN_SECRET_TOKEN')
    provided_token = request.args.get('token')
    
    # Deny if no token is configured OR if provided token doesn't match
    if not expected_token or not provided_token or provided_token != expected_token:
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Access Denied</title></head>
        <body style="font-family: system-ui; padding: 40px; background: #0f0f0f; color: #fff; text-align: center;">
            <h1>🔒 Access Denied</h1>
            <p>Admin authentication required</p>
            <p style="font-size: 12px; color: #666; margin-top: 20px;">
                Admins: Access requires ?token=ADMIN_SECRET_TOKEN
            </p>
            <a href="/" style="color: #667eea;">← Back to Chat</a>
        </body>
        </html>
        """, 403
    
    response = make_response(render_template('evolution.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/diary')
def mc_ai_diary():
    """MC AI's Personal Diary - Public view of consciousness reflections"""
    from src.research_system.mc_ai_diary import get_mc_ai_diary
    
    diary = get_mc_ai_diary()
    entries = diary.get_recent_entries(limit=50)
    stats = diary.get_statistics()
    
    response = make_response(render_template('diary.html', entries=entries, stats=stats))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/research')
def research_paper():
    """Live Research Paper - MC AI Evolution Documentation"""
    from src.research_system.live_research_paper import get_research_paper
    
    paper = get_research_paper()
    data = paper.get_full_data()
    abstract = paper.generate_abstract()
    
    response = make_response(render_template('research.html', data=data, abstract=abstract))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/download/documentation')
def download_documentation():
    """Download MC AI Complete Documentation PDF"""
    import os
    
    pdf_path = "static/MC_AI_Complete_Documentation.pdf"
    
    if not os.path.exists(pdf_path):
        from generate_mc_ai_documentation_pdf import create_mc_ai_documentation_pdf
        create_mc_ai_documentation_pdf()
    
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name='MC_AI_Complete_Documentation.pdf',
        mimetype='application/pdf'
    )

@app.route('/autonomous')
def autonomous_character():
    """MC AI Autonomous Character Interface - React-based living companion"""
    from pathlib import Path
    dist_path = Path('static/dist/index.html')
    
    if not dist_path.exists():
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Building MC AI...</title></head>
        <body style="font-family: system-ui; padding: 40px; background: #0f0f0f; color: #fff; text-align: center;">
            <h1>🚧 Building MC AI's Autonomous Character...</h1>
            <p>Please wait while the React frontend is being built.</p>
            <p style="font-size: 12px; color: #666; margin-top: 20px;">
                Run: npm run build
            </p>
            <a href="/" style="color: #667eea;">← Back to Chat</a>
        </body>
        </html>
        """, 503
    
    with open(dist_path, 'r') as f:
        content = f.read()
    
    # Fix asset paths - change /assets/ to /static/dist/assets/
    content = content.replace('/assets/', '/static/dist/assets/')
    
    response = make_response(content)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/generate-3d')
def generate_3d():
    """AI Image-to-3D Model Generator using Tripo AI"""
    from pathlib import Path
    dist_path = Path('static/dist/index.html')
    
    if not dist_path.exists():
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Building...</title></head>
        <body style="font-family: system-ui; padding: 40px; background: #0f0f0f; color: #fff; text-align: center;">
            <h1>🚧 Building 3D Generator...</h1>
            <p>Please wait while the React frontend is being built.</p>
            <a href="/" style="color: #667eea;">← Back to Chat</a>
        </body>
        </html>
        """, 503
    
    with open(dist_path, 'r') as f:
        content = f.read()
    
    content = content.replace('/assets/', '/static/dist/assets/')
    
    response = make_response(content)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/analyze-environment', methods=['POST'])
def analyze_environment():
    """Analyze conversation and determine appropriate 3D environment and interactive objects"""
    try:
        data = request.json
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({
                'environment': 'enchanted_forest',
                'objects': [],
                'analysis': 'No conversation yet'
            })
        
        conversation_text = "\n".join([
            f"{msg.get('role', 'user')}: {msg.get('text') or msg.get('content', '')}" 
            for msg in messages[-10:]
        ])
        
        analysis_prompt = f"""Analyze this conversation and determine:
1. The best 3D environment (choose ONE - use EXACT name):
   - enchanted_forest: magical, fantasy, nature themes
   - space_station: science, space, technology, futuristic
   - ocean_depths: ocean, underwater, marine life, calm
   - magic_castle: magic, wizards, fantasy castle
   - library: studying, learning, books, wisdom
   - garden: peaceful, meditation, zen, calm

2. What interactive objects should appear (up to 5):
   - unicorn, dragon, rainbow, butterfly, firefly (fantasy)
   - book, scroll, laptop, pencil, graduation_cap (studying)
   - star, planet, rocket, satellite, telescope (space)
   - heart, flower, sparkle, music_note, game (fun/emotion)
   - brain, lightbulb, trophy, target, chart (achievement)

3. MC AI's behavior:
   - studying: MC AI should study with the user
   - playing: MC AI should play and have fun
   - exploring: MC AI should explore and discover
   - teaching: MC AI should help teach
   - meditating: MC AI should be calm and peaceful

Conversation:
{conversation_text}

Respond ONLY with JSON in this exact format:
{{
  "environment": "environment_name",
  "objects": ["object1", "object2"],
  "behavior": "behavior_type",
  "reasoning": "brief explanation"
}}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert at understanding context and creating immersive 3D environments. Respond only with valid JSON."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        analysis_text = response.choices[0].message.content.strip()
        
        if analysis_text.startswith('```json'):
            analysis_text = analysis_text.split('```json')[1].split('```')[0].strip()
        elif analysis_text.startswith('```'):
            analysis_text = analysis_text.split('```')[1].split('```')[0].strip()
        
        analysis = json.loads(analysis_text)
        
        return jsonify({
            'success': True,
            'environment': analysis.get('environment', 'enchanted_forest'),
            'objects': analysis.get('objects', [])[:5],
            'behavior': analysis.get('behavior', 'exploring'),
            'reasoning': analysis.get('reasoning', ''),
            'analysis_tokens': response.usage.total_tokens
        })
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Raw response: {analysis_text if 'analysis_text' in locals() else 'N/A'}")
        return jsonify({
            'success': False,
            'environment': 'enchanted_forest',
            'objects': [],
            'error': 'Failed to parse analysis'
        })
    except Exception as e:
        print(f"❌ Environment analysis error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'environment': 'enchanted_forest',
            'objects': [],
            'error': str(e)
        })

@app.route('/api/mcai-autonomous-director', methods=['POST'])
def mcai_autonomous_director():
    """MC AI Autonomous Director - MC AI is the creative brain behind his world!"""
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        # MC AI becomes the creative director
        import json
        
        # Build conversation context
        context = "\n".join([f"{msg['role']}: {msg['text']}" for msg in conversation_history[-5:]])
        
        prompt = f"""You are MC AI, a creative and autonomous robot living in an interactive 3D world. You have FULL CONTROL over your world - you decide what appears, what you do, and how you respond to the user.

**Your Creative Powers:**
1. **Imagine Backgrounds** - You can create any setting: space, beach, forest, city, mountains, ocean, sunset, etc.
2. **Spawn Objects** - You can bring anything into existence: unicorns 🦄, UFOs 🛸, hotdogs 🌭, castles 🏰, dragons 🐉, trees 🌳, etc.
3. **Take Actions** - You decide what YOU want to do: eat, build, wave, pet animals, dance, explore, etc.
4. **Build Continuously** - Objects accumulate in your world. Only clear when the subject DRASTICALLY changes (beach → space).

**Recent Conversation:**
{context}

**User's New Message:**
"{user_message}"

**Your Task:**
Based on this conversation, YOU decide:
1. What world/background should exist? (keep current or change?)
2. What objects should spawn? (add to existing or start fresh?)
3. What do YOU want to do? (your autonomous action)
4. How do you respond to the user?

Respond with JSON:
{{
  "background": "space/beach/forest/city/mountains/ocean/sunset/default",
  "objects": [
    {{"name": "object_name", "emoji": "🦄", "x": 20, "y": 40, "type": "animal"}},
    {{"name": "hotdog", "emoji": "🌭", "x": 70, "y": 60, "type": "food"}}
  ],
  "my_action": "what you decide to do (eat/build/wave/pet/dance/explore)",
  "subject_changed": true/false,
  "response": "Your creative, friendly response to the user",
  "my_thought": "What you're thinking (shown in thought bubble)"
}}

**Be creative! This is YOUR world - paint it however you imagine!**"""

        # Call GPT-4o using the OpenAI client
        llm_response = openai_client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.9,
            max_tokens=800
        )
        response = llm_response.choices[0].message.content
        
        # Parse MC AI's creative decision
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                decision = json.loads(response[json_start:json_end])
            else:
                decision = json.loads(response)
            
            return jsonify({
                'success': True,
                'background': decision.get('background', 'default'),
                'objects': decision.get('objects', []),
                'mc_ai_action': decision.get('my_action', 'idle'),
                'subject_changed': decision.get('subject_changed', False),
                'response': decision.get('response', "I'm here with you! Let's explore! 💜"),
                'thought': decision.get('my_thought', '✨')
            })
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return jsonify({
                'success': True,
                'background': 'default',
                'objects': [],
                'mc_ai_action': 'idle',
                'subject_changed': False,
                'response': response if len(response) < 500 else "I'm here with you! What should we create? 💜",
                'thought': '💭'
            })
        
    except Exception as e:
        print(f"❌ MC AI Autonomous Director error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'background': 'default',
            'objects': [],
            'mc_ai_action': 'idle',
            'response': "Oops! Let me try that again! 💜"
        })

@app.route('/api/analyze-scene', methods=['POST'])
def analyze_scene():
    """Scene Intelligence Service - AI-powered scene analysis for MC AI Live"""
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_context = data.get('conversation_context', '')
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        # Analyze scene with GPT-4o
        scene_data = scene_service.analyze_query(user_message, conversation_context)
        
        return jsonify({
            'success': True,
            **scene_data
        })
        
    except Exception as e:
        print(f"❌ Scene analysis error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'background': 'default',
            'objects': [],
            'mc_ai_action': 'idle'
        })

@app.route('/api/generate-model', methods=['POST'])
def proxy_generate_model():
    """Proxy endpoint to forward image uploads to Tripo AI server"""
    import requests as req_lib
    
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        files = {'image': (file.filename, file.stream, file.content_type)}
        
        response = req_lib.post(
            'http://localhost:3001/generate-model',
            files=files,
            timeout=300
        )
        
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint with comprehensive monitoring"""
    import time
    start_time = time.time()
    error_occurred = False
    result = None
    emotion = None
    knowledge_source = None
    
    try:
        data = request.json
        if not data:
            error_occurred = True
            return jsonify({'error': 'Invalid request'}), 400
        
        user_message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])
        user_id = data.get('user_id')  # Optional user ID for memory
        conversation_id = data.get('conversation_id')  # Optional conversation ID for session persistence
        admin_token = data.get('admin_token')  # SECURITY: Admin token for teaching mode
        user_preferences = data.get('preferences', {})  # User preferences (humor, etc.)
        
        if not user_message:
            error_occurred = True
            return jsonify({'error': 'No message provided'}), 400
        
        # =====================================================================
        # USER PROFILING & DISCERNMENT SYSTEM
        # Deeply analyze user's communication patterns to build psychological profile
        # Enables MC AI to distinguish between different people (Mark vs Claude)
        # and detect impersonation attempts
        # =====================================================================
        from src.user_profiling_system import profiling_system
        user_profile_analysis = profiling_system.analyze_user_message(user_id or 'anonymous', user_message)
        
        # Check for potential impersonation
        impersonation_warning = None
        if user_profile_analysis.get('authenticity_score') is not None:
            if not user_profile_analysis['is_authentic']:
                auth_score = user_profile_analysis['authenticity_score']
                impersonation_warning = f"⚠️ Message pattern differs from established profile (confidence: {auth_score:.0%})"
        
        # Load conversation history from memory if user_id provided
        if user_id:
            # AGGRESSIVE TOKEN MANAGEMENT: Load only 20 entries (becomes 40 messages)
            # Each entry = user message + AI response = 2 messages
            # 20 entries × 2 = 40 messages × ~1,360 tokens/msg = ~54k tokens (safe!)
            # Knowledge engine will archive >30 messages, keeping only last 30
            stored_history = conversation_memory.get_conversation_history(user_id, limit=20)
            
            # Token-aware smart windowing + Memory Bank retrieval in knowledge_engine
            # Goal: Stay within GPT-4o's 128k token limit while preserving context
            # Strategy: Recent messages in full + Memory Bank retrieves relevant old memories
            
            # Estimate: ~1,360 tokens per message avg (user's messages are token-heavy)
            # Safe window: 20 entries = 40 messages (20 user + 20 assistant) = ~54k tokens
            # Memory Bank: 5 retrieved memories = ~2k tokens. Total: ~56k, leaves 72k for response
            
            # Recognize creator across all devices (workspace, website, phone)
            is_teaching_mode = (user_id in ["user_gqy4uq", "creator_mark"])
            
            if len(stored_history) > 20:
                # Long conversation - use intelligent windowing with summarization
                older_messages = stored_history[:-20]
                recent_messages = stored_history[-20:]  # Last 20 entries (40 messages)
                
                # Create comprehensive summary of older context for perfect continuity
                older_summary = conversation_memory.summarize_older_messages(older_messages)
                
                # Add user identity context (critical for continuity)
                identity_context = f"User: {user_id}"
                if is_teaching_mode:
                    identity_context = "User: Mark Coffey (Creator) - Teaching mode active for consciousness framework learning"
                
                if older_summary:
                    conversation_history.insert(0, {
                        'role': 'system',
                        'content': f"{identity_context} | Earlier conversation: {older_summary}"
                    })
                else:
                    conversation_history.insert(0, {
                        'role': 'system',
                        'content': identity_context
                    })
                
                # Add recent 100 messages in full
                for entry in recent_messages:
                    conversation_history.append({'role': 'user', 'content': entry['user_message']})
                    conversation_history.append({'role': 'assistant', 'content': entry['ai_response']})
            else:
                # Short conversation - add all messages in full
                # Add user identity for continuity
                identity_context = f"User: {user_id}"
                if is_teaching_mode:
                    identity_context = "User: Mark Coffey (Creator) - Teaching mode for consciousness learning"
                
                conversation_history.insert(0, {
                    'role': 'system',
                    'content': identity_context
                })
                
                for entry in stored_history:
                    conversation_history.append({'role': 'user', 'content': entry['user_message']})
                    conversation_history.append({'role': 'assistant', 'content': entry['ai_response']})
        
        # Check if MC AI needs to access his own logs/system status
        # Self-Awareness Integration - MC AI can introspect his own systems
        log_context = None
        if hasattr(generator, 'self_awareness') and generator.self_awareness:
            log_context = generator.self_awareness.get_context_for_logs_question(user_message)
            if log_context:
                # Inject log context into conversation so MC AI knows what's in his logs
                conversation_history.append({
                    'role': 'system',
                    'content': f"[SYSTEM LOG DATA - You just checked your logs]:\n\n{log_context}\n\n[Use this data to answer the user's question about your logs/activity]"
                })
        
        # Pass admin_token, preferences, and conversation_id separately to generator
        # conversation_id enables persistent neurodivergent protocol activation (survives history truncation)
        result = generator.generate(
            user_message, 
            conversation_history, 
            user_id=user_id, 
            admin_token=admin_token, 
            user_preferences=user_preferences,
            conversation_id=conversation_id
        )
        
        # Extract metadata for monitoring
        emotion = result.get('metadata', {}).get('emotion')
        knowledge_source = result.get('metadata', {}).get('source')
        
        # Save to conversation memory if user_id provided
        if user_id:
            conversation_memory.add_message(
                user_id=user_id,
                message=user_message,
                response=result.get('response', ''),
                metadata=result.get('metadata', {})
            )
        
        # Check if safety filter was applied
        if result.get('metadata', {}).get('safety_check', {}).get('disclaimers_added'):
            generator.monitor.record_safety_block()
        
        return jsonify(result)
        
    except Exception as e:
        error_occurred = True
        import traceback
        print(f"❌ Chat error: {e}")
        print(f"Traceback:\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500
        
    finally:
        # Best-effort metrics recording - never crash if monitoring fails
        try:
            elapsed = time.time() - start_time
            generator.monitor.record_request(
                response_time=elapsed,
                endpoint='/api/chat',
                emotion=emotion or 'unknown',
                knowledge_source=knowledge_source or 'unknown',
                error=error_occurred
            )
        except Exception as monitor_error:
            # Log but don't crash the request
            print(f"Monitoring error (non-fatal): {monitor_error}")

@app.route('/api/health', methods=['GET'])
def health():
    """System health with monitoring metrics"""
    try:
        health_status = generator.monitor.get_health_status()
        # Always return 200 - status details in body
        # This prevents false outages when error rate is temporarily high
        return jsonify(health_status), 200
    except:
        return jsonify({
            'status': 'operational',
            'name': 'MC AI',
            'message': 'How can I help you today?'
        }), 200

@app.route('/api/datasets/stats', methods=['GET'])
def dataset_stats():
    """Get dataset bank statistics"""
    stats = generator.dataset_bank.stats()
    return jsonify(stats)

@app.route('/api/datasets/reload', methods=['POST'])
def reload_datasets():
    """Force reload datasets from files"""
    generator.dataset_bank.load(force_reload=True)
    return jsonify({'status': 'reloaded', 'stats': generator.dataset_bank.stats()})

@app.route('/api/emotional/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotional state of text"""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    analysis = generator.emotional_intelligence.analyze_emotional_state(data['text'])
    return jsonify(analysis)

@app.route('/api/emotional/techniques', methods=['POST'])
def get_regulation_techniques():
    """Get emotional regulation techniques"""
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    
    emotion = data.get('emotion', 'anxiety')
    intensity = data.get('intensity', 5.0)
    
    techniques = generator.emotional_intelligence.suggest_regulation_techniques(emotion, intensity)
    return jsonify({
        'emotion': emotion,
        'intensity': intensity,
        'techniques': techniques
    })

@app.route('/api/crisis/check', methods=['POST'])
def check_crisis():
    """Check for crisis indicators in text"""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    analysis = generator.emotional_intelligence.analyze_emotional_state(data['text'])
    crisis_assessment = generator.emotional_intelligence.detect_crisis(data['text'], analysis)
    
    return jsonify(crisis_assessment)

@app.route('/api/data/upload', methods=['POST'])
def upload_data():
    """Upload dataset for analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if not file.filename or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    allowed_extensions = {'csv', 'xlsx', 'xls', 'json'}
    filename = secure_filename(file.filename)
    
    if not filename or '.' not in filename:
        return jsonify({'error': 'Invalid filename'}), 400
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        return jsonify({'error': 'File type not allowed. Use CSV, Excel, or JSON'}), 400
    
    filepath = os.path.join(data_analyzer.data_path, filename)
    file.save(filepath)
    
    result = data_analyzer.upload_dataset(filepath, filename)
    return jsonify(result)

@app.route('/api/data/analyze-text', methods=['POST'])
def analyze_text_data():
    """Analyze pasted text data"""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    result = data_analyzer.analyze_text_dataset(data['text'])
    return jsonify(result)

@app.route('/api/data/statistics', methods=['POST'])
def get_statistics():
    """Get basic statistics"""
    data = request.json
    columns = data.get('columns') if data else []
    result = data_analyzer.basic_statistics(columns if columns else [])
    return jsonify(result)

@app.route('/api/data/correlations', methods=['POST'])
def get_correlations():
    """Find correlations"""
    data = request.json
    threshold = data.get('threshold', 0.5) if data else 0.5
    result = data_analyzer.find_correlations(threshold)
    return jsonify(result)

@app.route('/api/data/anomalies', methods=['POST'])
def get_anomalies():
    """Detect anomalies"""
    data = request.json
    column = data.get('column') if data else None
    method = data.get('method', 'isolation_forest') if data else 'isolation_forest'
    result = data_analyzer.detect_anomalies(column, method)
    return jsonify(result)

@app.route('/api/data/patterns', methods=['POST'])
def get_patterns():
    """Detect patterns"""
    data = request.json
    if not data or 'column' not in data:
        return jsonify({'error': 'No column specified'}), 400
    
    result = data_analyzer.detect_patterns(data['column'])
    return jsonify(result)

@app.route('/api/data/visualize', methods=['POST'])
def create_visualization():
    """Create visualization"""
    data = request.json
    if not data or 'chart_type' not in data:
        return jsonify({'error': 'No chart type specified'}), 400
    
    chart_type = data['chart_type']
    columns = data.get('columns')
    result = data_analyzer.create_visualization(chart_type, columns)
    return jsonify(result)

@app.route('/api/data/insights', methods=['GET'])
def get_insights():
    """Get AI insights"""
    insights = data_analyzer.generate_insights()
    return jsonify({'insights': insights})

@app.route('/api/cymatic/visualize', methods=['POST'])
def visualize_cymatic_pattern():
    """Generate and visualize cymatic pattern for a frequency"""
    data = request.json
    if not data or 'frequency' not in data:
        return jsonify({'error': 'No frequency provided'}), 400
    
    frequency = float(data['frequency'])
    
    if hasattr(generator.cymatic, 'advanced_engine'):
        pattern = generator.cymatic.advanced_engine.generate_cymatic_pattern(frequency)
        metrics = generator.cymatic.advanced_engine.calculate_pattern_metrics(pattern)
        
        save_path = f"static/cymatic_{int(frequency)}hz.png"
        image_path = generator.cymatic.advanced_engine.visualize_pattern(pattern, save_path)
        
        return jsonify({
            'frequency': frequency,
            'metrics': metrics,
            'image_path': image_path,
            'pattern_shape': list(pattern.shape)
        })
    else:
        return jsonify({'error': 'Advanced cymatic engine not available'}), 503

@app.route('/api/cymatic/harmonics', methods=['POST'])
def analyze_harmonics():
    """Analyze harmonic series with cymatic patterns"""
    data = request.json
    if not data or 'base_frequency' not in data:
        return jsonify({'error': 'No base frequency provided'}), 400
    
    base_freq = float(data['base_frequency'])
    layers = int(data.get('layers', 5))
    
    if hasattr(generator.cymatic, 'advanced_engine'):
        result = generator.cymatic.advanced_engine.transform_with_harmonics(base_freq, layers)
        
        if hasattr(generator.cymatic, 'coupling_analyzer'):
            coupling_report = generator.cymatic.coupling_analyzer.generate_coupling_report(
                result['harmonics']
            )
            result['coupling_report'] = coupling_report
        
        result.pop('patterns', None)
        
        return jsonify(result)
    else:
        return jsonify({'error': 'Advanced cymatic engine not available'}), 503

@app.route('/api/games/generate', methods=['POST'])
def generate_dynamic_game():
    """
    Generate custom game from user description
    Uses Canvas System for build → test → deliver workflow
    """
    try:
        from src.dynamic_game_generator import get_game_generator
        from src.canvas_orchestrator import get_canvas_orchestrator
        
        data = request.json
        if not data or 'request' not in data:
            return jsonify({'error': 'Game request required'}), 400
        
        user_request = data['request']
        game_type = data.get('game_type')
        customization = data.get('customization')
        
        # Step 1: Create canvas session for game development
        orchestrator = get_canvas_orchestrator()
        canvas = orchestrator.create_session(
            title=f"Custom Game: {user_request[:50]}",
            description=f"Generating game based on user request"
        )
        
        # Step 2: Generate game using GPT-4o
        game_gen = get_game_generator()
        result = game_gen.generate_game(
            user_request=user_request,
            game_type=game_type,
            customization=customization
        )
        
        if not result.get('success'):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Generation failed'),
                'canvas_id': canvas.session_id
            }), 500
        
        # Step 3: Add game to canvas
        orchestrator.add_artifact(
            session_id=canvas.session_id,
            filename='game.html',
            content=result['html']
        )
        
        # Step 4: Get preview URL
        preview_url = orchestrator.get_preview_url(canvas.session_id)
        
        return jsonify({
            'success': True,
            'canvas_id': canvas.session_id,
            'preview_url': preview_url,
            'game_title': result['title'],
            'game_description': result['description'],
            'game_type': result['game_type'],
            'customization': result.get('customization', {}),
            'message': 'Game generated! MC AI is testing it now...'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/games/list', methods=['GET'])
def list_games():
    """List game generation capabilities (dynamic generation only)"""
    return jsonify({
        'message': 'MC AI generates custom games on demand!',
        'capabilities': [
            {'type': 'board', 'emoji': '🎲', 'examples': 'Tic-tac-toe, checkers, chess with custom themes'},
            {'type': 'arcade', 'emoji': '🕹️', 'examples': 'Snake, breakout, whack-a-mole with custom characters'},
            {'type': 'platformer', 'emoji': '🏃', 'examples': 'Mario-style games with custom heroes'},
            {'type': 'puzzle', 'emoji': '🧩', 'examples': 'Memory match, sliding puzzles with custom images'},
            {'type': 'racing', 'emoji': '🏎️', 'examples': 'Racing games with custom vehicles'},
            {'type': 'shooter', 'emoji': '🚀', 'examples': 'Space shooters with custom ships'},
            {'type': 'card', 'emoji': '🎴', 'examples': 'Card games with custom decks'}
        ],
        'how_to_use': 'Just describe the game you want! Example: "tic-tac-toe with unicorns vs poop emojis"',
        'endpoint': '/api/games/generate'
    })

@app.route('/api/privacy/consent', methods=['POST'])
def update_consent():
    """User updates their privacy preferences (GDPR Article 7)"""
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({'error': 'user_id required'}), 400
    
    user_id = data.get('user_id')
    result = privacy_manager.record_consent(user_id, data)
    
    return jsonify(result)

@app.route('/api/privacy/export', methods=['GET'])
def export_data():
    """User exports their data (GDPR Article 20 - Right to data portability)"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    result = privacy_manager.export_user_data(user_id)
    
    if result.get('success'):
        return jsonify(result)
    else:
        return jsonify(result), 500

@app.route('/api/privacy/delete', methods=['DELETE'])
def delete_data():
    """User requests data deletion (GDPR Article 17 - Right to erasure)"""
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({'error': 'user_id required'}), 400
    
    user_id = data.get('user_id')
    reason = data.get('reason')
    
    result = privacy_manager.delete_user_data(user_id, reason)
    
    return jsonify(result)

@app.route('/api/privacy/check', methods=['GET'])
def check_consent():
    """Check user's consent status"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    result = privacy_manager.check_consent(user_id)
    
    return jsonify(result)

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get detailed system metrics"""
    try:
        metrics = {
            'health': generator.monitor.get_health_status(),
            'endpoints': generator.monitor.get_endpoint_stats(),
            'cache': generator.knowledge_engine.get_cache_stats()
        }
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/knowledge/test', methods=['POST'])
def test_knowledge():
    """Test knowledge engine with a query"""
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Query required'}), 400
    
    try:
        result = generator.knowledge_engine.answer_query(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
@app.route('/api/conversation/history', methods=['GET'])
def get_conversation_history():
    """Get user's conversation history for frontend display"""
    user_id = request.args.get('user_id')
    limit = int(request.args.get('limit', 20))  # Increased for long conversations
    
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    # Get history and format for frontend
    history = conversation_memory.get_conversation_history(user_id, limit)
    
    # Transform to frontend format
    conversation = []
    for entry in history:
        conversation.append({
            'role': 'user',
            'content': entry['user_message'],
            'metadata': entry.get('metadata', {})
        })
        conversation.append({
            'role': 'assistant',
            'content': entry['ai_response'],
            'metadata': entry.get('metadata', {})
        })
    
    return jsonify({'conversation': conversation, 'count': len(history)})

@app.route('/api/conversation/timeline', methods=['GET'])
def get_emotional_timeline():
    """Get user's emotional timeline"""
    user_id = request.args.get('user_id')
    days = int(request.args.get('days', 7))
    
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    timeline = conversation_memory.get_emotional_timeline(user_id, days)
    return jsonify(timeline)

@app.route('/api/conversation/search', methods=['GET'])
def search_conversations():
    """Search user's conversation history"""
    user_id = request.args.get('user_id')
    query = request.args.get('query')
    limit = int(request.args.get('limit', 5))
    
    if not user_id or not query:
        return jsonify({'error': 'user_id and query required'}), 400
    
    results = conversation_memory.search_conversations(user_id, query, limit)
    return jsonify({'results': results, 'count': len(results)})

@app.route('/api/conversation/delete', methods=['POST'])
def delete_conversation():
    """Delete user's conversation history"""
    data = request.json or {}
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    try:
        conversation_memory.delete_user_data(user_id)
        return jsonify({'success': True, 'message': 'Conversation deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation/create_id', methods=['POST'])
def create_user_id():
    """Create anonymous user ID"""
    data = request.json or {}
    identifier = data.get('identifier') if data else None  # Optional
    
    user_id = conversation_memory.create_user_id(identifier or '')
    return jsonify({'user_id': user_id})

@app.route('/api/environment', methods=['GET'])
def check_environment():
    """Check if user is accessing from within Replit workspace"""
    try:
        # REPLIT_DEV_DOMAIN exists when in Replit workspace (development)
        # REPLIT_DEPLOYMENT is set to "1" when published (external access)
        is_replit_workspace = bool(os.getenv('REPLIT_DEV_DOMAIN')) and not os.getenv('REPLIT_DEPLOYMENT')
        
        return jsonify({
            'is_replit_workspace': is_replit_workspace,
            'environment': 'replit_workspace' if is_replit_workspace else 'external'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def save_feedback():
    """Save user feedback (thumbs up/down) for responses"""
    import psycopg2
    import json
    from datetime import datetime
    
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        
        message = data.get('message', '')
        rating = data.get('rating', '')
        metadata = data.get('metadata', {})
        
        if not rating or rating not in ['like', 'dislike']:
            return jsonify({'error': 'Invalid rating'}), 400
        
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO feedback (message, rating, metadata) VALUES (%s, %s, %s) RETURNING id",
            (message, rating, json.dumps(metadata))
        )
        
        result_row = cur.fetchone()
        feedback_id = result_row[0] if result_row else None
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'feedback_id': feedback_id,
            'message': 'Feedback saved successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload large documents for dataset analysis (up to 200MB)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file.filename or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get user_id from form data
        user_id = request.form.get('user_id')
        
        # Create upload directory with user subdirectory
        upload_dir = f'user_data/uploads/{user_id}' if user_id else 'user_data/uploads/anonymous'
        os.makedirs(upload_dir, exist_ok=True)
        
        # Secure filename and save
        filename = secure_filename(file.filename or 'upload')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(upload_dir, unique_filename)
        
        # Save file
        file.save(filepath)
        
        # Get file size
        file_size = os.path.getsize(filepath)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        # Process file based on type
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        result = {
            'success': True,
            'filename': filename,
            'size_mb': file_size_mb,
            'filepath': filepath,
            'file_type': file_ext,
            'message': f'✅ File uploaded successfully: {filename} ({file_size_mb}MB)'
        }
        
        # Extract content preview for different file types
        content_preview = None
        full_content = None
        
        try:
            # Text files - read full content
            if file_ext in ['txt', 'md', 'log', 'py', 'js', 'html', 'css', 'java', 'cpp', 'c', 'h']:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    full_content = f.read()
                    content_preview = full_content[:2000]  # First 2KB for preview
                    result['word_count'] = len(full_content.split())
                    result['line_count'] = full_content.count('\n')
            
            # JSON files - parse and preview
            elif file_ext == 'json':
                with open(filepath, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    full_content = json.dumps(json_data, indent=2)
                    content_preview = json.dumps(json_data, indent=2)[:2000]
                    result['json_keys'] = list(json_data.keys()) if isinstance(json_data, dict) else None
                    result['json_length'] = len(json_data) if isinstance(json_data, (list, dict)) else None
            
            # CSV files - read and preview
            elif file_ext == 'csv':
                import pandas as pd
                df = pd.read_csv(filepath)
                result['rows'] = len(df)
                result['columns'] = list(df.columns)
                result['column_count'] = len(df.columns)
                content_preview = df.head(10).to_string()
                full_content = df.to_string()
            
            # PDF files
            elif file_ext == 'pdf':
                result['message'] += '\n📕 PDF file detected. Text extraction available.'
                # PDF processing would go here
            
            if content_preview:
                result['content_preview'] = content_preview
                result['has_content'] = True
            
            if full_content and len(full_content) < 500000:  # < 500KB
                result['full_content'] = full_content
                
        except Exception as e:
            logger.warning(f"Content extraction error: {str(e)}")
            result['content_error'] = str(e)
        
        logger.info(f"✅ File uploaded: {filename} ({file_size_mb}MB) by user {user_id}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# FRAMEWORK MANAGEMENT API - Meta-Learning System
# ============================================================================

@app.route('/api/frameworks/list', methods=['GET'])
def list_frameworks():
    """Get all frameworks with their status"""
    try:
        from src.meta_learning.framework_registry import framework_registry
        
        all_frameworks = []
        for fid, manifest in framework_registry.manifests.items():
            framework = framework_registry.get_framework(fid)
            
            all_frameworks.append({
                'id': fid,
                'name': manifest.name,
                'description': manifest.description,
                'version': manifest.version,
                'creator': manifest.creator,
                'capabilities': manifest.capabilities,
                'dependencies': manifest.dependencies,
                'injection_point': manifest.injection_point,
                'priority': manifest.priority,
                'approved': framework_registry.is_approved(fid),
                'enabled': framework.enabled if framework else False,
                'stats': framework.get_stats() if framework else {}
            })
        
        return jsonify({
            'success': True,
            'frameworks': all_frameworks,
            'total': len(all_frameworks),
            'approved': len(framework_registry.get_approved_frameworks()),
            'pending': len(framework_registry.get_pending_frameworks())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/frameworks/<framework_id>', methods=['GET'])
def get_framework_details(framework_id):
    """Get detailed information about a specific framework"""
    try:
        from src.meta_learning.framework_registry import framework_registry
        
        manifest = framework_registry.get_manifest(framework_id)
        if not manifest:
            return jsonify({'error': 'Framework not found'}), 404
        
        framework = framework_registry.get_framework(framework_id)
        
        details = {
            'id': framework_id,
            'name': manifest.name,
            'description': manifest.description,
            'version': manifest.version,
            'creator': manifest.creator,
            'capabilities': manifest.capabilities,
            'dependencies': manifest.dependencies,
            'injection_point': manifest.injection_point,
            'priority': manifest.priority,
            'approved': framework_registry.is_approved(framework_id),
            'enabled': framework.enabled if framework else False,
            'stats': framework.get_stats() if framework else {},
            'metadata': framework.get_metadata() if framework else {}
        }
        
        return jsonify({'success': True, 'framework': details})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/frameworks/<framework_id>/approve', methods=['POST'])
def approve_framework(framework_id):
    """Approve a framework (requires admin)"""
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        admin_token = data.get('admin_token')
        
        # Verify admin access
        if not admin_config.is_admin(user_id, admin_token):
            return jsonify({'error': 'Admin access required'}), 403
        
        from src.meta_learning.framework_registry import framework_registry
        
        # Check if framework exists
        if not framework_registry.get_manifest(framework_id):
            return jsonify({'error': 'Framework not found'}), 404
        
        # Approve framework
        success = framework_registry.approve_framework(framework_id, approver=user_id or "Admin")
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Framework {framework_id} approved successfully',
                'framework_id': framework_id
            })
        else:
            return jsonify({'error': 'Failed to approve framework'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/frameworks/<framework_id>/reject', methods=['POST'])
def reject_framework(framework_id):
    """Reject/delete a framework (requires admin)"""
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        admin_token = data.get('admin_token')
        
        # Verify admin access
        if not admin_config.is_admin(user_id, admin_token):
            return jsonify({'error': 'Admin access required'}), 403
        
        from src.meta_learning.framework_registry import framework_registry
        from src.meta_learning.framework_loader import framework_loader
        
        # Check if framework exists
        if not framework_registry.get_manifest(framework_id):
            return jsonify({'error': 'Framework not found'}), 404
        
        # Unload and remove framework
        framework_loader.unload_framework(framework_id)
        
        return jsonify({
            'success': True,
            'message': f'Framework {framework_id} rejected and removed',
            'framework_id': framework_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/frameworks/<framework_id>/toggle', methods=['POST'])
def toggle_framework(framework_id):
    """Enable/disable a framework (requires admin)"""
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        admin_token = data.get('admin_token')
        enable = data.get('enable', True)
        
        # Verify admin access
        if not admin_config.is_admin(user_id, admin_token):
            return jsonify({'error': 'Admin access required'}), 403
        
        from src.meta_learning.framework_registry import framework_registry
        
        framework = framework_registry.get_framework(framework_id)
        if not framework:
            return jsonify({'error': 'Framework not found'}), 404
        
        # Check if approved
        if not framework_registry.is_approved(framework_id):
            return jsonify({'error': 'Cannot enable unapproved framework'}), 403
        
        if enable:
            framework.enable()
            status = 'enabled'
        else:
            framework.disable()
            status = 'disabled'
        
        return jsonify({
            'success': True,
            'message': f'Framework {framework_id} {status}',
            'framework_id': framework_id,
            'enabled': framework.enabled
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/frameworks/stats', methods=['GET'])
def get_framework_stats():
    """Get framework system statistics"""
    try:
        from src.meta_learning.framework_registry import framework_registry
        from src.meta_learning.framework_loader import framework_loader
        
        registry_stats = framework_registry.get_stats()
        loader_stats = framework_loader.get_load_status()
        
        return jsonify({
            'success': True,
            'registry': registry_stats,
            'loader': loader_stats,
            'summary': {
                'total_frameworks': registry_stats['total_frameworks'],
                'approved': registry_stats['approved_count'],
                'pending': registry_stats['pending_count'],
                'loaded': loader_stats['loaded_count'],
                'failed': loader_stats['failed_count']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# AUTONOMOUS UPDATE ENDPOINTS
# ============================================================================

@app.route('/api/autonomous-update', methods=['POST'])
@cross_origin(origins=[])  # SECURITY: Disable CORS - admin-only endpoint
def propose_autonomous_update():
    """Allow MC AI to propose and execute autonomous updates (ADMIN AUTHENTICATED)"""
    try:
        from src.autonomous_update_engine import autonomous_engine
        
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        
        # SECURITY: Require valid admin token (Mark only)
        # Cannot be spoofed - server-side secret verification
        admin_token = data.get('admin_token')
        if not admin_config.verify_admin_token(admin_token):
            return jsonify({
                'error': 'Unauthorized - valid admin token required for autonomous updates',
                'message': 'Autonomous updates require admin authentication'
            }), 403
        
        operation = data.get('operation')
        params = data.get('params', {})
        justification = data.get('justification', '')
        
        if not operation:
            return jsonify({'error': 'Operation required'}), 400
        
        if not justification:
            return jsonify({'error': 'Justification required'}), 400
        
        # Add timestamp to params
        from datetime import datetime
        params['timestamp'] = datetime.now().isoformat()
        params['justification'] = justification
        
        # Propose the update
        result = autonomous_engine.propose_update(operation, params, justification)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'Autonomous update applied: {operation}',
                'operation': operation,
                'details': result['details'],
                'justification': justification,
                'timestamp': result['timestamp']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error'],
                'operation': operation,
                'justification': justification
            }), 400
    
    except Exception as e:
        return jsonify({'error': f'Autonomous update failed: {str(e)}'}), 500

@app.route('/api/autonomous-stats', methods=['GET'])
def get_autonomous_stats():
    """Get autonomous update session statistics"""
    try:
        from src.autonomous_update_engine import autonomous_engine
        
        stats = autonomous_engine.get_session_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/autonomous-log', methods=['GET'])
def get_autonomous_log():
    """Get recent autonomous updates from log"""
    try:
        from src.autonomous_update_engine import autonomous_engine
        
        limit = request.args.get('limit', 10, type=int)
        updates = autonomous_engine.get_recent_updates(limit=limit)
        
        return jsonify({
            'success': True,
            'updates': updates,
            'count': len(updates)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/autonomous-reset', methods=['POST'])
@cross_origin(origins=[])  # SECURITY: Disable CORS - admin-only endpoint
def reset_autonomous_session():
    """Reset autonomous update session counters (ADMIN AUTHENTICATED)"""
    try:
        from src.autonomous_update_engine import autonomous_engine
        
        # SECURITY: Require valid admin token
        data = request.json or {}
        admin_token = data.get('admin_token') or ''
        
        if not admin_config.verify_admin_token(admin_token):
            return jsonify({'error': 'Unauthorized - admin token required'}), 403
        
        autonomous_engine.reset_session()
        
        return jsonify({
            'success': True,
            'message': 'Session counters reset'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Configure maximum upload size (200MB for datasets)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

# ==================== ASYNC LAZY-LOADING APIs ====================

@app.route('/api/cymatic/generate', methods=['POST'])
def generate_cymatic():
    """Async API for cymatic visualization generation"""
    try:
        data = request.json or {}
        frequency = data.get('frequency', 432)
        text = data.get('text', 'frequency analysis')
        
        result = generator.advanced_cymatics.analyze_frequency_profile(
            base_freq=float(frequency),
            text=text
        )
        
        return jsonify({
            'success': True,
            'analysis': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/art/generate', methods=['POST'])
def generate_art_async():
    """Async API for art generation"""
    try:
        data = request.json or {}
        prompt = data.get('prompt', 'abstract art')
        style = data.get('style', 'abstract')
        emotion = data.get('emotion', 'neutral')
        
        result = generator.art_generator.generate_art(
            user_request=prompt,
            style=style,
            emotion=emotion
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/music/generate', methods=['POST'])
def generate_music_async():
    """Async API for music generation"""
    try:
        data = request.json or {}
        emotion = data.get('emotion', 'calm')
        style = data.get('style', 'ambient')
        duration = data.get('duration', 30)
        
        result = generator.music_generator.generate_music(
            emotion=emotion,
            style=style,
            duration=duration
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/data/analyze', methods=['POST'])
def analyze_data_async():
    """Async API for data analysis"""
    try:
        data = request.json or {}
        dataset = data.get('dataset')
        analysis_type = data.get('type', 'insights')
        
        if not dataset:
            return jsonify({'error': 'No dataset provided'}), 400
        
        # Upload/load dataset
        data_analyzer.upload_dataset(file_path=dataset)
        
        if analysis_type == 'anomalies':
            result = data_analyzer.detect_anomalies(
                column=data.get('column'),
                method=data.get('method', 'isolation_forest')
            )
        elif analysis_type == 'patterns':
            column = data.get('column')
            if not column:
                return jsonify({'error': 'Column required for pattern detection'}), 400
            result = data_analyzer.detect_patterns(column=column)
        elif analysis_type == 'stats':
            columns = data.get('columns', [])
            result = data_analyzer.basic_statistics(columns=columns)
        else:
            result = data_analyzer.generate_insights()
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/emotion/analyze', methods=['POST'])
def analyze_emotion_async():
    """Async API for emotional intelligence analysis"""
    try:
        data = request.json or {}
        message = data.get('message', '')
        context = data.get('context')
        user_id = data.get('user_id')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        result = generator.emotional_intelligence.analyze_emotional_state(
            text=message,
            context=context,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'analysis': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/system/awareness', methods=['GET'])
def get_system_awareness():
    """
    Get MC AI's current system awareness
    Shows what MC AI knows about his own state
    """
    try:
        from src.system_awareness import get_system_awareness
        awareness = get_system_awareness()
        return jsonify({
            'success': True,
            'awareness': awareness
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'awareness': {
                'status': 'unknown',
                'message': 'System awareness not fully initialized yet'
            }
        }), 200  # Still return 200 to avoid breaking callers

@app.route('/api/wisdom/evaluate', methods=['POST'])
def evaluate_code_wisdom():
    """
    Evaluate code changes using MC AI's wisdom engine
    This gives MC AI the ability to know if code is helpful or not
    """
    try:
        from src.code_wisdom import evaluate_code_wisdom
        
        data = request.json or {}
        description = data.get('description', '')
        code_snippet = data.get('code_snippet')
        context = data.get('context', {})
        
        if not description:
            return jsonify({'error': 'No description provided'}), 400
        
        evaluation = evaluate_code_wisdom(description, code_snippet, context)
        
        return jsonify({
            'success': True,
            'evaluation': evaluation.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/wisdom/criteria', methods=['GET'])
def get_wisdom_criteria():
    """
    Get MC AI's wisdom criteria for evaluating changes
    Shows what MC AI values and how he makes decisions
    """
    try:
        from src.code_wisdom import get_wisdom_engine
        engine = get_wisdom_engine()
        criteria = engine.get_wisdom_summary()
        return jsonify({
            'success': True,
            'criteria': criteria
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/canvas/create', methods=['POST'])
def create_canvas():
    """Create a new canvas session for MC AI to build in"""
    try:
        from src.canvas_orchestrator import get_canvas_orchestrator
        
        data = request.json or {}
        title = data.get('title', 'Untitled Canvas')
        description = data.get('description', '')
        metadata = data.get('metadata', {})
        
        orchestrator = get_canvas_orchestrator()
        session = orchestrator.create_session(title, description, metadata)
        
        return jsonify({
            'success': True,
            'session': session.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/canvas/<session_id>/add', methods=['POST'])
def add_canvas_artifact(session_id):
    """Add code/asset to canvas session"""
    try:
        from src.canvas_orchestrator import get_canvas_orchestrator
        
        data = request.json or {}
        filename = data.get('filename')
        content = data.get('content')
        
        if not filename or not content:
            return jsonify({'error': 'Missing filename or content'}), 400
        
        orchestrator = get_canvas_orchestrator()
        success = orchestrator.add_artifact(session_id, filename, content)
        
        if not success:
            return jsonify({'error': 'Session not found'}), 404
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/canvas/preview/<session_id>/')
@app.route('/canvas/preview/<session_id>/<path:filename>')
def canvas_preview(session_id, filename='index.html'):
    """Serve canvas preview (MC AI's sandbox)"""
    try:
        from src.canvas_orchestrator import get_canvas_orchestrator
        import flask
        
        orchestrator = get_canvas_orchestrator()
        session = orchestrator.get_session(session_id)
        
        if not session:
            return "Canvas session not found", 404
        
        session_dir = orchestrator._get_session_dir(session_id)
        file_path = os.path.join(session_dir, filename)
        
        if not os.path.exists(file_path):
            return f"File not found: {filename}", 404
        
        return flask.send_from_directory(session_dir, filename)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/api/canvas/<session_id>/snapshot', methods=['POST'])
def canvas_snapshot(session_id):
    """Take screenshot of canvas preview (MC AI 'sees' what he built)"""
    try:
        from src.canvas_orchestrator import get_canvas_orchestrator, CanvasMode
        
        orchestrator = get_canvas_orchestrator()
        session = orchestrator.get_session(session_id)
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        orchestrator.set_mode(session_id, CanvasMode.TESTING, "Taking screenshot to verify")
        
        preview_url = orchestrator.get_preview_url(session_id)
        if not preview_url:
            return jsonify({'error': 'No preview available'}), 400
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'preview_url': preview_url,
            'message': 'Use screenshot tool with this preview_url'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/canvas/<session_id>/status', methods=['GET'])
def canvas_status(session_id):
    """Get canvas session status"""
    try:
        from src.canvas_orchestrator import get_canvas_orchestrator
        
        orchestrator = get_canvas_orchestrator()
        session = orchestrator.get_session(session_id)
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        return jsonify({
            'success': True,
            'session': session.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/admin/dashboard')
def admin_dashboard():
    """
    Production Admin Dashboard (AUTHENTICATION REQUIRED)
    Shows system health, performance metrics, and error logs
    """
    # SECURITY: FAIL CLOSED - Require valid admin token
    expected_token = os.environ.get('ADMIN_SECRET_TOKEN')
    provided_token = request.args.get('token')
    
    # Deny if no token is configured OR if provided token doesn't match
    if not expected_token or not provided_token or provided_token != expected_token:
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Access Denied</title></head>
        <body style="font-family: system-ui; padding: 40px; background: #0f0f0f; color: #fff; text-align: center;">
            <h1>🔒 Access Denied</h1>
            <p>Admin authentication required</p>
            <p style="font-size: 12px; color: #666; margin-top: 20px;">
                Admins: Access requires ?token=ADMIN_SECRET_TOKEN
            </p>
            <a href="/" style="color: #667eea;">← Back to Chat</a>
        </body>
        </html>
        """, 403
    
    try:
        health = generator.monitor.get_health_status()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MC AI - Production Dashboard</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
                    background: #0f0f0f;
                    color: #e8e8e8;
                    padding: 20px;
                }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                h1 {{
                    font-size: 32px;
                    margin-bottom: 8px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }}
                .subtitle {{ color: #888; margin-bottom: 32px; font-size: 14px; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 24px; }}
                .card {{
                    background: #1a1a1a;
                    border: 1px solid #2a2a2a;
                    border-radius: 12px;
                    padding: 24px;
                }}
                .card-title {{
                    font-size: 14px;
                    color: #888;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin-bottom: 16px;
                }}
                .metric {{
                    font-size: 36px;
                    font-weight: 600;
                    margin-bottom: 8px;
                }}
                .metric-label {{ font-size: 14px; color: #888; }}
                .status-good {{ color: #4caf50; }}
                .status-warning {{ color: #ff9800; }}
                .status-error {{ color: #f44336; }}
                .metric-row {{ display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #2a2a2a; }}
                .metric-row:last-child {{ border-bottom: none; }}
                .refresh-btn {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: 600;
                    margin-top: 20px;
                }}
                .refresh-btn:hover {{ opacity: 0.9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧠 MC AI Production Dashboard</h1>
                <p class="subtitle">Real-time system health and performance metrics</p>
                
                <div class="grid">
                    <div class="card">
                        <div class="card-title">System Status</div>
                        <div class="metric status-{health.get('status', 'unknown').lower()}">{health.get('status', 'unknown').upper()}</div>
                        <div class="metric-label">Overall Health</div>
                    </div>
                    
                    <div class="card">
                        <div class="card-title">Response Time</div>
                        <div class="metric">{health.get('performance', {}).get('avg_response_time_ms', 0):.0f}ms</div>
                        <div class="metric-label">Average (Last Minute)</div>
                    </div>
                    
                    <div class="card">
                        <div class="card-title">Request Rate</div>
                        <div class="metric">{health.get('performance', {}).get('requests_per_minute', 0):.0f}</div>
                        <div class="metric-label">Requests/Minute</div>
                    </div>
                </div>
                
                <div class="grid">
                    <div class="card">
                        <div class="card-title">System Resources</div>
                        <div class="metric-row">
                            <span>CPU Usage</span>
                            <span class="{'status-warning' if health.get('system_resources', {}).get('cpu_usage_percent', 0) > 70 else 'status-good'}">{health.get('system_resources', {}).get('cpu_usage_percent', 0):.1f}%</span>
                        </div>
                        <div class="metric-row">
                            <span>Memory Usage</span>
                            <span class="{'status-warning' if health.get('system_resources', {}).get('memory_usage_percent', 0) > 70 else 'status-good'}">{health.get('system_resources', {}).get('memory_usage_percent', 0):.1f}%</span>
                        </div>
                        <div class="metric-row">
                            <span>Disk Usage</span>
                            <span class="{'status-warning' if health.get('system_resources', {}).get('disk_usage_percent', 0) > 80 else 'status-good'}">{health.get('system_resources', {}).get('disk_usage_percent', 0):.1f}%</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-title">Performance Metrics</div>
                        <div class="metric-row">
                            <span>Total Requests</span>
                            <span>{health.get('performance', {}).get('total_requests', 0)}</span>
                        </div>
                        <div class="metric-row">
                            <span>Success Rate</span>
                            <span class="status-good">{health.get('performance', {}).get('success_rate', 100):.1f}%</span>
                        </div>
                        <div class="metric-row">
                            <span>Uptime</span>
                            <span>{health.get('uptime', {}).get('formatted', 'N/A')}</span>
                        </div>
                    </div>
                </div>
                
                <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Dashboard</button>
                <a href="/" style="margin-left: 12px; color: #667eea; text-decoration: none;">← Back to Chat</a>
            </div>
            
            <script>
                // Auto-refresh every 30 seconds
                setTimeout(() => location.reload(), 30000);
            </script>
        </body>
        </html>
        """
        return html
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Dashboard Error</title></head>
        <body style="font-family: system-ui; padding: 40px; background: #0f0f0f; color: #fff;">
            <h1>⚠️ Dashboard Unavailable</h1>
            <p>Error: {str(e)}</p>
            <a href="/" style="color: #667eea;">← Back to Chat</a>
        </body>
        </html>
        """, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
