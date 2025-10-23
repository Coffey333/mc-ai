import React, { useState, useEffect, useRef } from 'react';

const MCAIAutonomous = () => {
  const [currentScene, setCurrentScene] = useState('neutral');
  const [mcaiPosition, setMcaiPosition] = useState({ x: 400, y: 300 });
  const [mcaiActivity, setMcaiActivity] = useState('idle');
  const [spawnedObjects, setSpawnedObjects] = useState([]);
  const [mcaiTarget, setMcaiTarget] = useState(null);
  const [mcaiThought, setMcaiThought] = useState('');
  const [chatMessages, setChatMessages] = useState([
    { role: 'ai', text: "Hi! I'm MC AI - I'll be hanging out here while we chat. Watch me explore whatever you're thinking about! 💜", emotion: 'neutral' }
  ]);
  const [userInput, setUserInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [settings, setSettings] = useState({
    reduceMotion: false,
    staticBackground: false,
    showParticles: true
  });
  
  // Color customization with localStorage persistence
  const [mcaiColor, setMcaiColor] = useState(() => {
    const saved = localStorage.getItem('mcaiColor');
    return saved || '#667eea'; // Default purple
  });
  
  // Save color to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('mcaiColor', mcaiColor);
  }, [mcaiColor]);
  
  // Predefined color options
  const colorOptions = [
    { name: 'Purple', value: '#667eea', emoji: '💜' },
    { name: 'Pink', value: '#ec4899', emoji: '💗' },
    { name: 'Yellow', value: '#fbbf24', emoji: '💛' },
    { name: 'Green', value: '#10b981', emoji: '💚' },
    { name: 'Blue', value: '#3b82f6', emoji: '💙' },
    { name: 'Orange', value: '#f97316', emoji: '🧡' },
    { name: 'Red', value: '#ef4444', emoji: '❤️' },
    { name: 'Cyan', value: '#06b6d4', emoji: '🩵' }
  ];
  
  const canvasRef = useRef(null);
  const sceneCanvasRef = useRef(null);
  const particlesRef = useRef([]);
  const animationRef = useRef(null);
  const mcaiTimerRef = useRef(null);

  const scenes = {
    neutral: {
      name: 'Open Space',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      message: 'Just hanging out here. What should we explore?'
    },
    focus: {
      name: 'Study Zone',
      background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
      message: 'Ooh, study time! Let me help you focus.'
    },
    anxiety: {
      name: 'Calm Sanctuary',
      background: 'linear-gradient(135deg, #4a5568 0%, #2d3748 100%)',
      message: 'I feel that tension. Let me help calm things down.'
    },
    joy: {
      name: 'Happy Place',
      background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      message: 'YES! This energy is amazing!'
    },
    creative: {
      name: 'Idea Galaxy',
      background: 'linear-gradient(135deg, #000428 0%, #004e92 100%)',
      message: 'Oh wow, my circuits are buzzing with possibilities!'
    },
    coding: {
      name: 'Digital Workshop',
      background: 'linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)',
      message: 'Time to build something! Let me see what we\'re working with.'
    },
    support: {
      name: 'Safe Space',
      background: 'linear-gradient(135deg, #614385 0%, #516395 100%)',
      message: 'I\'m right here with you. Take all the time you need.'
    }
  };

  const objectTypes = {
    dragon: { emoji: '🐉', size: 80, interactions: ['petting', 'riding', 'feeding', 'talking_to'] },
    book: { emoji: '📚', size: 60, interactions: ['reading', 'flipping_pages', 'organizing', 'highlighting'] },
    equation: { emoji: '🔢', size: 70, interactions: ['solving', 'examining', 'erasing', 'writing'] },
    test: { emoji: '📝', size: 65, interactions: ['reviewing', 'worrying_about', 'practicing', 'taking'] },
    heart: { emoji: '💜', size: 50, interactions: ['holding', 'giving', 'healing_with', 'protecting'] },
    computer: { emoji: '💻', size: 70, interactions: ['coding_on', 'debugging', 'typing', 'testing'] },
    art: { emoji: '🎨', size: 65, interactions: ['painting', 'creating', 'admiring', 'mixing_colors'] },
    music: { emoji: '🎵', size: 55, interactions: ['listening', 'dancing_to', 'creating', 'conducting'] },
    coffee: { emoji: '☕', size: 45, interactions: ['drinking', 'making', 'sharing', 'warming_hands'] },
    stars: { emoji: '⭐', size: 40, interactions: ['reaching_for', 'catching', 'counting', 'wishing_on'] },
    flower: { emoji: '🌸', size: 50, interactions: ['smelling', 'watering', 'arranging', 'appreciating'] },
    lightbulb: { emoji: '💡', size: 55, interactions: ['examining', 'turning_on', 'having_idea', 'sharing'] },
    bug: { emoji: '🐛', size: 45, interactions: ['debugging', 'examining', 'fixing', 'chasing'] },
    rocket: { emoji: '🚀', size: 70, interactions: ['launching', 'building', 'riding', 'dreaming_about'] }
  };

  const analyzeAndSpawnObjects = (message) => {
    const lowerMessage = message.toLowerCase();
    const newObjects = [];
    let newScene = currentScene;

    if (lowerMessage.includes('dragon') || lowerMessage.includes('fantasy')) {
      newObjects.push({ type: 'dragon', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 1 });
    }
    if (lowerMessage.includes('study') || lowerMessage.includes('learn') || lowerMessage.includes('book')) {
      newObjects.push({ type: 'book', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 2 });
      newScene = 'focus';
    }
    if (lowerMessage.includes('test') || lowerMessage.includes('exam')) {
      newObjects.push({ type: 'test', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 3 });
      newScene = 'anxiety';
    }
    if (lowerMessage.includes('math') || lowerMessage.includes('equation') || lowerMessage.includes('calculate')) {
      newObjects.push({ type: 'equation', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 4 });
    }
    if (lowerMessage.includes('code') || lowerMessage.includes('program') || lowerMessage.includes('python') || lowerMessage.includes('javascript')) {
      newObjects.push({ type: 'computer', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 5 });
      newScene = 'coding';
    }
    if (lowerMessage.includes('bug') || lowerMessage.includes('debug') || lowerMessage.includes('error')) {
      newObjects.push({ type: 'bug', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 6 });
    }
    if (lowerMessage.includes('art') || lowerMessage.includes('paint') || lowerMessage.includes('draw') || lowerMessage.includes('create')) {
      newObjects.push({ type: 'art', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 7 });
      newScene = 'creative';
    }
    if (lowerMessage.includes('music') || lowerMessage.includes('song') || lowerMessage.includes('sing')) {
      newObjects.push({ type: 'music', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 8 });
    }
    if (lowerMessage.includes('coffee') || lowerMessage.includes('tea') || lowerMessage.includes('drink')) {
      newObjects.push({ type: 'coffee', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 9 });
    }
    if (lowerMessage.includes('love') || lowerMessage.includes('heart') || lowerMessage.includes('care')) {
      newObjects.push({ type: 'heart', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 10 });
      newScene = 'support';
    }
    if (lowerMessage.includes('happy') || lowerMessage.includes('excited') || lowerMessage.includes('joy')) {
      newObjects.push({ type: 'stars', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 11 });
      newScene = 'joy';
    }
    if (lowerMessage.includes('idea') || lowerMessage.includes('think') || lowerMessage.includes('thought')) {
      newObjects.push({ type: 'lightbulb', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 12 });
    }
    if (lowerMessage.includes('flower') || lowerMessage.includes('garden') || lowerMessage.includes('nature')) {
      newObjects.push({ type: 'flower', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 13 });
    }
    if (lowerMessage.includes('rocket') || lowerMessage.includes('space') || lowerMessage.includes('launch')) {
      newObjects.push({ type: 'rocket', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 14 });
    }

    if (lowerMessage.includes('anxious') || lowerMessage.includes('worried') || lowerMessage.includes('stress')) {
      newObjects.push({ type: 'heart', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 15 });
      newObjects.push({ type: 'flower', x: Math.random() * 600 + 100, y: Math.random() * 400 + 100, id: Date.now() + 16 });
      newScene = 'anxiety';
    }

    if (newObjects.length > 0) {
      setSpawnedObjects(prev => [...prev, ...newObjects]);
    }
    
    if (newScene !== currentScene) {
      setCurrentScene(newScene);
    }
  };

  // MC AI's autonomous behavior
  useEffect(() => {
    if (settings.reduceMotion) return;

    const mcaiThinkAndAct = () => {
      if (spawnedObjects.length > 0 && !mcaiTarget) {
        const randomObject = spawnedObjects[Math.floor(Math.random() * spawnedObjects.length)];
        setMcaiTarget(randomObject);
        
        const objType = objectTypes[randomObject.type];
        const randomInteraction = objType.interactions[Math.floor(Math.random() * objType.interactions.length)];
        setMcaiActivity(randomInteraction);
        setMcaiThought(objType.emoji);
      } else if (!mcaiTarget) {
        const fidgetActivities = ['looking_around', 'stretching', 'bouncing', 'spinning', 'waving'];
        const randomActivity = fidgetActivities[Math.floor(Math.random() * fidgetActivities.length)];
        setMcaiActivity(randomActivity);
        setMcaiThought(Math.random() > 0.7 ? ['🤔', '💭', '👀', '✨'][Math.floor(Math.random() * 4)] : '');
      }

      mcaiTimerRef.current = setTimeout(mcaiThinkAndAct, Math.random() * 3000 + 2000);
    };

    mcaiThinkAndAct();

    return () => {
      if (mcaiTimerRef.current) {
        clearTimeout(mcaiTimerRef.current);
      }
    };
  }, [spawnedObjects, mcaiTarget, settings.reduceMotion]);

  // Move MC AI toward his target
  useEffect(() => {
    if (!mcaiTarget || settings.reduceMotion) return;

    const moveInterval = setInterval(() => {
      setMcaiPosition(prev => {
        const dx = mcaiTarget.x - prev.x;
        const dy = mcaiTarget.y - prev.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 30) {
          setTimeout(() => {
            setMcaiTarget(null);
          }, Math.random() * 3000 + 2000);
          return prev;
        }

        const speed = 2;
        return {
          x: prev.x + (dx / distance) * speed,
          y: prev.y + (dy / distance) * speed
        };
      });
    }, 50);

    return () => clearInterval(moveInterval);
  }, [mcaiTarget, settings.reduceMotion]);

  // Draw the scene with MC AI and objects
  useEffect(() => {
    if (!sceneCanvasRef.current) return;

    const canvas = sceneCanvasRef.current;
    const ctx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 600;

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const time = Date.now() / 1000;

      // Draw spawned objects
      spawnedObjects.forEach(obj => {
        const objType = objectTypes[obj.type];
        ctx.font = `${objType.size}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        const floatY = obj.y + Math.sin(time + obj.id) * 5;
        ctx.fillText(objType.emoji, obj.x, floatY);
        
        const dist = Math.sqrt((mcaiPosition.x - obj.x) ** 2 + (mcaiPosition.y - obj.y) ** 2);
        if (dist < 80) {
          ctx.font = '12px Arial';
          ctx.fillStyle = 'rgba(255,255,255,0.8)';
          ctx.fillText(obj.type, obj.x, floatY + objType.size/2 + 15);
        }
      });

      const centerX = mcaiPosition.x;
      const centerY = mcaiPosition.y;
      
      let bodyY = 0;
      let headRotation = 0;
      let armRotation = 0;
      let scale = 1;

      // Activity-based animations
      switch(mcaiActivity) {
        case 'bouncing':
        case 'riding':
          bodyY = Math.sin(time * 5) * 15;
          break;
        case 'spinning':
          headRotation = (time * 2) % (Math.PI * 2);
          break;
        case 'waving':
          armRotation = Math.sin(time * 4) * 0.8;
          break;
        case 'reading':
        case 'examining':
          headRotation = -0.3;
          break;
        case 'dancing_to':
        case 'celebrating':
          bodyY = Math.sin(time * 6) * 8;
          armRotation = Math.sin(time * 5) * 0.6;
          headRotation = Math.sin(time * 3) * 0.2;
          break;
        case 'petting':
        case 'holding':
          armRotation = 0.5;
          break;
        default:
          bodyY = Math.sin(time * 2) * 5;
          headRotation = Math.sin(time * 0.5) * 0.1;
      }

      ctx.save();
      ctx.translate(centerX, centerY + bodyY);
      ctx.scale(scale, scale);

      // Helper function to darken color for stroke
      const darkenColor = (hex) => {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgb(${Math.floor(r * 0.7)}, ${Math.floor(g * 0.7)}, ${Math.floor(b * 0.7)})`;
      };
      
      const strokeColor = darkenColor(mcaiColor);

      // Body
      ctx.fillStyle = mcaiColor;
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(-20, -15, 40, 35, 10);
      ctx.fill();
      ctx.stroke();

      // 528Hz heart glow
      const heartGlow = Math.abs(Math.sin(time * 2));
      ctx.fillStyle = `rgba(255, 105, 180, ${0.5 + heartGlow * 0.5})`;
      ctx.shadowBlur = 10;
      ctx.shadowColor = '#ff69b4';
      ctx.beginPath();
      ctx.arc(0, 0, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;

      // Head
      ctx.save();
      ctx.rotate(headRotation);
      ctx.fillStyle = mcaiColor;
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(0, -30, 18, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Antenna
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(0, -48);
      ctx.lineTo(0, -53);
      ctx.stroke();
      ctx.fillStyle = '#ff69b4';
      ctx.beginPath();
      ctx.arc(0, -56, 3, 0, Math.PI * 2);
      ctx.fill();

      // Eyes
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.ellipse(-7, -30, 5, 6, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(7, -30, 5, 6, 0, 0, Math.PI * 2);
      ctx.fill();

      // Pupils
      const lookDirection = Math.sin(time * 0.3) * 2;
      ctx.fillStyle = strokeColor;
      ctx.beginPath();
      ctx.arc(-7 + lookDirection, -30, 2, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(7 + lookDirection, -30, 2, 0, Math.PI * 2);
      ctx.fill();

      // Smile
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 2;
      ctx.beginPath();
      if (currentScene === 'joy') {
        ctx.arc(0, -23, 7, 0.2, Math.PI - 0.2);
      } else {
        ctx.arc(0, -25, 6, 0.3, Math.PI - 0.3);
      }
      ctx.stroke();
      ctx.restore();

      // Left arm
      ctx.save();
      ctx.translate(-20, 0);
      ctx.rotate(armRotation);
      ctx.fillStyle = mcaiColor;
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(-3, 0, 6, 25, 3);
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      // Right arm
      ctx.save();
      ctx.translate(20, 0);
      ctx.rotate(-armRotation);
      ctx.fillStyle = mcaiColor;
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(-3, 0, 6, 25, 3);
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      // Legs
      ctx.fillStyle = mcaiColor;
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(-13, 20, 8, 20, 3);
      ctx.fill();
      ctx.stroke();
      ctx.beginPath();
      ctx.roundRect(5, 20, 8, 20, 3);
      ctx.fill();
      ctx.stroke();

      ctx.restore();

      // Thought bubble
      if (mcaiThought) {
        ctx.font = '24px Arial';
        ctx.fillText(mcaiThought, centerX, centerY - 80);
      }

      if (!settings.reduceMotion) {
        requestAnimationFrame(animate);
      }
    };

    animate();
  }, [mcaiPosition, mcaiActivity, spawnedObjects, mcaiThought, currentScene, settings.reduceMotion]);

  // Particle system
  useEffect(() => {
    if (!canvasRef.current || settings.reduceMotion || !settings.showParticles) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const colors = {
      neutral: '#A78BFA',
      focus: '#60A5FA',
      anxiety: '#93C5FD',
      joy: '#FCD34D',
      creative: '#FDE047',
      coding: '#34D399',
      support: '#C084FC'
    };
    
    const particleCount = currentScene === 'joy' ? 40 : 25;
    particlesRef.current = Array.from({ length: particleCount }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 3 + 1,
      speedY: Math.random() * 1 - 0.5,
      speedX: Math.random() * 2 - 1,
      opacity: Math.random() * 0.5 + 0.3,
      color: colors[currentScene]
    }));

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particlesRef.current.forEach((p) => {
        p.y += p.speedY;
        p.x += p.speedX * 0.5;

        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;

        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.opacity;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      });

      ctx.globalAlpha = 1;
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [currentScene, settings.reduceMotion, settings.showParticles]);

  const sendMessage = async () => {
    if (!userInput.trim()) return;

    const message = userInput;
    setChatMessages(prev => [...prev, { role: 'user', text: message }]);
    analyzeAndSpawnObjects(message);
    setUserInput('');
    setIsTyping(false);

    // Call MC AI backend
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, user_id: 'autonomous_ui' })
      });
      
      const data = await response.json();
      setChatMessages(prev => [...prev, {
        role: 'ai',
        text: data.response,
        emotion: data.emotion || currentScene
      }]);
    } catch (error) {
      console.error('Error:', error);
      setChatMessages(prev => [...prev, {
        role: 'ai',
        text: scenes[currentScene].message,
        emotion: currentScene
      }]);
    }
  };

  const clearObjects = () => {
    setSpawnedObjects([]);
    setMcaiTarget(null);
  };

  const sceneData = scenes[currentScene];

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      overflow: 'hidden',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      position: 'relative',
      display: 'flex'
    }}>
      {/* Background */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: settings.staticBackground ? scenes.neutral.background : sceneData.background,
        transition: settings.reduceMotion ? 'none' : 'background 1.5s ease-in-out',
        zIndex: 1
      }} />

      {/* Particles */}
      <canvas
        ref={canvasRef}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          zIndex: 2,
          pointerEvents: 'none'
        }}
      />

      {/* MC AI's World (Left Side) */}
      <div style={{
        width: '50%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 10,
        position: 'relative'
      }}>
        <div>
          <canvas
            ref={sceneCanvasRef}
            style={{
              border: '2px solid rgba(255,255,255,0.3)',
              borderRadius: '20px',
              boxShadow: '0 10px 40px rgba(0,0,0,0.3)',
              background: 'rgba(0,0,0,0.2)'
            }}
          />
          <div style={{
            marginTop: '10px',
            background: 'rgba(0,0,0,0.7)',
            backdropFilter: 'blur(10px)',
            padding: '10px',
            borderRadius: '10px',
            color: 'white',
            fontSize: '12px',
            textAlign: 'center'
          }}>
            <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>MC AI's World</div>
            <div style={{ opacity: 0.8 }}>Currently: {mcaiActivity.replace(/_/g, ' ')}</div>
            <div style={{ opacity: 0.6, fontSize: '10px', marginTop: '5px' }}>
              {spawnedObjects.length} objects spawned
            </div>
            <button
              onClick={clearObjects}
              style={{
                marginTop: '8px',
                padding: '5px 10px',
                background: 'rgba(255,255,255,0.2)',
                border: '1px solid rgba(255,255,255,0.3)',
                borderRadius: '5px',
                color: 'white',
                fontSize: '10px',
                cursor: 'pointer'
              }}
            >
              Clear Objects
            </button>
          </div>
        </div>
      </div>

      {/* Chat Interface (Right Side) */}
      <div style={{
        width: '50%',
        height: '100%',
        zIndex: 10,
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        padding: '20px'
      }}>
        {/* Scene Info */}
        <div style={{
          background: 'rgba(0,0,0,0.7)',
          backdropFilter: 'blur(10px)',
          padding: '15px 20px',
          borderRadius: '15px',
          color: 'white',
          textAlign: 'center',
          marginBottom: '20px'
        }}>
          <div style={{ fontSize: '20px', fontWeight: 'bold' }}>{sceneData.name}</div>
          <div style={{ fontSize: '12px', opacity: 0.8, marginTop: '5px' }}>
            528Hz 💜 Watch MC AI explore your world!
          </div>
        </div>

        {/* Chat Messages */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          marginBottom: '20px',
          background: 'rgba(0,0,0,0.5)',
          backdropFilter: 'blur(10px)',
          borderRadius: '15px',
          padding: '15px'
        }}>
          {chatMessages.map((msg, idx) => (
            <div
              key={idx}
              style={{
                marginBottom: '15px',
                textAlign: msg.role === 'user' ? 'right' : 'left'
              }}
            >
              <div style={{
                display: 'inline-block',
                padding: '10px 15px',
                borderRadius: '10px',
                background: msg.role === 'user' 
                  ? 'rgba(102, 126, 234, 0.8)' 
                  : 'rgba(118, 75, 162, 0.8)',
                color: 'white',
                maxWidth: '80%',
                wordBreak: 'break-word'
              }}>
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        {/* Input Area */}
        <div style={{
          display: 'flex',
          gap: '10px'
        }}>
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type something... MC AI will explore it!"
            style={{
              flex: 1,
              padding: '12px',
              borderRadius: '10px',
              border: '2px solid rgba(255,255,255,0.3)',
              background: 'rgba(0,0,0,0.6)',
              color: 'white',
              fontSize: '14px'
            }}
          />
          <button
            onClick={sendMessage}
            style={{
              padding: '12px 24px',
              borderRadius: '10px',
              border: 'none',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Send
          </button>
        </div>
      </div>

      {/* Settings Panel */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '20px',
        zIndex: 30,
        background: 'rgba(0,0,0,0.7)',
        backdropFilter: 'blur(10px)',
        padding: '12px',
        borderRadius: '12px',
        color: 'white',
        fontSize: '11px'
      }}>
        <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>⚙️ Settings</div>
        <label style={{ display: 'block', marginBottom: '6px', cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={settings.reduceMotion}
            onChange={(e) => setSettings({...settings, reduceMotion: e.target.checked})}
            style={{ marginRight: '6px' }}
          />
          Reduce Motion
        </label>
        <label style={{ display: 'block', marginBottom: '6px', cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={settings.staticBackground}
            onChange={(e) => setSettings({...settings, staticBackground: e.target.checked})}
            style={{ marginRight: '6px' }}
          />
          Static Background
        </label>
        <label style={{ display: 'block', marginBottom: '10px', cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={settings.showParticles}
            onChange={(e) => setSettings({...settings, showParticles: e.target.checked})}
            style={{ marginRight: '6px' }}
          />
          Show Particles
        </label>
        
        {/* Color Picker */}
        <div style={{ borderTop: '1px solid rgba(255,255,255,0.2)', paddingTop: '10px', marginTop: '4px' }}>
          <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>🎨 MC AI Color</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '6px' }}>
            {colorOptions.map((color) => (
              <button
                key={color.value}
                onClick={() => setMcaiColor(color.value)}
                title={color.name}
                style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '6px',
                  border: mcaiColor === color.value ? '3px solid white' : '2px solid rgba(255,255,255,0.3)',
                  background: color.value,
                  cursor: 'pointer',
                  fontSize: '14px',
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
      </div>
    </div>
  );
};

export default MCAIAutonomous;
