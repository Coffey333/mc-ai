import React, { useState, useEffect, useRef } from 'react';

const MCAIDelightful = () => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  
  // Environment transition refs
  const prevEnvironmentRef = useRef('enchanted_forest');
  const transitionProgressRef = useRef(1); // 0 to 1, 1 = fully transitioned
  
  // State
  const [mcai, setMcai] = useState({
    x: 400,
    y: 350,
    vx: 0,
    vy: 0,
    targetX: 400,
    targetY: 350,
    state: 'idle',
    facing: 'right',
    blinkTimer: 0,
    eyeOpenness: 1,
    expressionTimer: 0,
    currentExpression: 'happy'
  });
  
  const [environment, setEnvironment] = useState('enchanted_forest');
  const [objects, setObjects] = useState([]);
  const [particles, setParticles] = useState([]);
  const [thoughtBubble, setThoughtBubble] = useState({ show: false, text: '', emoji: '' });
  const [chatMessages, setChatMessages] = useState([
    { role: 'ai', text: "Hi! I'm MC AI! Let's explore amazing worlds together! ✨💜" }
  ]);
  const [userInput, setUserInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  
  // Settings
  const [mcaiColor, setMcaiColor] = useState(() => localStorage.getItem('mcaiColorDelightful') || '#667eea');
  const [settings, setSettings] = useState({ reduceMotion: false, soundEnabled: true });
  
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
  
  // Environments with rich details
  const environments = {
    enchanted_forest: {
      name: '🌲 Enchanted Forest',
      sky: { top: '#2d5a87', bottom: '#4a90c4' },
      ground: '#2d5016',
      layers: [
        { type: 'mountains', color: '#1a3d1a', y: 350, parallax: 0.3 },
        { type: 'trees_back', color: '#2d5016', y: 320, parallax: 0.5 },
        { type: 'trees_front', color: '#4a7c2f', y: 400, parallax: 0.8 }
      ],
      particles: 'fireflies'
    },
    space_station: {
      name: '🚀 Space Station',
      sky: { top: '#0a0e27', bottom: '#1a1f3a' },
      ground: '#2a2a3a',
      layers: [
        { type: 'stars', color: '#ffffff', y: 0, parallax: 0.2 },
        { type: 'planets', color: '#6a5acd', y: 100, parallax: 0.4 },
        { type: 'station', color: '#4a4a5a', y: 380, parallax: 1.0 }
      ],
      particles: 'stars'
    },
    ocean_depths: {
      name: '🌊 Ocean Depths',
      sky: { top: '#0a4d68', bottom: '#1e7ba8' },
      ground: '#1a3d5a',
      layers: [
        { type: 'coral', color: '#ff6b9d', y: 420, parallax: 0.6 },
        { type: 'seaweed', color: '#2d8659', y: 380, parallax: 0.7 },
        { type: 'bubbles', color: '#ffffff', y: 0, parallax: 0.3 }
      ],
      particles: 'bubbles'
    },
    magic_castle: {
      name: '🏰 Magic Castle',
      sky: { top: '#4a148c', bottom: '#7b1fa2' },
      ground: '#5e3a8e',
      layers: [
        { type: 'castle', color: '#9c27b0', y: 200, parallax: 0.4 },
        { type: 'towers', color: '#ba68c8', y: 300, parallax: 0.6 },
        { type: 'garden', color: '#8e24aa', y: 400, parallax: 0.9 }
      ],
      particles: 'magic'
    },
    library: {
      name: '📚 Mystic Library',
      sky: { top: '#1a1a2e', bottom: '#16213e' },
      ground: '#0f3460',
      layers: [
        { type: 'bookshelves', color: '#8b4513', y: 150, parallax: 0.3 },
        { type: 'desk', color: '#a0522d', y: 380, parallax: 0.8 },
        { type: 'books', color: '#cd853f', y: 350, parallax: 0.7 }
      ],
      particles: 'dust'
    },
    garden: {
      name: '🌸 Cherry Blossom Garden',
      sky: { top: '#ffe0f0', bottom: '#ffc0e0' },
      ground: '#90d890',
      layers: [
        { type: 'sakura_trees', color: '#ffb3d9', y: 200, parallax: 0.4 },
        { type: 'flowers', color: '#ff80bf', y: 400, parallax: 0.7 },
        { type: 'grass', color: '#70c070', y: 420, parallax: 0.9 }
      ],
      particles: 'petals'
    }
  };

  useEffect(() => {
    localStorage.setItem('mcaiColorDelightful', mcaiColor);
  }, [mcaiColor]);

  // Initialize canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Animation loop
  useEffect(() => {
    if (settings.reduceMotion) return;
    
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    let frameCount = 0;
    const env = environments[environment];
    
    const animate = () => {
      frameCount++;
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Handle environment transition
      if (transitionProgressRef.current < 1) {
        transitionProgressRef.current = Math.min(1, transitionProgressRef.current + 0.02); // Smooth 50-frame transition
      }
      
      // Draw sky with crossfade if transitioning
      if (transitionProgressRef.current < 1 && prevEnvironmentRef.current !== environment) {
        const prevEnv = environments[prevEnvironmentRef.current];
        const currEnv = environments[environment];
        const progress = transitionProgressRef.current;
        
        // Draw previous environment sky
        const prevSkyGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
        prevSkyGradient.addColorStop(0, prevEnv.sky.top);
        prevSkyGradient.addColorStop(1, prevEnv.sky.bottom);
        ctx.fillStyle = prevSkyGradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw current environment sky with alpha
        ctx.globalAlpha = progress;
        const currSkyGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
        currSkyGradient.addColorStop(0, currEnv.sky.top);
        currSkyGradient.addColorStop(1, currEnv.sky.bottom);
        ctx.fillStyle = currSkyGradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 1;
      } else {
        // Normal sky rendering
        const skyGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
        skyGradient.addColorStop(0, env.sky.top);
        skyGradient.addColorStop(1, env.sky.bottom);
        ctx.fillStyle = skyGradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }
      
      // Draw environment layers with parallax
      drawEnvironmentLayers(ctx, env, frameCount);
      
      // Update and draw particles
      updateAndDrawParticles(ctx, env, frameCount);
      
      // Update and draw objects
      updateAndDrawObjects(ctx, frameCount);
      
      // Draw ground
      ctx.fillStyle = env.ground;
      ctx.fillRect(0, canvas.height - 100, canvas.width, 100);
      
      // Update MC AI physics
      updateMCAI();
      
      // Draw MC AI character
      drawMCAI(ctx, frameCount);
      
      // Draw thought bubble
      if (thoughtBubble.show) {
        drawThoughtBubble(ctx);
      }
      
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [environment, mcai, objects, particles, thoughtBubble, mcaiColor, settings.reduceMotion]);

  const drawEnvironmentLayers = (ctx, env, frameCount) => {
    const time = frameCount * 0.02;
    
    env.layers.forEach((layer, index) => {
      ctx.save();
      ctx.globalAlpha = 0.7 + index * 0.1;
      
      if (layer.type === 'mountains') {
        drawMountains(ctx, layer, time);
      } else if (layer.type === 'trees_back' || layer.type === 'trees_front') {
        drawTrees(ctx, layer, time, layer.type === 'trees_front');
      } else if (layer.type === 'stars') {
        drawStarField(ctx, time);
      } else if (layer.type === 'planets') {
        drawPlanets(ctx, time);
      } else if (layer.type === 'castle') {
        drawCastle(ctx, layer);
      } else if (layer.type === 'bookshelves') {
        drawBookshelves(ctx, layer);
      } else if (layer.type === 'sakura_trees') {
        drawSakuraTrees(ctx, layer, time);
      }
      
      ctx.restore();
    });
  };

  const drawMountains = (ctx, layer, time) => {
    ctx.fillStyle = layer.color;
    ctx.beginPath();
    ctx.moveTo(0, ctx.canvas.height);
    for (let x = 0; x < ctx.canvas.width; x += 50) {
      const y = layer.y + Math.sin(x * 0.01 + time * layer.parallax) * 30;
      ctx.lineTo(x, y);
    }
    ctx.lineTo(ctx.canvas.width, ctx.canvas.height);
    ctx.closePath();
    ctx.fill();
  };

  const drawTrees = (ctx, layer, time, isFront) => {
    const treeCount = isFront ? 8 : 15;
    const treeWidth = isFront ? 40 : 25;
    const treeHeight = isFront ? 120 : 80;
    
    for (let i = 0; i < treeCount; i++) {
      const x = (i / treeCount) * ctx.canvas.width + Math.sin(time * layer.parallax + i) * 10;
      const y = layer.y;
      
      // Trunk
      ctx.fillStyle = '#4a3020';
      ctx.fillRect(x - treeWidth * 0.15, y, treeWidth * 0.3, treeHeight * 0.4);
      
      // Foliage
      ctx.fillStyle = layer.color;
      ctx.beginPath();
      ctx.ellipse(x, y - treeHeight * 0.2, treeWidth * 0.6, treeHeight * 0.6, 0, 0, Math.PI * 2);
      ctx.fill();
    }
  };

  const drawStarField = (ctx, time) => {
    for (let i = 0; i < 100; i++) {
      const x = (i * 137.5) % ctx.canvas.width;
      const y = (i * 197.3) % ctx.canvas.height;
      const size = (Math.sin(time + i) + 1) * 1.5;
      
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(x, y, size, 0, Math.PI * 2);
      ctx.fill();
    }
  };

  const drawPlanets = (ctx, time) => {
    // Large planet
    const gradient = ctx.createRadialGradient(200, 150, 20, 200, 150, 80);
    gradient.addColorStop(0, '#9370db');
    gradient.addColorStop(1, '#4b0082');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(200 + Math.sin(time * 0.2) * 20, 150, 80, 0, Math.PI * 2);
    ctx.fill();
    
    // Small moon
    ctx.fillStyle = '#b0c4de';
    ctx.beginPath();
    ctx.arc(ctx.canvas.width - 150, 100 + Math.cos(time * 0.3) * 30, 40, 0, Math.PI * 2);
    ctx.fill();
  };

  const drawCastle = (ctx, layer) => {
    const centerX = ctx.canvas.width / 2;
    const y = layer.y;
    
    // Main structure
    ctx.fillStyle = '#9c27b0';
    ctx.fillRect(centerX - 100, y, 200, 200);
    
    // Towers
    ctx.fillStyle = '#ba68c8';
    ctx.fillRect(centerX - 130, y - 50, 50, 250);
    ctx.fillRect(centerX + 80, y - 50, 50, 250);
    
    // Roof triangles
    ctx.fillStyle = '#8e24aa';
    ctx.beginPath();
    ctx.moveTo(centerX - 105, y - 50);
    ctx.lineTo(centerX - 155, y - 50);
    ctx.lineTo(centerX - 130, y - 100);
    ctx.closePath();
    ctx.fill();
    
    ctx.beginPath();
    ctx.moveTo(centerX + 105, y - 50);
    ctx.lineTo(centerX + 155, y - 50);
    ctx.lineTo(centerX + 130, y - 100);
    ctx.closePath();
    ctx.fill();
  };

  const drawBookshelves = (ctx, layer) => {
    const shelfCount = 5;
    const shelfHeight = 60;
    
    for (let i = 0; i < shelfCount; i++) {
      const y = layer.y + i * shelfHeight;
      
      // Shelf
      ctx.fillStyle = '#8b4513';
      ctx.fillRect(50, y, ctx.canvas.width - 100, 10);
      
      // Books
      for (let j = 0; j < 20; j++) {
        const bookX = 60 + j * ((ctx.canvas.width - 120) / 20);
        const bookHeight = 30 + Math.random() * 20;
        const bookWidth = 15 + Math.random() * 10;
        const hue = j * 20;
        
        ctx.fillStyle = `hsl(${hue}, 70%, 50%)`;
        ctx.fillRect(bookX, y - bookHeight, bookWidth, bookHeight);
      }
    }
  };

  const drawSakuraTrees = (ctx, layer, time) => {
    for (let i = 0; i < 6; i++) {
      const x = (i / 6) * ctx.canvas.width;
      const y = layer.y;
      
      // Trunk
      ctx.fillStyle = '#5d4037';
      ctx.fillRect(x - 10, y, 20, 200);
      
      // Branches with blossoms
      ctx.fillStyle = '#ffb3d9';
      for (let b = 0; b < 5; b++) {
        const bx = x + Math.cos(b + time * 0.1) * 60;
        const by = y + b * 30;
        ctx.beginPath();
        ctx.arc(bx, by, 40, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  };

  const updateAndDrawParticles = (ctx, env, frameCount) => {
    const time = frameCount * 0.05;
    
    if (env.particles === 'fireflies') {
      for (let i = 0; i < 30; i++) {
        const x = ((i * 73 + time * 2) % ctx.canvas.width);
        const y = 100 + Math.sin(time + i) * 200;
        const brightness = (Math.sin(time * 2 + i) + 1) / 2;
        
        ctx.fillStyle = `rgba(255, 255, 150, ${brightness})`;
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.shadowBlur = 10;
        ctx.shadowColor = 'yellow';
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    } else if (env.particles === 'stars') {
      // Already drawn in star field
    } else if (env.particles === 'bubbles') {
      for (let i = 0; i < 20; i++) {
        const x = ((i * 97 + time) % ctx.canvas.width);
        const y = ctx.canvas.height - ((time * 30 + i * 50) % ctx.canvas.height);
        const size = 5 + Math.sin(i) * 5;
        
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.stroke();
      }
    } else if (env.particles === 'magic') {
      for (let i = 0; i < 40; i++) {
        const x = ((i * 113 + time * 3) % ctx.canvas.width);
        const y = ((i * 127 + time * 2) % ctx.canvas.height);
        const hue = (time * 10 + i * 20) % 360;
        
        ctx.fillStyle = `hsla(${hue}, 100%, 70%, 0.6)`;
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    } else if (env.particles === 'petals') {
      for (let i = 0; i < 25; i++) {
        const x = ((i * 89 + time * 1.5) % ctx.canvas.width);
        const y = ((time * 40 + i * 60) % ctx.canvas.height);
        const rotation = time + i;
        
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rotation);
        ctx.fillStyle = '#ffb3d9';
        ctx.beginPath();
        ctx.ellipse(0, 0, 8, 4, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    } else if (env.particles === 'dust') {
      // Library dust motes - slow falling particles with depth
      for (let i = 0; i < 30; i++) {
        const depth = (i % 3) / 3; // 0, 0.33, 0.66 for depth layers
        const x = ((i * 107 + time * (0.5 + depth)) % ctx.canvas.width);
        const y = ((time * 15 * (1 + depth) + i * 70) % ctx.canvas.height);
        const size = 2 + depth * 2;
        const alpha = 0.2 + depth * 0.3;
        
        ctx.fillStyle = `rgba(200, 180, 150, ${alpha})`;
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
        
        // Slight glow
        ctx.shadowBlur = 5;
        ctx.shadowColor = 'rgba(255, 230, 200, 0.3)';
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    }
  };

  const updateAndDrawObjects = (ctx, frameCount) => {
    objects.forEach((obj, index) => {
      // Update object position with gentle floating
      obj.y += Math.sin(frameCount * 0.05 + index) * 0.3;
      
      // Draw object based on type
      ctx.save();
      ctx.font = `${obj.size}px Arial`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      // Shadow for depth
      ctx.shadowBlur = 10;
      ctx.shadowColor = 'rgba(0,0,0,0.3)';
      ctx.fillText(obj.emoji, obj.x, obj.y);
      
      ctx.restore();
    });
  };

  const updateMCAI = () => {
    setMcai(prev => {
      const newMcai = { ...prev };
      
      // Move towards target
      const dx = newMcai.targetX - newMcai.x;
      const dy = newMcai.targetY - newMcai.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance > 5) {
        newMcai.vx = dx * 0.05;
        newMcai.vy = dy * 0.05;
        newMcai.state = 'walking';
        newMcai.facing = dx > 0 ? 'right' : 'left';
      } else {
        newMcai.vx *= 0.9;
        newMcai.vy *= 0.9;
        if (Math.abs(newMcai.vx) < 0.1) newMcai.state = 'idle';
      }
      
      newMcai.x += newMcai.vx;
      newMcai.y += newMcai.vy;
      
      // Blink animation
      newMcai.blinkTimer++;
      if (newMcai.blinkTimer > 180) {
        newMcai.blinkTimer = 0;
      }
      if (newMcai.blinkTimer > 175 && newMcai.blinkTimer < 180) {
        newMcai.eyeOpenness = 0.2;
      } else {
        newMcai.eyeOpenness = 1;
      }
      
      return newMcai;
    });
  };

  const drawMCAI = (ctx, frameCount) => {
    const x = mcai.x;
    const y = mcai.y;
    const time = frameCount * 0.05;
    
    // Breathing animation
    const breathe = Math.sin(time * 2) * 3;
    const bounce = mcai.state === 'walking' ? Math.abs(Math.sin(time * 10) * 5) : 0;
    
    ctx.save();
    ctx.translate(x, y - bounce);
    if (mcai.facing === 'left') ctx.scale(-1, 1);
    
    // Shadow
    ctx.fillStyle = 'rgba(0,0,0,0.2)';
    ctx.beginPath();
    ctx.ellipse(0, 90, 50, 15, 0, 0, Math.PI * 2);
    ctx.fill();
    
    // Body (round and cute!)
    const bodyGradient = ctx.createRadialGradient(0, 0, 0, 0, 0, 70);
    bodyGradient.addColorStop(0, mcaiColor);
    bodyGradient.addColorStop(1, getDarkerColor(mcaiColor));
    ctx.fillStyle = bodyGradient;
    ctx.beginPath();
    ctx.arc(0, 0 + breathe, 60, 0, Math.PI * 2);
    ctx.fill();
    
    // Arms (cute little nubs!)
    ctx.fillStyle = mcaiColor;
    ctx.beginPath();
    ctx.ellipse(-50, 10 + breathe + Math.sin(time * 3) * 5, 20, 30, -0.3, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(50, 10 + breathe + Math.sin(time * 3 + 1) * 5, 20, 30, 0.3, 0, Math.PI * 2);
    ctx.fill();
    
    // Legs
    ctx.beginPath();
    ctx.ellipse(-20, 70 + breathe, 18, 25, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(20, 70 + breathe, 18, 25, 0, 0, Math.PI * 2);
    ctx.fill();
    
    // HUGE expressive eyes!
    const eyeY = -10 + breathe;
    const eyeSize = 20;
    const pupilSize = 12;
    
    // White of eyes
    ctx.fillStyle = 'white';
    ctx.beginPath();
    ctx.ellipse(-20, eyeY, eyeSize, eyeSize * mcai.eyeOpenness, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(20, eyeY, eyeSize, eyeSize * mcai.eyeOpenness, 0, 0, Math.PI * 2);
    ctx.fill();
    
    if (mcai.eyeOpenness > 0.5) {
      // Blue iris
      ctx.fillStyle = '#4a9eff';
      ctx.beginPath();
      ctx.arc(-20, eyeY, pupilSize, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(20, eyeY, pupilSize, 0, Math.PI * 2);
      ctx.fill();
      
      // Black pupils
      ctx.fillStyle = '#000';
      ctx.beginPath();
      ctx.arc(-20, eyeY, pupilSize * 0.6, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(20, eyeY, pupilSize * 0.6, 0, Math.PI * 2);
      ctx.fill();
      
      // Sparkle in eyes
      ctx.fillStyle = 'white';
      ctx.beginPath();
      ctx.arc(-23, eyeY - 3, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(17, eyeY - 3, 4, 0, Math.PI * 2);
      ctx.fill();
    }
    
    // Cute blush
    ctx.fillStyle = 'rgba(255, 182, 193, 0.6)';
    ctx.beginPath();
    ctx.ellipse(-40, 15 + breathe, 12, 8, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(40, 15 + breathe, 12, 8, 0, 0, Math.PI * 2);
    ctx.fill();
    
    // Happy smile
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.arc(0, 20 + breathe, 25, 0.2, Math.PI - 0.2);
    ctx.stroke();
    
    // Antenna with heart
    ctx.strokeStyle = getDarkerColor(mcaiColor);
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, -60 + breathe);
    ctx.lineTo(0, -80 + breathe + Math.sin(time * 2) * 3);
    ctx.stroke();
    
    // Glowing heart (528Hz)
    const heartGlow = (Math.sin(time * 3) + 1) / 2;
    ctx.shadowBlur = 15 + heartGlow * 10;
    ctx.shadowColor = '#ec4899';
    ctx.fillStyle = '#ec4899';
    ctx.font = 'bold 20px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('💖', 0, -85 + breathe + Math.sin(time * 2) * 3);
    ctx.shadowBlur = 0;
    
    ctx.restore();
  };

  const drawThoughtBubble = (ctx) => {
    const bubbleX = mcai.x;
    const bubbleY = mcai.y - 150;
    
    // Bubble tail
    ctx.fillStyle = 'white';
    ctx.beginPath();
    ctx.arc(bubbleX - 30, bubbleY + 45, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(bubbleX - 15, bubbleY + 55, 5, 0, Math.PI * 2);
    ctx.fill();
    
    // Main bubble (using arc instead of roundRect for compatibility)
    ctx.fillStyle = 'white';
    ctx.shadowBlur = 10;
    ctx.shadowColor = 'rgba(0,0,0,0.2)';
    const bx = bubbleX - 120;
    const by = bubbleY - 30;
    const bw = 240;
    const bh = 60;
    const br = 20;
    ctx.beginPath();
    ctx.moveTo(bx + br, by);
    ctx.lineTo(bx + bw - br, by);
    ctx.arc(bx + bw - br, by + br, br, -Math.PI/2, 0);
    ctx.lineTo(bx + bw, by + bh - br);
    ctx.arc(bx + bw - br, by + bh - br, br, 0, Math.PI/2);
    ctx.lineTo(bx + br, by + bh);
    ctx.arc(bx + br, by + bh - br, br, Math.PI/2, Math.PI);
    ctx.lineTo(bx, by + br);
    ctx.arc(bx + br, by + br, br, Math.PI, -Math.PI/2);
    ctx.closePath();
    ctx.fill();
    ctx.shadowBlur = 0;
    
    // Text
    ctx.fillStyle = '#333';
    ctx.font = '18px Comic Neue, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(thoughtBubble.text, bubbleX, bubbleY);
  };

  const getDarkerColor = (color) => {
    const hex = color.replace('#', '');
    const r = Math.max(0, parseInt(hex.substring(0, 2), 16) - 40);
    const g = Math.max(0, parseInt(hex.substring(2, 4), 16) - 40);
    const b = Math.max(0, parseInt(hex.substring(4, 6), 16) - 40);
    return `rgb(${r}, ${g}, ${b})`;
  };

  // MC AI autonomous behavior
  useEffect(() => {
    if (settings.reduceMotion) return;
    
    const roamInterval = setInterval(() => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      
      const newX = 100 + Math.random() * (canvas.width - 200);
      const newY = 300 + Math.random() * 100;
      
      setMcai(prev => ({ ...prev, targetX: newX, targetY: newY }));
      
      const thoughts = ['✨', '💭', '🤔', '💜', 'Where shall I go?', 'This is fun!', 'Exploring...'];
      showThought(thoughts[Math.floor(Math.random() * thoughts.length)]);
    }, 5000);
    
    return () => clearInterval(roamInterval);
  }, [settings.reduceMotion]);

  const showThought = (text, duration = 3000) => {
    setThoughtBubble({ show: true, text });
    setTimeout(() => setThoughtBubble({ show: false, text: '' }), duration);
  };

  const analyzeAndChangeEnvironment = (message) => {
    const lower = message.toLowerCase();
    let newEnv = environment;
    
    if (lower.includes('forest') || lower.includes('tree') || lower.includes('nature') || lower.includes('wood')) {
      newEnv = 'enchanted_forest';
    } else if (lower.includes('space') || lower.includes('star') || lower.includes('planet') || lower.includes('galaxy')) {
      newEnv = 'space_station';
    } else if (lower.includes('ocean') || lower.includes('sea') || lower.includes('water') || lower.includes('beach')) {
      newEnv = 'ocean_depths';
    } else if (lower.includes('castle') || lower.includes('magic') || lower.includes('fairy') || lower.includes('kingdom')) {
      newEnv = 'magic_castle';
    } else if (lower.includes('book') || lower.includes('study') || lower.includes('learn') || lower.includes('library')) {
      newEnv = 'library';
    } else if (lower.includes('flower') || lower.includes('garden') || lower.includes('spring') || lower.includes('cherry')) {
      newEnv = 'garden';
    }
    
    // Trigger smooth transition if environment changed
    if (newEnv !== environment) {
      prevEnvironmentRef.current = environment;
      transitionProgressRef.current = 0;
      setEnvironment(newEnv);
    }
  };

  const spawnObject = (emoji, type) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const newObj = {
      emoji,
      type,
      x: Math.random() * canvas.width,
      y: 200 + Math.random() * 200,
      size: 40,
      id: Date.now() + Math.random()
    };
    
    setObjects(prev => [...prev, newObj]);
    
    // Make MC AI go investigate
    setMcai(prev => ({ ...prev, targetX: newObj.x, targetY: newObj.y + 50 }));
  };

  const sendMessage = async () => {
    if (!userInput.trim()) return;
    
    const message = userInput.trim();
    setUserInput('');
    setChatMessages(prev => [...prev, { role: 'user', text: message }]);
    
    setIsTyping(true);
    setMcai(prev => ({ ...prev, state: 'thinking' }));
    showThought('Let me think about that... 🤔', 2000);
    
    // Analyze message for environment change
    analyzeAndChangeEnvironment(message);
    
    // Spawn relevant objects
    const lower = message.toLowerCase();
    if (lower.includes('dragon')) spawnObject('🐉', 'dragon');
    if (lower.includes('book')) spawnObject('📚', 'book');
    if (lower.includes('star')) spawnObject('⭐', 'star');
    if (lower.includes('heart') || lower.includes('love')) spawnObject('💜', 'heart');
    if (lower.includes('code') || lower.includes('program')) spawnObject('💻', 'computer');
    
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          user_id: 'delightful_user',
          conversation_id: localStorage.getItem('delightful_conversation_id') || undefined
        })
      });
      
      const data = await response.json();
      
      if (data.conversation_id) {
        localStorage.setItem('delightful_conversation_id', data.conversation_id);
      }
      
      setIsTyping(false);
      setChatMessages(prev => [...prev, { role: 'ai', text: data.response }]);
      showThought('"' + message.substring(0, 25) + '..." - I love it! ✨', 4000);
      
      setMcai(prev => ({ ...prev, state: 'celebrating' }));
      setTimeout(() => setMcai(prev => ({ ...prev, state: 'idle' })), 2000);
      
    } catch (error) {
      console.error('Chat error:', error);
      setIsTyping(false);
      setChatMessages(prev => [...prev, { role: 'ai', text: "Oops! Something went wrong, but I'm still here! 💜" }]);
    }
  };

  return (
    <div style={{ width: '100vw', height: '100vh', overflow: 'hidden', position: 'relative' }}>
      {/* Main Canvas */}
      <canvas
        ref={canvasRef}
        style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}
        onClick={(e) => {
          const rect = e.currentTarget.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          setMcai(prev => ({ ...prev, targetX: x, targetY: y }));
        }}
      />
      
      {/* Chat Interface */}
      <div style={{
        position: 'fixed',
        bottom: 20,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '90%',
        maxWidth: '700px',
        zIndex: 10
      }}>
        {/* Recent messages */}
        {chatMessages.length > 1 && (
          <div style={{ marginBottom: 12, maxHeight: 150, overflowY: 'auto' }}>
            {chatMessages.slice(-3).map((msg, idx) => (
              <div key={idx} style={{ marginBottom: 8, textAlign: msg.role === 'user' ? 'right' : 'left' }}>
                <div style={{
                  display: 'inline-block',
                  background: msg.role === 'user' ? 'rgba(102, 126, 234, 0.95)' : 'rgba(255, 255, 255, 0.95)',
                  color: msg.role === 'user' ? 'white' : '#1a202c',
                  padding: '10px 16px',
                  borderRadius: 16,
                  maxWidth: '70%',
                  fontSize: 15,
                  backdropFilter: 'blur(10px)',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
                }}>
                  {msg.text}
                </div>
              </div>
            ))}
          </div>
        )}
        
        {/* Input */}
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Tell me about your world..."
            style={{
              flex: 1,
              padding: '16px 20px',
              borderRadius: 999,
              border: 'none',
              background: 'rgba(255, 255, 255, 0.95)',
              fontSize: 16,
              outline: 'none',
              boxShadow: '0 4px 20px rgba(0,0,0,0.2)'
            }}
          />
          <button
            onClick={sendMessage}
            style={{
              width: 56,
              height: 56,
              borderRadius: '50%',
              border: 'none',
              background: 'linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%)',
              color: 'white',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 15px rgba(255, 126, 95, 0.4)'
            }}
          >
            <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </div>
      </div>

      {/* Settings */}
      <div style={{
        position: 'fixed',
        top: 20,
        left: 20,
        background: 'rgba(0,0,0,0.7)',
        backdropFilter: 'blur(10px)',
        padding: 12,
        borderRadius: 12,
        color: 'white',
        fontSize: 12,
        zIndex: 30
      }}>
        <div style={{ fontWeight: 'bold', marginBottom: 8 }}>⚙️ Settings</div>
        <label style={{ display: 'block', marginBottom: 12, cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={settings.reduceMotion}
            onChange={(e) => setSettings({...settings, reduceMotion: e.target.checked})}
            style={{ marginRight: 6 }}
          />
          Reduce Motion
        </label>
        
        <div style={{ borderTop: '1px solid rgba(255,255,255,0.2)', paddingTop: 10 }}>
          <div style={{ fontWeight: 'bold', marginBottom: 8 }}>🎨 MC AI Color</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 6 }}>
            {colorOptions.map((color) => (
              <button
                key={color.value}
                onClick={() => setMcaiColor(color.value)}
                title={color.name}
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: 6,
                  border: mcaiColor === color.value ? '3px solid white' : '2px solid rgba(255,255,255,0.3)',
                  background: color.value,
                  cursor: 'pointer',
                  fontSize: 14
                }}
              >
                {color.emoji}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Environment selector */}
      <div style={{
        position: 'fixed',
        top: 20,
        right: 20,
        background: 'rgba(0,0,0,0.7)',
        backdropFilter: 'blur(10px)',
        padding: 12,
        borderRadius: 12,
        color: 'white',
        fontSize: 12,
        zIndex: 30
      }}>
        <div style={{ fontWeight: 'bold', marginBottom: 8 }}>🌍 World</div>
        {Object.keys(environments).map((envKey) => (
          <div
            key={envKey}
            onClick={() => setEnvironment(envKey)}
            style={{
              padding: '6px 10px',
              borderRadius: 6,
              cursor: 'pointer',
              background: environment === envKey ? 'rgba(102, 126, 234, 0.5)' : 'transparent',
              marginBottom: 4
            }}
          >
            {environments[envKey].name}
          </div>
        ))}
      </div>

      {/* Global Styles */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');
        * { font-family: 'Comic Neue', cursive, -apple-system, BlinkMacSystemFont, sans-serif; }
      `}</style>
    </div>
  );
};

export default MCAIDelightful;
