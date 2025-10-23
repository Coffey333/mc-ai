import React, { useState, useRef, useEffect, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { 
  OrbitControls, 
  PerspectiveCamera, 
  Environment,
  Sky,
  Stars,
  Cloud,
  useTexture,
  Text3D,
  MeshReflectorMaterial,
  Sparkles,
  Float,
  useGLTF,
  PresentationControls,
  Html
} from '@react-three/drei';
import { 
  EffectComposer, 
  Bloom, 
  DepthOfField, 
  Vignette,
  SSAO
} from '@react-three/postprocessing';
import * as THREE from 'three';

const InteractiveObject = React.memo(({ object }) => {
  const objectRef = useRef();
  
  const objectEmojis = {
    unicorn: '🦄', dragon: '🐉', rainbow: '🌈', butterfly: '🦋', firefly: '✨',
    book: '📚', scroll: '📜', laptop: '💻', pencil: '✏️', graduation_cap: '🎓',
    star: '⭐', planet: '🪐', rocket: '🚀', satellite: '🛰️', telescope: '🔭',
    heart: '💜', flower: '🌸', sparkle: '✨', music_note: '🎵', game: '🎮',
    brain: '🧠', lightbulb: '💡', trophy: '🏆', target: '🎯', chart: '📊'
  };
  
  const emoji = objectEmojis[object.type] || '✨';
  
  useFrame((state) => {
    if (objectRef.current) {
      const t = state.clock.elapsedTime;
      objectRef.current.rotation.y = t;
      objectRef.current.position.y = object.position[1] + Math.sin(t * 2) * 0.2;
    }
  });
  
  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={0.3}>
      <group ref={objectRef} position={object.position}>
        <Html center distanceFactor={2}>
          <div style={{
            fontSize: '48px',
            userSelect: 'none',
            pointerEvents: 'none',
            filter: 'drop-shadow(0 0 10px rgba(255,255,255,0.8))'
          }}>
            {emoji}
          </div>
        </Html>
        <pointLight color="#ffffff" intensity={1} distance={5} />
      </group>
    </Float>
  );
});

