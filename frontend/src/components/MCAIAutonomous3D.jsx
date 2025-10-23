import React, { useState, useEffect, useRef } from 'react';
import CuteMCAICharacter from './CuteMCAICharacter';

const MCAIAutonomous3D = () => {
  const [mcaiPosition, setMcaiPosition] = useState({ x: 50, y: 75 }); // Start near bottom
  const [mcaiRotation, setMcaiRotation] = useState(0);
  const [mcaiActivity, setMcaiActivity] = useState('idle');
  const [thoughtBubble, setThoughtBubble] = useState({ show: false, text: '' });
  const [currentBackground, setCurrentBackground] = useState('default');
  const [spawnedObjects, setSpawnedObjects] = useState([]); // NEW: Track spawned objects
  const [chatMessages, setChatMessages] = useState([
    { role: 'ai', text: "Hi there! I'm so happy to chat with you! What's on your mind today? 💜" }
  ]);
  const [userInput, setUserInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [isUserInteracting, setIsUserInteracting] = useState(false);
  const [showSettings, setShowSettings] = useState(false); // NEW: Toggle settings
  const [isFloating, setIsFloating] = useState(false); // NEW: Walking vs floating
  
  // Color customization
  const [mcaiColor, setMcaiColor] = useState(() => {
    const saved = localStorage.getItem('mcaiColor3D');
    return saved || '#9CA3AF'; // Default to grey robot
  });
  
  // Settings
  const [settings, setSettings] = useState({
    reduceMotion: false,
    showParticles: true
  });

  const roamingTimerRef = useRef(null);
  const thoughtTimerRef = useRef(null);

  const colorOptions = [
    { name: 'Grey', value: '#9CA3AF', emoji: '🤖' },
    { name: 'Purple', value: '#667eea', emoji: '💜' },
    { name: 'Pink', value: '#ec4899', emoji: '💗' },
    { name: 'Yellow', value: '#fbbf24', emoji: '💛' },
    { name: 'Green', value: '#10b981', emoji: '💚' },
    { name: 'Blue', value: '#3b82f6', emoji: '💙' },
    { name: 'Orange', value: '#f97316', emoji: '🧡' },
    { name: 'Red', value: '#ef4444', emoji: '❤️' }
  ];

  // Background presets
  const backgrounds = {
    default: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    space: 'url("https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?q=80&w=2071&auto=format&fit=crop")',
    forest: 'url("https://images.unsplash.com/photo-1448375240586-882707db8886?q=80&w=2070&auto=format&fit=crop")',
    ocean: 'url("https://images.unsplash.com/photo-1505142468610-359e7d316be0?q=80&w=2070&auto=format&fit=crop")',
    beach: 'url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2073&auto=format&fit=crop")',
    mountains: 'url("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=2070&auto=format&fit=crop")',
    sunset: 'url("https://images.unsplash.com/photo-1495567720989-cebdbdd97913?q=80&w=2070&auto=format&fit=crop")',
    city: 'url("https://images.unsplash.com/photo-1514565131-fce0801e5785?q=80&w=2056&auto=format&fit=crop")',
    calm: 'linear-gradient(135deg, #4a5568 0%, #2d3748 100%)',
    happy: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    focus: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)'
  };

  // Save color preference
  useEffect(() => {
    localStorage.setItem('mcaiColor3D', mcaiColor);
  }, [mcaiColor]);

  // Determine if MC AI should float based on background
  useEffect(() => {
    setIsFloating(currentBackground === 'space');
  }, [currentBackground]);

  // Roaming behavior when idle
  const roam = () => {
    if (settings.reduceMotion || isUserInteracting) return;
    
    const x = Math.random() * 80 + 10; // 10% to 90% horizontal
    const y = isFloating ? Math.random() * 60 + 20 : Math.random() * 10 + 70; // Stay at bottom when walking (70-80%), float in space
    const rotation = (Math.random() - 0.5) * 20;
    
    setMcaiPosition({ x, y });
    setMcaiRotation(rotation);
    setMcaiActivity(Math.random() > 0.7 ? 'fidgeting' : 'exploring');
    
    // Random thoughts while roaming
    if (Math.random() > 0.7) {
      const thoughts = [
        '💭',
        '✨',
        '🤔',
        '👀',
        'Where should I go next?',
        'This is nice!',
        'Hmm...'
      ];
      showThought(thoughts[Math.floor(Math.random() * thoughts.length)], 2000);
    }
    
    const nextRoam = Math.random() * 4000 + 3000; // 3-7 seconds
    roamingTimerRef.current = setTimeout(roam, nextRoam);
  };

  // Start roaming when component mounts
  useEffect(() => {
    // MC AI autonomously roams when idle!
    if (!isUserInteracting && !settings.reduceMotion) {
      roam();
    }
    return () => {
      if (roamingTimerRef.current) clearTimeout(roamingTimerRef.current);
    };
  }, [settings.reduceMotion, isUserInteracting, isFloating]);

  const showThought = (text, duration = 3000) => {
    setThoughtBubble({ show: true, text });
    if (thoughtTimerRef.current) clearTimeout(thoughtTimerRef.current);
    thoughtTimerRef.current = setTimeout(() => {
      setThoughtBubble({ show: false, text: '' });
    }, duration);
  };

  const focusOnUser = () => {
    if (roamingTimerRef.current) clearTimeout(roamingTimerRef.current);
    setIsUserInteracting(true);
    // Keep MC AI at bottom when user focuses
    setMcaiPosition({ x: 50, y: 75 });
    setMcaiRotation(0);
    setMcaiActivity('listening');
  };

  const returnToRoaming = () => {
    setTimeout(() => {
      setIsUserInteracting(false);
      roam();
    }, 1000);
  };

  // MC AI is now the autonomous director - he controls scene creation!

  // AUTONOMOUS BEHAVIOR CONTROLLER
  const autonomousBehavior = (action, objects) => {
    console.log(`🤖 MC AI autonomously decides to: ${action}`);
    
    // Parse action and choose behavior
    const actionLower = action.toLowerCase();
    
    if (actionLower.includes('eat') || actionLower.includes('food')) {
      setMcaiActivity('eating');
      // Find food object and move towards it
      const foodObj = objects.find(o => ['hotdog', 'pizza', 'burger', 'ice cream'].includes(o.name));
      if (foodObj) {
        setTimeout(() => {
          setMcaiPosition({ x: foodObj.x, y: foodObj.y + 5 });
          showThought('Yum! This looks delicious! 🌭', 3000);
        }, 500);
      }
    } else if (actionLower.includes('build') || actionLower.includes('sandcastle')) {
      setMcaiActivity('building');
      const castleObj = objects.find(o => o.name === 'sandcastle' || o.name === 'castle');
      if (castleObj) {
        setTimeout(() => {
          setMcaiPosition({ x: castleObj.x, y: castleObj.y + 5 });
          showThought('Let me build this! 🏰', 3000);
        }, 500);
      }
    } else if (actionLower.includes('wave') || actionLower.includes('hello')) {
      setMcaiActivity('waving');
      showThought('Hello there! 👋', 2500);
    } else if (actionLower.includes('pet') || actionLower.includes('unicorn') || actionLower.includes('animal')) {
      setMcaiActivity('happy');
      const animalObj = objects.find(o => ['unicorn', 'dragon', 'dog', 'cat'].includes(o.name));
      if (animalObj) {
        setTimeout(() => {
          setMcaiPosition({ x: animalObj.x - 10, y: animalObj.y });
          showThought('So cute! 💜', 3000);
        }, 500);
      }
    } else if (actionLower.includes('dance') || actionLower.includes('happy')) {
      setMcaiActivity('happy');
      showThought('This is amazing! ✨', 2500);
    } else if (actionLower.includes('explore') || actionLower.includes('look')) {
      setMcaiActivity('exploring');
      // Move to random object
      if (objects.length > 0) {
        const randomObj = objects[Math.floor(Math.random() * objects.length)];
        setTimeout(() => {
          setMcaiPosition({ x: randomObj.x, y: randomObj.y + 10 });
          showThought(`Wow! ${randomObj.emoji}`, 2500);
        }, 500);
      }
    } else {
      // Default: roam and explore
      setMcaiActivity('idle');
    }
    
    // Return to idle after action completes
    setTimeout(() => {
      setMcaiActivity('idle');
    }, 4000);
  };

  const sendMessage = async () => {
    if (!userInput.trim()) return;
    
    const message = userInput.trim();
    setUserInput('');
    setChatMessages(prev => [...prev, { role: 'user', text: message }]);
    
    setIsThinking(true);
    setMcaiActivity('thinking');
    showThought('Let me imagine something...', 2000);
    
    try {
      // MC AI AUTONOMOUS DIRECTOR - MC AI controls everything!
      const response = await fetch('/api/mcai-autonomous-director', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          conversation_history: chatMessages
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        // MC AI decided what background to use
        if (data.background && data.background !== 'default') {
          setCurrentBackground(data.background);
        }
        
        // MC AI decided if subject changed (clear old objects)
        if (data.subject_changed) {
          console.log('🔄 MC AI says: Subject changed! Starting fresh...');
          setSpawnedObjects([]);
        }
        
        // MC AI spawned objects from HIS imagination
        if (data.objects && data.objects.length > 0) {
          setSpawnedObjects(prev => [...prev, ...data.objects]);
          console.log('✨ MC AI created:', data.objects.map(o => o.emoji).join(' '));
        }
        
        // MC AI decided what HE wants to do
        if (data.mc_ai_action) {
          autonomousBehavior(data.mc_ai_action, data.objects || []);
        }
        
        // MC AI's thought bubble
        if (data.thought) {
          showThought(data.thought, 3000);
        }
        
        // MC AI's response
        setIsThinking(false);
        setChatMessages(prev => [...prev, { 
          role: 'ai', 
          text: data.response || "I'm here with you! Let's create something amazing! 💜" 
        }]);
        
        setMcaiActivity('happy');
        
        setTimeout(() => {
          if (!isUserInteracting) {
            setMcaiActivity('idle');
          }
        }, 3000);
      } else {
        throw new Error(data.error || 'Unknown error');
      }
      
    } catch (error) {
      console.error('MC AI Autonomous Director error:', error);
      setIsThinking(false);
      setChatMessages(prev => [...prev, { 
        role: 'ai', 
        text: "Oops! Let me try that again! I'm still here with you! 💜" 
      }]);
    }
  };

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      overflow: 'hidden',
      position: 'relative',
      fontFamily: '"Comic Neue", cursive, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      {/* Dynamic Background */}
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: backgrounds[currentBackground],
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        transition: 'background 1.5s ease-in-out',
        zIndex: 0
      }} />
      
      {/* Gradient Overlay for Text Readability */}
      <div style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        width: '100%',
        height: '40%',
        background: 'linear-gradient(to top, rgba(0,0,0,0.7), rgba(0,0,0,0))',
        pointerEvents: 'none',
        zIndex: 1
      }} />

      {/* Spawned Objects Layer */}
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: 2
      }}>
        {spawnedObjects.map((obj, idx) => (
          <div
            key={idx}
            style={{
              position: 'absolute',
              left: `${obj.x}%`,
              top: `${obj.y}%`,
              fontSize: obj.type === 'rainbow' ? '120px' : obj.type === 'sun' || obj.type === 'moon' ? '80px' : '60px',
              transform: 'translate(-50%, -50%)',
              animation: obj.type === 'butterfly' || obj.type === 'bird' ? 'floatAround 10s ease-in-out infinite' : 
                         obj.type === 'cloud' ? 'driftSlow 30s linear infinite' : 'none',
              filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.3))'
            }}
          >
            {obj.emoji}
          </div>
        ))}
      </div>

      {/* BOXY MC AI CHARACTER - Full-screen positioning container */}
      <div style={{ 
        position: 'fixed', 
        top: 0, 
        left: 0, 
        width: '100%', 
        height: '100%', 
        pointerEvents: 'none',
        zIndex: 3 
      }}>
        <CuteMCAICharacter
          position={mcaiPosition}
          activity={mcaiActivity}
          emotion={isThinking ? 'thinking' : 'happy'}
          color={mcaiColor}
          scale={1}
        />
      </div>

      {/* Thought Bubble */}
      {thoughtBubble.show && (
        <div style={{
          position: 'fixed',
          left: `${mcaiPosition.x}%`,
          top: `calc(${mcaiPosition.y}% - 140px)`,
          transform: 'translateX(-50%)',
          background: 'white',
          color: '#1a202c',
          padding: '12px 18px',
          borderRadius: '20px',
          maxWidth: '280px',
          fontSize: '16px',
          fontWeight: '600',
          boxShadow: '0 4px 15px rgba(0,0,0,0.3)',
          zIndex: 50,
          opacity: 1,
          transition: 'opacity 0.3s ease-out',
          animation: 'thoughtBubbleFloat 0.3s ease-out'
        }}>
          {thoughtBubble.text}
          <div style={{
            position: 'absolute',
            bottom: '-10px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: 0,
            height: 0,
            borderLeft: '15px solid transparent',
            borderRight: '15px solid transparent',
            borderTop: '15px solid white'
          }} />
        </div>
      )}

      {/* MC AI Chat Bubble - Above His Head! */}
      {chatMessages.length > 1 && chatMessages[chatMessages.length - 1].role === 'ai' && (
        <div style={{
          position: 'fixed',
          left: `${mcaiPosition.x}%`,
          top: `${Math.max(mcaiPosition.y - 15, 5)}%`,
          transform: 'translate(-50%, -100%)',
          zIndex: 90,
          maxWidth: '85%',
          width: 'auto',
          animation: 'chatBubbleSlideIn 0.3s ease-out'
        }}>
          <div style={{
            background: 'rgba(255, 255, 255, 0.95)',
            color: '#1a202c',
            padding: '12px 20px',
            borderRadius: '20px',
            fontSize: '14px',
            lineHeight: '1.4',
            backdropFilter: 'blur(10px)',
            boxShadow: '0 4px 20px rgba(0,0,0,0.25)',
            textAlign: 'center',
            maxHeight: '120px',
            overflowY: 'auto',
            wordWrap: 'break-word'
          }}>
            {chatMessages[chatMessages.length - 1].text}
          </div>
          {/* Pointer arrow pointing down to MC AI */}
          <div style={{
            position: 'absolute',
            bottom: '-8px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: 0,
            height: 0,
            borderLeft: '10px solid transparent',
            borderRight: '10px solid transparent',
            borderTop: '10px solid rgba(255, 255, 255, 0.95)'
          }} />
        </div>
      )}

      {/* Chat Interface - Input at Bottom */}
      <div style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 100,
        padding: '24px',
        maxWidth: '800px',
        margin: '0 auto'
      }}>

        {/* Input Area */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          width: '100%'
        }}>
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onFocus={focusOnUser}
            onBlur={returnToRoaming}
            placeholder="Ask anything..."
            style={{
              flex: 1,
              padding: '16px 20px',
              borderRadius: '999px',
              border: 'none',
              background: 'rgba(20, 20, 20, 0.8)',
              backdropFilter: 'blur(10px)',
              color: 'white',
              fontSize: '16px',
              outline: 'none',
              boxShadow: '0 5px 20px rgba(0,0,0,0.5)',
              minWidth: 0
            }}
          />
          <button
            onClick={sendMessage}
            disabled={!userInput.trim()}
            style={{
              padding: '16px',
              borderRadius: '50%',
              border: 'none',
              background: 'linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%)',
              color: 'white',
              cursor: userInput.trim() ? 'pointer' : 'not-allowed',
              width: '56px',
              height: '56px',
              minWidth: '56px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 15px rgba(255, 126, 95, 0.4)',
              transition: 'opacity 0.2s',
              opacity: userInput.trim() ? 1 : 0.6,
              flexShrink: 0
            }}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </div>
      </div>

      {/* Top Controls: Home + Settings */}
      <div style={{
        position: 'fixed',
        top: '16px',
        left: '16px',
        zIndex: 200,
        display: 'flex',
        gap: '8px'
      }}>
        {/* Home Button */}
        <button
          onClick={() => window.location.href = '/'}
          style={{
            width: '40px',
            height: '40px',
            borderRadius: '8px',
            border: 'none',
            background: 'rgba(0,0,0,0.6)',
            backdropFilter: 'blur(10px)',
            color: 'white',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '20px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
            transition: 'background 0.2s'
          }}
          onMouseEnter={(e) => e.target.style.background = 'rgba(0,0,0,0.8)'}
          onMouseLeave={(e) => e.target.style.background = 'rgba(0,0,0,0.6)'}
          title="Return to Main Chat"
        >
          🏠
        </button>
        
        {/* Settings Button */}
        <button
          onClick={() => setShowSettings(!showSettings)}
          style={{
            width: '40px',
            height: '40px',
            borderRadius: '8px',
            border: 'none',
            background: 'rgba(0,0,0,0.6)',
            backdropFilter: 'blur(10px)',
            color: 'white',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '20px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
            transition: 'transform 0.2s, background 0.2s',
            transform: showSettings ? 'rotate(90deg)' : 'rotate(0deg)'
          }}
          onMouseEnter={(e) => e.target.style.background = 'rgba(0,0,0,0.8)'}
          onMouseLeave={(e) => e.target.style.background = 'rgba(0,0,0,0.6)'}
        >
          ⚙️
        </button>

        {/* Settings Dropdown */}
        {showSettings && (
          <div style={{
            position: 'absolute',
            top: '48px',
            left: '0',
            background: 'rgba(0,0,0,0.85)',
            backdropFilter: 'blur(15px)',
            padding: '16px',
            borderRadius: '12px',
            color: 'white',
            fontSize: '13px',
            minWidth: '200px',
            boxShadow: '0 8px 24px rgba(0,0,0,0.4)',
            animation: 'settingsFadeIn 0.2s ease-out'
          }}>
            <div style={{ fontWeight: 'bold', marginBottom: '12px', fontSize: '14px' }}>Settings</div>
            
            <label style={{ display: 'block', marginBottom: '10px', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={settings.reduceMotion}
                onChange={(e) => setSettings({...settings, reduceMotion: e.target.checked})}
                style={{ marginRight: '8px' }}
              />
              Reduce Motion
            </label>
            
            <label style={{ display: 'block', marginBottom: '16px', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={settings.showParticles}
                onChange={(e) => setSettings({...settings, showParticles: e.target.checked})}
                style={{ marginRight: '8px' }}
              />
              Show Particles
            </label>
            
            <div style={{ borderTop: '1px solid rgba(255,255,255,0.2)', paddingTop: '12px' }}>
              <div style={{ fontWeight: 'bold', marginBottom: '10px' }}>🎨 Robot Color</div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '8px' }}>
                {colorOptions.map((color) => (
                  <button
                    key={color.value}
                    onClick={() => setMcaiColor(color.value)}
                    title={color.name}
                    style={{
                      width: '36px',
                      height: '36px',
                      borderRadius: '6px',
                      border: mcaiColor === color.value ? '3px solid white' : '2px solid rgba(255,255,255,0.3)',
                      background: color.value,
                      cursor: 'pointer',
                      fontSize: '16px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      transition: 'transform 0.2s',
                      transform: mcaiColor === color.value ? 'scale(1.1)' : 'scale(1)'
                    }}
                  >
                    {color.emoji}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={() => setSpawnedObjects([])}
              style={{
                marginTop: '12px',
                width: '100%',
                padding: '8px',
                borderRadius: '6px',
                border: 'none',
                background: 'rgba(239, 68, 68, 0.8)',
                color: 'white',
                cursor: 'pointer',
                fontSize: '12px',
                fontWeight: 'bold'
              }}
            >
              🗑️ Clear Objects
            </button>
          </div>
        )}
      </div>

      {/* Global Styles */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');
        
        @keyframes thoughtBubbleFloat {
          from {
            opacity: 0;
            transform: translateX(-50%) scale(0.8) translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateX(-50%) scale(1) translateY(0px);
          }
        }
        
        @keyframes floatAround {
          0%, 100% {
            transform: translate(-50%, -50%) translateX(0px) translateY(0px);
          }
          25% {
            transform: translate(-50%, -50%) translateX(20px) translateY(-15px);
          }
          50% {
            transform: translate(-50%, -50%) translateX(-10px) translateY(-25px);
          }
          75% {
            transform: translate(-50%, -50%) translateX(-20px) translateY(-10px);
          }
        }
        
        @keyframes driftSlow {
          from {
            transform: translate(-50%, -50%) translateX(0);
          }
          to {
            transform: translate(-50%, -50%) translateX(100vw);
          }
        }
        
        @keyframes settingsFadeIn {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        @keyframes chatBubbleSlideIn {
          from {
            opacity: 0;
            transform: translate(-50%, -100%) scale(0.9);
          }
          to {
            opacity: 1;
            transform: translate(-50%, -100%) scale(1);
          }
        }
        
        /* Respect reduce motion preference */
        @media (prefers-reduced-motion: reduce) {
          * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
          }
        }
      `}</style>
    </div>
  );
};

export default MCAIAutonomous3D;
