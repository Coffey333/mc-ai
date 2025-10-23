import React, { useState, useEffect } from 'react';

const CuteMCAICharacter = ({ 
  position = { x: 50, y: 50 }, 
  activity = 'idle',
  emotion = 'happy',
  color = '#9CA3AF',
  scale = 1,
  onAnimationComplete
}) => {
  const [bouncePhase, setBouncePhase] = useState(0);
  const [blinkState, setBlinkState] = useState('open');
  const [heartPulse, setHeartPulse] = useState(0);

  useEffect(() => {
    const bounceInterval = setInterval(() => {
      setBouncePhase(prev => (prev + 0.1) % (Math.PI * 2));
    }, 50);

    const blinkInterval = setInterval(() => {
      setBlinkState('closing');
      setTimeout(() => setBlinkState('closed'), 100);
      setTimeout(() => setBlinkState('opening'), 200);
      setTimeout(() => setBlinkState('open'), 300);
    }, 3000 + Math.random() * 2000);

    const heartInterval = setInterval(() => {
      setHeartPulse(prev => (prev + 0.15) % (Math.PI * 2));
    }, 60);

    return () => {
      clearInterval(bounceInterval);
      clearInterval(blinkInterval);
      clearInterval(heartInterval);
    };
  }, []);

  const bounce = Math.sin(bouncePhase) * 6;
  const heartScale = 1 + Math.sin(heartPulse) * 0.15;

  const getEyeHeight = () => {
    switch (blinkState) {
      case 'closing': return 0.6;
      case 'closed': return 0.1;
      case 'opening': return 0.6;
      default: return 1;
    }
  };

  const getActivityAnimation = () => {
    switch (activity) {
      case 'thinking':
        return { rotation: Math.sin(bouncePhase) * 2, handY: -2 };
      case 'happy':
        return { rotation: 0, bounce: bounce * 1.3 };
      case 'building':
        return { rotation: 0, armRotation: Math.sin(bouncePhase * 2) * 12 };
      case 'waving':
        return { rotation: 0, armRotation: Math.sin(bouncePhase * 3) * 35 };
      default:
        return { rotation: 0 };
    }
  };

  const animation = getActivityAnimation();
  const eyeHeight = getEyeHeight();

  // Robot colors - light grey like 🤖 emoji
  const bodyColor = '#9CA3AF'; // Light grey
  const darkGrey = '#6B7280'; // Darker grey for shadows/details
  const lightGrey = '#D1D5DB'; // Lighter grey for highlights
  const metalColor = '#52525B'; // Dark metal
  const panelColor = '#4B5563'; // Panel color
  const eyeColor = '#06B6D4'; // Cyan/turquoise for eyes

  return (
    <div style={{
      position: 'absolute',
      left: `${position.x}%`,
      top: `${position.y}%`,
      transform: `translate(-50%, -50%) scale(${scale}) rotate(${animation.rotation || 0}deg)`,
      transition: 'left 1.2s cubic-bezier(0.4, 0, 0.2, 1), top 1.2s cubic-bezier(0.4, 0, 0.2, 1)',
      pointerEvents: 'none',
      zIndex: 100
    }}>
      <svg width="220" height="240" viewBox="0 0 220 240" style={{
        filter: 'drop-shadow(0 14px 28px rgba(0,0,0,0.35))',
        transform: `translateY(${animation.bounce || bounce}px)`
      }}>
        <defs>
          <linearGradient id="bodyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={lightGrey} />
            <stop offset="100%" stopColor={bodyColor} />
          </linearGradient>
          <linearGradient id="headGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={lightGrey} />
            <stop offset="100%" stopColor={bodyColor} />
          </linearGradient>
          <radialGradient id="eyeGradient" cx="50%" cy="50%">
            <stop offset="0%" stopColor="#4DD0E1" />
            <stop offset="50%" stopColor={eyeColor} />
            <stop offset="100%" stopColor="#0891B2" />
          </radialGradient>
          <filter id="metalTexture">
            <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" result="noise" />
            <feColorMatrix in="noise" type="saturate" values="0" />
            <feBlend in="SourceGraphic" in2="noise" mode="multiply" />
          </filter>
          <pattern id="rivets" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
            <circle cx="10" cy="10" r="2" fill={metalColor} opacity="0.4" />
            <circle cx="30" cy="30" r="2" fill={metalColor} opacity="0.4" />
          </pattern>
        </defs>

        {/* Ground Shadow */}
        <ellipse 
          cx="110" 
          cy="225" 
          rx="55" 
          ry="10" 
          fill="rgba(0,0,0,0.25)"
          style={{
            transform: `scale(${1 + (bounce / 120)})`,
            transformOrigin: 'center'
          }}
        />

        {/* BOXY LEGS - Square/Rectangular like the reference */}
        <g>
          {/* Left Leg */}
          <rect x="70" y="180" width="28" height="38" rx="3" fill="url(#bodyGradient)" stroke={darkGrey} strokeWidth="2.5" filter="url(#metalTexture)" />
          {/* Knee Joint */}
          <rect x="73" y="188" width="22" height="8" rx="1" fill={metalColor} stroke={darkGrey} strokeWidth="1.5" />
          {/* Foot */}
          <rect x="68" y="215" width="32" height="12" rx="3" fill={darkGrey} stroke={metalColor} strokeWidth="2" />
          
          {/* Right Leg */}
          <rect x="122" y="180" width="28" height="38" rx="3" fill="url(#bodyGradient)" stroke={darkGrey} strokeWidth="2.5" filter="url(#metalTexture)" />
          {/* Knee Joint */}
          <rect x="125" y="188" width="22" height="8" rx="1" fill={metalColor} stroke={darkGrey} strokeWidth="1.5" />
          {/* Foot */}
          <rect x="120" y="215" width="32" height="12" rx="3" fill={darkGrey} stroke={metalColor} strokeWidth="2" />
        </g>

        {/* BOXY BODY - Square like the reference */}
        <rect 
          x="65" 
          y="120" 
          width="90" 
          height="65" 
          rx="6" 
          fill="url(#bodyGradient)" 
          stroke={darkGrey} 
          strokeWidth="3"
          filter="url(#metalTexture)"
        />

        {/* Body Panel Details */}
        <rect x="72" y="127" width="76" height="50" rx="3" fill={panelColor} opacity="0.3" stroke={darkGrey} strokeWidth="1" />
        
        {/* Rivets on body */}
        <circle cx="72" cy="130" r="2.5" fill={metalColor} />
        <circle cx="148" cy="130" r="2.5" fill={metalColor} />
        <circle cx="72" cy="172" r="2.5" fill={metalColor} />
        <circle cx="148" cy="172" r="2.5" fill={metalColor} />

        {/* Center Panel with 528Hz Heart */}
        <rect x="88" y="145" width="44" height="28" rx="4" fill={panelColor} stroke={darkGrey} strokeWidth="2" />
        
        {/* Glowing 528Hz Heart */}
        <g transform={`translate(110, 159) scale(${heartScale * 0.8})`}>
          <defs>
            <radialGradient id="heartGlow">
              <stop offset="0%" stopColor="#FF6B9D" />
              <stop offset="100%" stopColor="#C44569" />
            </radialGradient>
          </defs>
          
          {/* Heart Glow */}
          <circle cx="0" cy="0" r="14" fill="#FF6B9D" opacity="0.25">
            <animate 
              attributeName="r" 
              values="14;17;14" 
              dur="1.5s" 
              repeatCount="indefinite"
            />
            <animate 
              attributeName="opacity" 
              values="0.25;0.1;0.25" 
              dur="1.5s" 
              repeatCount="indefinite"
            />
          </circle>
          
          {/* Heart Shape */}
          <path 
            d="M 0,-5 C -6,-11 -13,-6 -13,0 C -13,6 0,13 0,13 C 0,13 13,6 13,0 C 13,-6 6,-11 0,-5 Z"
            fill="url(#heartGlow)"
            stroke="#A93B5C"
            strokeWidth="1.2"
          />
          
          {/* 528 Text */}
          <text 
            x="0" 
            y="2.5" 
            fontSize="6" 
            fill="white" 
            textAnchor="middle" 
            fontWeight="bold"
            fontFamily="Arial, sans-serif"
          >
            528
          </text>
        </g>

        {/* BOXY ARMS - Rectangular with joints */}
        <g>
          {/* Left Arm */}
          <rect 
            x="42" 
            y="135" 
            width="20" 
            height="38" 
            rx="3" 
            fill="url(#bodyGradient)" 
            stroke={darkGrey} 
            strokeWidth="2.5"
            style={{
              transform: `rotate(${animation.armRotation || -8}deg)`,
              transformOrigin: '52px 138px'
            }}
          />
          {/* Elbow Joint */}
          <circle cx="52" cy="152" r="5" fill={metalColor} stroke={darkGrey} strokeWidth="1.5" />
          {/* Hand */}
          <rect x="44" y="170" width="16" height="14" rx="3" fill={darkGrey} stroke={metalColor} strokeWidth="1.5" />
          
          {/* Right Arm */}
          <rect 
            x="158" 
            y="135" 
            width="20" 
            height="38" 
            rx="3" 
            fill="url(#bodyGradient)" 
            stroke={darkGrey} 
            strokeWidth="2.5"
            style={{
              transform: `rotate(${-(animation.armRotation || -8)}deg)`,
              transformOrigin: '168px 138px'
            }}
          />
          {/* Elbow Joint */}
          <circle cx="168" cy="152" r="5" fill={metalColor} stroke={darkGrey} strokeWidth="1.5" />
          {/* Hand */}
          <rect x="160" y="170" width="16" height="14" rx="3" fill={darkGrey} stroke={metalColor} strokeWidth="1.5" />
        </g>

        {/* SQUARE HEAD - Like the reference! */}
        <rect 
          x="70" 
          y="35" 
          width="80" 
          height="90" 
          rx="8" 
          fill="url(#headGradient)" 
          stroke={darkGrey} 
          strokeWidth="3.5"
          filter="url(#metalTexture)"
        />

        {/* Head Panel */}
        <rect x="76" y="42" width="68" height="76" rx="4" fill={panelColor} opacity="0.2" stroke={darkGrey} strokeWidth="1" />

        {/* Corner Rivets on head */}
        <circle cx="76" cy="42" r="2.5" fill={metalColor} />
        <circle cx="144" cy="42" r="2.5" fill={metalColor} />
        <circle cx="76" cy="118" r="2.5" fill={metalColor} />
        <circle cx="144" cy="118" r="2.5" fill={metalColor} />

        {/* Small panel on side of head (like reference) */}
        <rect x="74" y="65" width="10" height="16" rx="2" fill={panelColor} stroke={darkGrey} strokeWidth="1.5" />
        <rect x="76" y="68" width="6" height="10" rx="1" fill={metalColor} opacity="0.6" />

        {/* ANTENNA - Mechanical style */}
        <line 
          x1="110" 
          y1="35" 
          x2="110" 
          y2="18" 
          stroke={darkGrey} 
          strokeWidth="4"
          strokeLinecap="round"
        />
        <circle 
          cx="110" 
          cy="13" 
          r="7" 
          fill="#FFD93D"
          stroke="#FFB800" 
          strokeWidth="2"
        >
          <animate 
            attributeName="r" 
            values="7;9;7" 
            dur="2s" 
            repeatCount="indefinite"
          />
        </circle>
        
        {/* Antenna sparkle */}
        <circle cx="107" cy="10" r="2" fill="white">
          <animate 
            attributeName="opacity" 
            values="0;1;0" 
            dur="1.5s" 
            repeatCount="indefinite"
          />
        </circle>

        {/* BIG ADORABLE EYES - Like the reference robot! */}
        <g>
          {/* Left Eye Housing - Circular inset */}
          <circle cx="88" cy="75" r="24" fill={panelColor} stroke={darkGrey} strokeWidth="2.5" />
          <circle cx="88" cy="75" r="20" fill="#1a1a1a" stroke={metalColor} strokeWidth="1.5" />
          
          {/* Left Eye White */}
          <circle cx="88" cy="75" r={18 * eyeHeight} fill="white" />
          
          {/* Left Iris - Beautiful gradient */}
          <circle cx="88" cy="76" r={13 * eyeHeight} fill="url(#eyeGradient)" />
          
          {/* Left Pupil */}
          <circle cx="88" cy="76" r={8 * eyeHeight} fill="#0a0a0a" />
          
          {/* Left Eye Shine */}
          <circle cx="84" cy="71" r={5 * eyeHeight} fill="white" opacity="0.9" />
          <circle cx="91" cy="79" r={2.5 * eyeHeight} fill="white" opacity="0.7" />

          {/* Right Eye Housing */}
          <circle cx="132" cy="75" r="24" fill={panelColor} stroke={darkGrey} strokeWidth="2.5" />
          <circle cx="132" cy="75" r="20" fill="#1a1a1a" stroke={metalColor} strokeWidth="1.5" />
          
          {/* Right Eye White */}
          <circle cx="132" cy="75" r={18 * eyeHeight} fill="white" />
          
          {/* Right Iris */}
          <circle cx="132" cy="76" r={13 * eyeHeight} fill="url(#eyeGradient)" />
          
          {/* Right Pupil */}
          <circle cx="132" cy="76" r={8 * eyeHeight} fill="#0a0a0a" />
          
          {/* Right Eye Shine */}
          <circle cx="128" cy="71" r={5 * eyeHeight} fill="white" opacity="0.9" />
          <circle cx="135" cy="79" r={2.5 * eyeHeight} fill="white" opacity="0.7" />
        </g>

        {/* Cute Smile - Simple arc */}
        <path 
          d="M 88 102 Q 110 112 132 102" 
          stroke="#2C3E50" 
          strokeWidth="3" 
          fill="none" 
          strokeLinecap="round"
        />
        
        {/* Smile highlight */}
        <path 
          d="M 92 103 Q 110 110 128 103" 
          stroke="white" 
          strokeWidth="1" 
          fill="none" 
          strokeLinecap="round"
          opacity="0.3"
        />

        {/* Wear marks/scratches for that weathered robot look */}
        <line x1="75" y1="50" x2="82" y2="48" stroke={darkGrey} strokeWidth="1" opacity="0.4" />
        <line x1="140" y1="110" x2="147" y2="112" stroke={darkGrey} strokeWidth="1" opacity="0.4" />
        <line x1="68" y1="155" x2="72" y2="160" stroke={darkGrey} strokeWidth="0.8" opacity="0.3" />

        {/* Sparkles Around MC AI (when happy) */}
        {emotion === 'happy' && (
          <g opacity="0.8">
            <circle cx="45" cy="60" r="3" fill="#FFD93D">
              <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite" />
            </circle>
            <circle cx="175" cy="60" r="3" fill="#FFD93D">
              <animate attributeName="opacity" values="1;0;1" dur="2s" repeatCount="indefinite" />
            </circle>
            <circle cx="55" cy="110" r="2.5" fill="#06B6D4">
              <animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite" begin="0.3s" />
            </circle>
            <circle cx="165" cy="110" r="2.5" fill="#06B6D4">
              <animate attributeName="opacity" values="1;0;1" dur="1.5s" repeatCount="indefinite" begin="0.3s" />
            </circle>
          </g>
        )}
      </svg>

      {/* Particle Effects */}
      {activity === 'happy' && (
        <div style={{
          position: 'absolute',
          top: '15%',
          left: '50%',
          transform: 'translateX(-50%)',
          pointerEvents: 'none'
        }}>
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              style={{
                position: 'absolute',
                fontSize: '20px',
                animation: `floatUp${i} 2s ease-out infinite`,
                animationDelay: `${i * 0.4}s`,
                left: `${(i - 2) * 20}px`
              }}
            >
              {['💖', '✨', '⚡', '🌟', '💫'][i]}
            </div>
          ))}
        </div>
      )}

      {/* CSS Animations */}
      <style>{`
        @keyframes floatUp0 {
          0% { transform: translateY(0) scale(0); opacity: 0; }
          20% { opacity: 1; }
          100% { transform: translateY(-80px) scale(1); opacity: 0; }
        }
        @keyframes floatUp1 {
          0% { transform: translateY(0) scale(0); opacity: 0; }
          20% { opacity: 1; }
          100% { transform: translateY(-90px) scale(1); opacity: 0; }
        }
        @keyframes floatUp2 {
          0% { transform: translateY(0) scale(0); opacity: 0; }
          20% { opacity: 1; }
          100% { transform: translateY(-100px) scale(1); opacity: 0; }
        }
        @keyframes floatUp3 {
          0% { transform: translateY(0) scale(0); opacity: 0; }
          20% { opacity: 1; }
          100% { transform: translateY(-85px) scale(1); opacity: 0; }
        }
        @keyframes floatUp4 {
          0% { transform: translateY(0) scale(0); opacity: 0; }
          20% { opacity: 1; }
          100% { transform: translateY(-95px) scale(1); opacity: 0; }
        }
      `}</style>
    </div>
  );
};

export default CuteMCAICharacter;