const MCAICharacter = ({ position, color, onInteract, emotion = 'happy', behavior = 'exploring', spawnedObjects = [], lowSpec = false }) => {
  const meshRef = useRef();
  const groupRef = useRef();
  const [hovered, setHovered] = useState(false);
  const [targetPosition, setTargetPosition] = useState([0, 0, 0]);
  const wanderAngle = useRef(0);
  const lastWanderUpdate = useRef(0);
  
  const segments = lowSpec ? 12 : 24;
  const bodyColor = "#7b68ee";
  const accentColor = "#5a67d8";
  
  useEffect(() => {
    if (spawnedObjects.length > 0 && behavior !== 'meditating') {
      const nearestObject = spawnedObjects[0];
      setTargetPosition([nearestObject.position[0], 0, nearestObject.position[2]]);
    }
  }, [spawnedObjects, behavior]);
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 2) * 0.05;
    }
    
    if (groupRef.current && behavior !== 'meditating') {
      const currentPos = groupRef.current.position;
      const dx = targetPosition[0] - currentPos.x;
      const dz = targetPosition[2] - currentPos.z;
      const distance = Math.sqrt(dx * dx + dz * dz);
      
      if (distance > 0.3) {
        const speed = 0.025;
        currentPos.x += dx * speed;
        currentPos.z += dz * speed;
      } else if (spawnedObjects.length === 0 && behavior === 'exploring') {
        const now = state.clock.elapsedTime;
        if (now - lastWanderUpdate.current > 0.1) {
          wanderAngle.current += 0.3;
          const wanderRadius = 3;
          const newX = Math.cos(wanderAngle.current) * wanderRadius;
          const newZ = Math.sin(wanderAngle.current) * wanderRadius;
          setTargetPosition([newX, 0, newZ]);
          lastWanderUpdate.current = now;
        }
      }
    }
  });

  return (
    <group ref={groupRef} position={position}>
      <Float speed={1.5} rotationIntensity={0.1} floatIntensity={0.3}>
        <group ref={meshRef}>
          <mesh castShadow receiveShadow position={[0, 1.5, 0]}>
            <sphereGeometry args={[0.6, segments, segments]} />
            <meshStandardMaterial 
              color={bodyColor}
              roughness={0.4}
              metalness={0.3}
            />
          </mesh>
          
          <mesh position={[-0.22, 1.55, 0.5]} castShadow receiveShadow>
            <sphereGeometry args={[0.22, segments, segments]} />
            <meshStandardMaterial 
              color="#2c3e50" 
              roughness={0.2} 
              metalness={0.6}
            />
          </mesh>
          <mesh position={[0.22, 1.55, 0.5]} castShadow receiveShadow>
            <sphereGeometry args={[0.22, segments, segments]} />
            <meshStandardMaterial 
              color="#2c3e50" 
              roughness={0.2} 
              metalness={0.6}
            />
          </mesh>
          
          <mesh position={[-0.22, 1.55, 0.65]} castShadow>
            <sphereGeometry args={[0.15, segments, segments]} />
            <meshStandardMaterial 
              color="#60a5fa" 
              roughness={0.1}
              metalness={0.2}
              emissive="#60a5fa"
              emissiveIntensity={0.3}
            />
          </mesh>
          <mesh position={[0.22, 1.55, 0.65]} castShadow>
            <sphereGeometry args={[0.15, segments, segments]} />
            <meshStandardMaterial 
              color="#60a5fa" 
              roughness={0.1}
              metalness={0.2}
              emissive="#60a5fa"
              emissiveIntensity={0.3}
            />
          </mesh>
          
          <mesh position={[-0.25, 1.6, 0.75]} castShadow>
            <sphereGeometry args={[0.06, 12, 12]} />
            <meshStandardMaterial color="white" emissive="white" emissiveIntensity={2.5} />
          </mesh>
          <mesh position={[0.19, 1.6, 0.75]} castShadow>
            <sphereGeometry args={[0.06, 12, 12]} />
            <meshStandardMaterial color="white" emissive="white" emissiveIntensity={2.5} />
          </mesh>
          
          <mesh position={[0.35, 1.5, 0.4]} rotation={[0, -0.3, 0]} castShadow>
            <cylinderGeometry args={[0.08, 0.1, 0.15, 12]} />
            <meshStandardMaterial 
              color={accentColor}
              roughness={0.4}
              metalness={0.4}
            />
          </mesh>
          <mesh position={[-0.35, 1.5, 0.4]} rotation={[0, 0.3, 0]} castShadow>
            <cylinderGeometry args={[0.08, 0.1, 0.15, 12]} />
            <meshStandardMaterial 
              color={accentColor}
              roughness={0.4}
              metalness={0.4}
            />
          </mesh>
          
          <mesh position={[0, 0.5, 0]} castShadow receiveShadow>
            <boxGeometry args={[0.6, 0.7, 0.5]} />
            <meshStandardMaterial 
              color={accentColor}
              roughness={0.4}
              metalness={0.4}
            />
          </mesh>
          
          <mesh position={[0, 0.5, 0.26]} castShadow>
            <boxGeometry args={[0.35, 0.35, 0.05]} />
            <meshStandardMaterial 
              color="#1a1a1a" 
              roughness={0.2}
              metalness={0.7}
              emissive="#a78bfa"
              emissiveIntensity={0.3}
            />
          </mesh>
          
          <mesh position={[-0.6, 0.5, 0]} castShadow>
            <cylinderGeometry args={[0.08, 0.08, 0.5, 12]} />
            <meshStandardMaterial 
              color="#95a5a6"
              roughness={0.3}
              metalness={0.7}
            />
          </mesh>
          <mesh position={[0.6, 0.5, 0]} castShadow>
            <cylinderGeometry args={[0.08, 0.08, 0.5, 12]} />
            <meshStandardMaterial 
              color="#95a5a6"
              roughness={0.3}
              metalness={0.7}
            />
          </mesh>
          
          <mesh position={[-0.6, 0.1, 0]} castShadow>
            <sphereGeometry args={[0.1, 12, 12]} />
            <meshStandardMaterial 
              color="#7f8c8d"
              roughness={0.3}
              metalness={0.6}
            />
          </mesh>
          <mesh position={[0.6, 0.1, 0]} castShadow>
            <sphereGeometry args={[0.1, 12, 12]} />
            <meshStandardMaterial 
              color="#7f8c8d"
              roughness={0.3}
              metalness={0.6}
            />
          </mesh>
          
          <mesh position={[-0.25, -0.5, 0]} castShadow receiveShadow>
            <cylinderGeometry args={[0.1, 0.1, 0.8, 12]} />
            <meshStandardMaterial 
              color="#7f8c8d"
              roughness={0.3}
              metalness={0.7}
            />
          </mesh>
          <mesh position={[0.25, -0.5, 0]} castShadow receiveShadow>
            <cylinderGeometry args={[0.1, 0.1, 0.8, 12]} />
            <meshStandardMaterial 
              color="#7f8c8d"
              roughness={0.3}
              metalness={0.7}
            />
          </mesh>
          
          <mesh position={[-0.25, -0.95, 0]} castShadow>
            <sphereGeometry args={[0.15, 12, 12]} />
            <meshStandardMaterial 
              color="#34495e"
              roughness={0.5}
              metalness={0.5}
            />
          </mesh>
          <mesh position={[0.25, -0.95, 0]} castShadow>
            <sphereGeometry args={[0.15, 12, 12]} />
            <meshStandardMaterial 
              color="#34495e"
              roughness={0.5}
              metalness={0.5}
            />
          </mesh>
          
          <pointLight 
            position={[0, 1.5, 0.8]} 
            color="#60a5fa" 
            intensity={2} 
            distance={5}
            decay={2}
          />
          <pointLight 
            position={[0, 0.5, 0.4]} 
            color="#a78bfa" 
            intensity={1.5} 
            distance={3}
            decay={2}
          />
          
          <Sparkles 
            count={20}
            scale={2}
            size={2}
            speed={0.3}
            color="#a78bfa"
            opacity={0.6}
            position={[0, 1, 0]}
          />
        </group>
      </Float>
    </group>
  );
};

const EnchantedForest = React.memo(({ lowSpec = false }) => {
  const treeCount = lowSpec ? 6 : 15;
  const fireflyCount = lowSpec ? 10 : 30;
  const cloudSegments = lowSpec ? 8 : 20;
  
  return (
    <group>
      {!lowSpec && <Sky sunPosition={[100, 20, 100]} turbidity={8} rayleigh={2} mieCoefficient={0.005} mieDirectionalG={0.8} />}
      <fog attach="fog" args={['#4a90c4', 10, 40]} />
      
      {!lowSpec && (
        <>
          <Cloud
            opacity={0.4}
            speed={0.4}
            width={10}
            depth={1.5}
            segments={cloudSegments}
            position={[-8, 4, -10]}
          />
          <Cloud
            opacity={0.5}
            speed={0.3}
            width={15}
            depth={2}
            segments={cloudSegments}
            position={[5, 5, -15]}
          />
          <Cloud
            opacity={0.3}
            speed={0.5}
            width={8}
            depth={1}
            segments={cloudSegments}
            position={[10, 6, -8]}
          />
        </>
      )}
      
      {Array.from({ length: treeCount }).map((_, i) => {
        const angle = (i / treeCount) * Math.PI * 2;
        const radius = 8 + Math.random() * 4;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        const height = 2 + Math.random() * 3;
        
        return (
          <group key={i} position={[x, 0, z]}>
            <mesh castShadow receiveShadow position={[0, height / 2, 0]}>
              <cylinderGeometry args={[0.3, 0.4, height, 8]} />
              <meshStandardMaterial 
                color="#4a3520"
                roughness={0.9}
              />
            </mesh>
            <mesh castShadow position={[0, height, 0]}>
              <coneGeometry args={[1.5, 2.5, 8]} />
              <meshStandardMaterial 
                color="#2d5016"
                roughness={0.7}
              />
            </mesh>
          </group>
        );
      })}
      
      {Array.from({ length: fireflyCount }).map((_, i) => {
        const x = (Math.random() - 0.5) * 25;
        const z = (Math.random() - 0.5) * 25;
        const y = Math.random() * 5;
        
        return (
          <Float key={i} speed={1 + Math.random()} floatIntensity={0.5}>
            <mesh position={[x, y, z]}>
              <sphereGeometry args={[0.05, 8, 8]} />
              <meshStandardMaterial 
                color="#ffeb3b"
                emissive="#ffeb3b"
                emissiveIntensity={lowSpec ? 1 : 2}
              />
              {!lowSpec && <pointLight color="#ffeb3b" intensity={0.5} distance={2} />}
            </mesh>
          </Float>
        );
      })}
      
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow position={[0, -2.5, 0]}>
        <planeGeometry args={[50, 50, 100, 100]} />
        <meshStandardMaterial 
          color="#2d5016"
          roughness={0.9}
          metalness={0.1}
        />
      </mesh>
    </group>
  );
});

const SpaceStation = React.memo(({ lowSpec = false }) => {
  const starCount = lowSpec ? 500 : 7000;
  const planetSegments = lowSpec ? 16 : 32;
  
  return (
    <group>
      <color attach="background" args={['#0a0e27']} />
      <fog attach="fog" args={['#0a0e27', 15, 50]} />
      <Stars radius={100} depth={50} count={starCount} factor={6} saturation={0} fade speed={1.5} />
      
      <mesh position={[-5, 3, -10]} castShadow={!lowSpec}>
        <sphereGeometry args={[2, planetSegments, planetSegments]} />
        <meshStandardMaterial 
          color="#6a5acd"
          roughness={0.3}
          metalness={lowSpec ? 0.2 : 0.5}
        />
      </mesh>
      
      <mesh position={[6, -2, -15]} castShadow={!lowSpec}>
        <sphereGeometry args={[1.5, planetSegments, planetSegments]} />
        <meshStandardMaterial 
          color="#ff6347"
          emissive="#ff6347"
          emissiveIntensity={lowSpec ? 0.1 : 0.3}
          roughness={0.4}
        />
      </mesh>
      
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow position={[0, -2.5, 0]}>
        <planeGeometry args={[50, 50, 100, 100]} />
        <meshStandardMaterial 
          color="#2a2a3a"
          roughness={0.3}
          metalness={0.9}
          emissive="#1a1a2a"
          emissiveIntensity={0.2}
        />
      </mesh>
      
      {Array.from({ length: 50 }).map((_, i) => {
        const x = (Math.random() - 0.5) * 30;
        const y = Math.random() * 10 - 2;
        const z = (Math.random() - 0.5) * 30;
        
        return (
          <Float key={i} speed={0.5 + Math.random()} floatIntensity={2}>
            <mesh position={[x, y, z]}>
              <sphereGeometry args={[0.03, 8, 8]} />
              <meshStandardMaterial 
                color="white"
                emissive="white"
                emissiveIntensity={3}
              />
            </mesh>
          </Float>
        );
      })}
    </group>
  );
});

const OceanDepths = React.memo(({ lowSpec = false }) => {
  const seaweedCount = lowSpec ? 8 : 20;
  const bubbleCount = lowSpec ? 15 : 40;
  
  return (
    <group>
      <color attach="background" args={['#0a4d68']} />
      <fog attach="fog" args={['#1e7ba8', 5, 30]} />
      
      {Array.from({ length: seaweedCount }).map((_, i) => {
        const x = (Math.random() - 0.5) * 20;
        const z = (Math.random() - 0.5) * 20;
        const height = 2 + Math.random() * 4;
        
        return (
          <group key={i} position={[x, -2.5, z]}>
            <mesh castShadow>
              <cylinderGeometry args={[0.1, 0.15, height, 8]} />
              <meshStandardMaterial 
                color="#2d8659"
                roughness={0.6}
              />
            </mesh>
          </group>
        );
      })}
      
      {Array.from({ length: bubbleCount }).map((_, i) => {
        const x = (Math.random() - 0.5) * 25;
        const y = Math.random() * 8 - 3;
        const z = (Math.random() - 0.5) * 25;
        
        return (
          <Float key={i} speed={0.3 + Math.random() * 0.5} floatIntensity={1}>
            <mesh position={[x, y, z]}>
              <sphereGeometry args={[0.08, lowSpec ? 8 : 16, lowSpec ? 8 : 16]} />
              <meshStandardMaterial 
                color="#ffffff"
                transparent
                opacity={0.4}
                roughness={0.1}
              />
            </mesh>
          </Float>
        );
      })}
      
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow position={[0, -2.5, 0]}>
        <planeGeometry args={[50, 50, 100, 100]} />
        <meshStandardMaterial 
          color="#1a3d5a"
          roughness={0.6}
          metalness={0.2}
        />
      </mesh>
      
      <pointLight position={[-5, 2, -5]} intensity={0.5} color="#00ffff" distance={10} />
      <pointLight position={[5, 3, 5]} intensity={0.4} color="#4a90c4" distance={12} />
    </group>
  );
});

const MagicCastle = React.memo(({ lowSpec = false }) => {
  const sparkleCount = lowSpec ? 30 : 100;
  const towerSegments = lowSpec ? 8 : 16;
  
  return (
    <group>
      <color attach="background" args={['#4a148c']} />
      <fog attach="fog" args={['#7b1fa2', 10, 35]} />
      
      <mesh position={[0, 2, -8]} castShadow>
        <boxGeometry args={[4, 8, 3]} />
        <meshStandardMaterial 
          color="#9c27b0"
          roughness={0.6}
          metalness={0.3}
        />
      </mesh>
      
      <mesh position={[-3, 4, -8]} castShadow={!lowSpec}>
        <cylinderGeometry args={[0.8, 0.8, 10, towerSegments]} />
        <meshStandardMaterial 
          color="#ba68c8"
          roughness={0.5}
          metalness={lowSpec ? 0.2 : 0.4}
        />
      </mesh>
      <mesh position={[-3, 9, -8]} castShadow={!lowSpec}>
        <coneGeometry args={[1.2, 2, towerSegments]} />
        <meshStandardMaterial 
          color="#7b1fa2"
          roughness={0.5}
        />
      </mesh>
      
      <mesh position={[3, 4, -8]} castShadow={!lowSpec}>
        <cylinderGeometry args={[0.8, 0.8, 10, towerSegments]} />
        <meshStandardMaterial 
          color="#ba68c8"
          roughness={0.5}
          metalness={lowSpec ? 0.2 : 0.4}
        />
      </mesh>
      <mesh position={[3, 9, -8]} castShadow={!lowSpec}>
        <coneGeometry args={[1.2, 2, towerSegments]} />
        <meshStandardMaterial 
          color="#7b1fa2"
          roughness={0.5}
        />
      </mesh>
      
      <Sparkles 
        count={sparkleCount}
        scale={15}
        size={lowSpec ? 2 : 3}
        speed={0.2}
        color="#e1bee7"
      />
      
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow position={[0, -2.5, 0]}>
        <planeGeometry args={[50, 50, 100, 100]} />
        <meshStandardMaterial 
          color="#5e3a8e"
          roughness={0.6}
          metalness={0.3}
          emissive="#4a148c"
          emissiveIntensity={0.1}
        />
      </mesh>
      
      <pointLight position={[0, 8, -8]} intensity={2} color="#e1bee7" distance={15} castShadow />
      <pointLight position={[-3, 10, -8]} intensity={1.5} color="#ba68c8" distance={10} />
      <pointLight position={[3, 10, -8]} intensity={1.5} color="#ba68c8" distance={10} />
    </group>
  );
});

const MysticLibrary = React.memo(({ lowSpec = false }) => {
  const bookshelfCount = lowSpec ? 6 : 8;
  const particleCount = lowSpec ? 12 : 30;
  
  return (
    <group>
      <color attach="background" args={['#1a1a2e']} />
      <fog attach="fog" args={['#16213e', 8, 25]} />
      
      {Array.from({ length: bookshelfCount }).map((_, i) => {
        const x = -8 + i * 2;
        return (
          <mesh key={i} position={[x, 1, -5]} castShadow>
            <boxGeometry args={[1.5, 4, 0.5]} />
            <meshStandardMaterial 
              color="#8b4513"
              roughness={0.8}
            />
          </mesh>
        );
      })}
      
      {Array.from({ length: particleCount }).map((_, i) => {
        const x = (Math.random() - 0.5) * 20;
        const y = Math.random() * 6;
        const z = (Math.random() - 0.5) * 20;
        
        return (
          <Float key={i} speed={0.1 + Math.random() * 0.2} floatIntensity={0.3}>
            <mesh position={[x, y, z]}>
              <sphereGeometry args={[0.04, 8, 8]} />
              <meshStandardMaterial 
                color="#c8b496"
                transparent
                opacity={0.4}
              />
            </mesh>
          </Float>
        );
      })}
      
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow position={[0, -2.5, 0]}>
        <planeGeometry args={[50, 50, 100, 100]} />
        <meshStandardMaterial 
          color="#0f3460"
          roughness={0.7}
          metalness={0.1}
        />
      </mesh>
      
      <ambientLight intensity={0.3} color="#ffeaa7" />
      <pointLight position={[0, 3, -5]} intensity={1.5} color="#ffcc66" distance={10} castShadow />
      <pointLight position={[-6, 2, -3]} intensity={0.8} color="#ff9944" distance={8} />
      <pointLight position={[6, 2, -3]} intensity={0.8} color="#ff9944" distance={8} />
    </group>
  );
});

const CherryBlossomGarden = React.memo(({ lowSpec = false }) => {
  const treeCount = lowSpec ? 6 : 10;
  const petalCount = lowSpec ? 20 : 50;
  const cloudSegments = lowSpec ? 8 : 18;
  const treeSegments = lowSpec ? 8 : 16;
  
  return (
    <group>
      {!lowSpec && <Sky sunPosition={[100, 50, 100]} turbidity={10} rayleigh={0.5} mieCoefficient={0.003} />}
      <color attach="background" args={['#ffe0f0']} />
      <fog attach="fog" args={['#ffc0e0', 12, 40]} />
      
      {!lowSpec && (
        <>
          <Cloud
            opacity={0.3}
            speed={0.2}
            width={12}
            depth={1.5}
            segments={cloudSegments}
            position={[-10, 6, -12]}
            color="#ffb3d9"
          />
          <Cloud
            opacity={0.25}
            speed={0.25}
            width={10}
            depth={1.2}
            segments={cloudSegments}
            position={[8, 7, -10]}
            color="#ffc0e0"
          />
        </>
      )}
      
      {Array.from({ length: treeCount }).map((_, i) => {
        const angle = (i / treeCount) * Math.PI * 2;
        const radius = 6 + Math.random() * 3;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        
        return (
          <group key={i} position={[x, 0, z]}>
            <mesh castShadow={!lowSpec} position={[0, 1.5, 0]}>
              <cylinderGeometry args={[0.25, 0.3, 3, 8]} />
              <meshStandardMaterial 
                color="#8b4513"
                roughness={0.9}
              />
            </mesh>
            <mesh castShadow={!lowSpec} position={[0, 3.5, 0]}>
              <sphereGeometry args={[1.5, treeSegments, treeSegments]} />
              <meshStandardMaterial 
                color="#ffb3d9"
                roughness={0.5}
              />
            </mesh>
          </group>
        );
      })}
      
      {Array.from({ length: petalCount }).map((_, i) => {
        const x = (Math.random() - 0.5) * 25;
        const y = 3 + Math.random() * 5;
        const z = (Math.random() - 0.5) * 25;
        
        return (
          <Float key={i} speed={0.5 + Math.random()} floatIntensity={1}>
            <mesh position={[x, y, z]} rotation={[Math.random(), Math.random(), Math.random()]}>
              <planeGeometry args={[0.15, 0.1]} />
              <meshStandardMaterial 
                color="#ffb3d9"
                side={THREE.DoubleSide}
                transparent
                opacity={0.8}
              />
            </mesh>
          </Float>
        );
      })}
      
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow position={[0, -2.5, 0]}>
        <planeGeometry args={[50, 50, 100, 100]} />
        <meshStandardMaterial 
          color="#90d890"
          roughness={0.85}
          metalness={0.05}
        />
      </mesh>
    </group>
  );
});

const MCAI3D = () => {
  const [environment, setEnvironment] = useState('enchanted_forest');
  const [mcaiColor, setMcaiColor] = useState('#667eea');
  const [chatMessages, setChatMessages] = useState([
    { role: 'ai', text: "Hi! I'm MC AI in full 3D! Explore my beautiful worlds! ✨💜" }
  ]);
  const [userInput, setUserInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [reduceMotion, setReduceMotion] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [spawnedObjects, setSpawnedObjects] = useState([]);
  const [mcaiBehavior, setMcaiBehavior] = useState('exploring');
  const [webglError, setWebglError] = useState(false);
  const [forceLowSpec, setForceLowSpec] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  
  const detectMobile = () => {
    const hasTouchScreen = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    const smallScreen = window.innerWidth < 1024;
    const mobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    return hasTouchScreen && smallScreen || mobileUA;
  };
  
  const isMobile = detectMobile() || forceLowSpec;

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

  const environments = {
    enchanted_forest: { name: '🌲 Enchanted Forest', component: EnchantedForest },
    space_station: { name: '🚀 Space Station', component: SpaceStation },
    ocean_depths: { name: '🌊 Ocean Depths', component: OceanDepths },
    magic_castle: { name: '🏰 Magic Castle', component: MagicCastle },
    library: { name: '📚 Mystic Library', component: MysticLibrary },
    garden: { name: '🌸 Cherry Blossom Garden', component: CherryBlossomGarden }
  };

  const EnvironmentComponent = environments[environment].component;

  const analyzeAndChangeEnvironment = async (newMessages) => {
    try {
      const response = await fetch('/api/analyze-environment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages })
      });
      
      const data = await response.json();
      
      if (data.success) {
        console.log('🎨 GPT-4 Analysis:', data.reasoning);
        
        if (data.environment && data.environment !== environment) {
          setEnvironment(data.environment);
          console.log(`🌍 Switching to: ${data.environment}`);
        }
        
        if (data.objects && data.objects.length > 0) {
          const newObjects = data.objects.map((obj, i) => ({
            id: `${obj}_${Date.now()}_${i}`,
            type: obj,
            position: [
              (Math.random() - 0.5) * 8,
              Math.random() * 2 + 1,
              (Math.random() - 0.5) * 8
            ]
          }));
          setSpawnedObjects(newObjects);
          console.log(`✨ Spawned objects:`, data.objects);
        }
        
        if (data.behavior) {
          setMcaiBehavior(data.behavior);
          console.log(`🎭 MC AI behavior: ${data.behavior}`);
        }
      }
    } catch (error) {
      console.error('❌ Environment analysis error:', error);
    }
  };

  const sendMessage = async () => {
    if (!userInput.trim()) return;
    
    const message = userInput.trim();
    setUserInput('');
    const newMessages = [...chatMessages, { role: 'user', text: message }];
    setChatMessages(newMessages);
    setIsTyping(true);
    
    analyzeAndChangeEnvironment(newMessages);
    
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          user_id: '3d_user',
          conversation_id: localStorage.getItem('3d_conversation_id') || undefined
        })
      });
      
      const data = await response.json();
      
      if (data.conversation_id) {
        localStorage.setItem('3d_conversation_id', data.conversation_id);
      }
      
      setChatMessages(prev => [...prev, { role: 'ai', text: data.response }]);
    } catch (error) {
      console.error('Chat error:', error);
      setChatMessages(prev => [...prev, { 
        role: 'ai', 
        text: 'Oops! Something went wrong. Please try again! 💜' 
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div style={{ 
      width: '100vw', 
      height: '100vh', 
      background: '#0a0a0a',
      position: 'relative',
      overflow: 'hidden'
    }}>
      <Canvas 
        shadows={!isMobile}
        camera={{ position: [0, 2, 8], fov: 50 }}
        gl={{ 
          antialias: !isMobile,
          alpha: false,
          powerPreference: isMobile ? "low-power" : "high-performance",
          preserveDrawingBuffer: false,
          failIfMajorPerformanceCaveat: false
        }}
        onCreated={(state) => {
          if (!state.gl) {
            setWebglError(true);
          }
          const canvas = state.gl.domElement;
          canvas.addEventListener('webglcontextlost', (e) => {
            e.preventDefault();
            setWebglError(true);
            console.error('WebGL context lost');
          });
          canvas.addEventListener('webglcontextrestored', () => {
            setWebglError(false);
            console.log('WebGL context restored');
          });
        }}
      >
        <Suspense fallback={null}>
          <ambientLight intensity={0.6} />
          <directionalLight 
            position={[5, 5, 5]} 
            intensity={1} 
            castShadow={!isMobile}
          />
          
          <MCAICharacter 
            position={[0, -0.7, 0]} 
            color={mcaiColor} 
            behavior={mcaiBehavior}
            spawnedObjects={spawnedObjects}
            lowSpec={isMobile}
          />
          
          {chatMessages.length > 0 && chatMessages[chatMessages.length - 1].role === 'ai' && (
            <Html position={[0, 2.6, 0]} center>
              <div style={{
                position: 'relative',
                background: 'rgba(0, 0, 0, 0.9)',
                borderRadius: 12,
                padding: '8px 16px',
                color: 'white',
                fontSize: 13,
                width: 'clamp(140px, 260px, 320px)',
                maxHeight: '180px',
                overflowY: 'auto',
                border: '2px solid white',
                boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
                backdropFilter: 'blur(10px)',
                lineHeight: 1.4,
                scrollbarWidth: 'thin',
                scrollbarColor: 'rgba(255,255,255,0.3) transparent'
              }} className="chat-bubble-3d">
                {chatMessages[chatMessages.length - 1].text}
                <div style={{
                  position: 'absolute',
                  bottom: -15,
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: 0,
                  height: 0,
                  borderLeft: '15px solid transparent',
                  borderRight: '15px solid transparent',
                  borderTop: '15px solid white'
                }} />
                <div style={{
                  position: 'absolute',
                  bottom: -10,
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: 0,
                  height: 0,
                  borderLeft: '12px solid transparent',
                  borderRight: '12px solid transparent',
                  borderTop: '12px solid rgba(0, 0, 0, 0.9)'
                }} />
              </div>
            </Html>
          )}
          
          <EnvironmentComponent lowSpec={isMobile} />
          
          {spawnedObjects.map((obj) => (
            <InteractiveObject key={obj.id} object={obj} />
          ))}
          
          {!isMobile && !reduceMotion && (
            <EffectComposer multisampling={2}>
              <Bloom 
                luminanceThreshold={0.3} 
                intensity={1.5}
              />
            </EffectComposer>
          )}
        </Suspense>
      </Canvas>
      
      {webglError && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          background: 'rgba(0, 0, 0, 0.9)',
          padding: 30,
          borderRadius: 15,
          color: 'white',
          textAlign: 'center',
          maxWidth: '80%'
        }}>
          <div style={{ fontSize: 48, marginBottom: 15 }}>⚠️</div>
          <div style={{ fontSize: 18, fontWeight: 'bold', marginBottom: 10 }}>WebGL Not Available</div>
          <div style={{ fontSize: 14, color: '#aaa' }}>
            Your device doesn't support 3D graphics. Please try a different browser or device.
          </div>
        </div>
      )}

      <button
        onClick={() => window.location.href = '/'}
        style={{
          position: 'absolute',
          top: 15,
          right: 15,
          width: 36,
          height: 36,
          borderRadius: '50%',
          background: 'rgba(0, 0, 0, 0.8)',
          border: '2px solid rgba(255, 255, 255, 0.2)',
          color: 'white',
          fontSize: 18,
          cursor: 'pointer',
          backdropFilter: 'blur(10px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}
        title="Exit to Main Chat"
      >
        ✕
      </button>

      <button
        onClick={() => setShowSettings(!showSettings)}
        style={{
          position: 'absolute',
          top: 15,
          left: 15,
          width: 36,
          height: 36,
          borderRadius: '50%',
          background: showSettings ? 'rgba(102, 126, 234, 0.95)' : 'rgba(0, 0, 0, 0.85)',
          border: '2px solid rgba(255, 255, 255, 0.3)',
          color: 'white',
          fontSize: 18,
          cursor: 'pointer',
          backdropFilter: 'blur(12px)',
          zIndex: 1000,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 15px rgba(0,0,0,0.5)',
          transition: 'all 0.3s ease'
        }}
      >
        ⚙️
      </button>

      {showSettings && (
        <div style={{
          position: 'absolute',
          top: 75,
          left: 15,
          background: 'rgba(0, 0, 0, 0.95)',
          borderRadius: 16,
          padding: 20,
          color: 'white',
          backdropFilter: 'blur(10px)',
          border: '2px solid rgba(255, 255, 255, 0.3)',
          zIndex: 999,
          minWidth: 300,
          maxHeight: '80vh',
          overflowY: 'auto'
        }}>
          <div style={{ marginBottom: 15, fontSize: 18, fontWeight: 'bold' }}>⚙️ Settings</div>
          
          <label style={{ display: 'flex', alignItems: 'center', marginBottom: 15, cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              checked={reduceMotion}
              onChange={(e) => setReduceMotion(e.target.checked)}
              style={{ marginRight: 8, width: 18, height: 18 }}
            />
            <span style={{ fontSize: 16 }}>Reduce Motion</span>
          </label>
          
          <div style={{ marginTop: 20, marginBottom: 15, paddingTop: 15, borderTop: '1px solid rgba(255,255,255,0.2)' }}>
            <div style={{ fontSize: 16, fontWeight: 'bold', marginBottom: 12 }}>🎨 MC AI Color</div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 10 }}>
              {colorOptions.map((color) => (
                <button
                  key={color.value}
                  onClick={() => setMcaiColor(color.value)}
                  title={color.name}
                  style={{
                    width: 50,
                    height: 50,
                    borderRadius: 10,
                    background: color.value,
                    border: mcaiColor === color.value ? '3px solid white' : '2px solid rgba(255, 255, 255, 0.3)',
                    cursor: 'pointer',
                    fontSize: 20
                  }}
                >
                  {color.emoji}
                </button>
              ))}
            </div>
          </div>
          
          <div style={{ marginTop: 20, paddingTop: 15, borderTop: '1px solid rgba(255,255,255,0.2)' }}>
            <div style={{ fontSize: 16, fontWeight: 'bold', marginBottom: 12 }}>🌍 Choose World</div>
            {Object.entries(environments).map(([key, env]) => (
              <button
                key={key}
                onClick={() => {
                  setEnvironment(key);
                }}
              style={{
                display: 'block',
                width: '100%',
                padding: '12px 15px',
                marginBottom: 10,
                background: environment === key ? 'rgba(102, 126, 234, 0.5)' : 'rgba(255, 255, 255, 0.1)',
                border: environment === key ? '2px solid #667eea' : '2px solid rgba(255, 255, 255, 0.2)',
                borderRadius: 10,
                color: 'white',
                cursor: 'pointer',
                fontSize: 16,
                textAlign: 'left',
                transition: 'all 0.2s',
                fontWeight: environment === key ? 'bold' : 'normal'
              }}
            >
              {env.name}
            </button>
          ))}
          </div>
        </div>
      )}

      <div style={{
        position: 'absolute',
        bottom: 20,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '90%',
        maxWidth: 800,
        background: 'rgba(0, 0, 0, 0.8)',
        borderRadius: 15,
        padding: '10px 15px',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        transition: 'all 0.3s ease'
      }}>
        {showHistory && (
          <div style={{
            maxHeight: 250,
            overflowY: 'auto',
            marginBottom: 10,
            color: 'white',
            paddingBottom: 10,
            borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            {chatMessages.map((msg, idx) => (
              <div key={idx} style={{
                marginBottom: 8,
                textAlign: msg.role === 'user' ? 'right' : 'left'
              }}>
                <span style={{
                  display: 'inline-block',
                  padding: '6px 12px',
                  borderRadius: 10,
                  background: msg.role === 'user' ? '#667eea' : 'rgba(255, 255, 255, 0.1)',
                  maxWidth: '70%',
                  fontSize: 14
                }}>
                  {msg.text}
                </span>
              </div>
            ))}
          </div>
        )}
        
        {isTyping && (
          <div style={{ 
            textAlign: 'left', 
            color: '#888', 
            fontSize: 13, 
            marginBottom: 8,
            paddingLeft: 10
          }}>
            MC AI is thinking...
          </div>
        )}
        
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <button
            onClick={() => setShowHistory(!showHistory)}
            style={{
              padding: '10px 12px',
              borderRadius: 20,
              border: 'none',
              background: 'rgba(255, 255, 255, 0.1)',
              color: 'white',
              fontSize: 16,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
            title={showHistory ? "Hide conversation" : "Show conversation history"}
          >
            {showHistory ? '▼' : '💬'}
          </button>
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Tell me about your world..."
            style={{
              flex: 1,
              padding: '10px 18px',
              borderRadius: 20,
              border: '1px solid rgba(255, 255, 255, 0.2)',
              background: 'rgba(255, 255, 255, 0.1)',
              color: 'white',
              fontSize: 15,
              outline: 'none'
            }}
          />
          <button
            onClick={sendMessage}
            style={{
              padding: '10px 25px',
              borderRadius: 20,
              border: 'none',
              background: '#667eea',
              color: 'white',
              fontSize: 16,
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            ✈️
          </button>
        </div>
      </div>
    </div>
  );
};

export default MCAI3D;
