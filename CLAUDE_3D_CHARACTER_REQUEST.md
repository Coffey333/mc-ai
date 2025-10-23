# Technical Request for 3D Character Design - MC AI Robot

## Project Overview
I'm working on a React/Three.js 3D character interface that currently uses basic geometric shapes (spheres, capsules) to create a simple robot character. I need to upgrade this to match a specific cute robot design drawing that has a Mega Man-inspired aesthetic.

## Current Technical Stack
- **Framework**: React 18 + Three.js (via React Three Fiber)
- **File**: `frontend/src/components/MCAI3D.jsx`
- **Current Implementation**: Lines 68-240 (MCAICharacter component)
- **Rendering**: Real-time WebGL with mobile optimization support
- **Performance**: Must maintain 60fps on desktop, 30fps on mobile

## Target Design Requirements

### Reference Style
The character should resemble:
- **Primary Reference**: The attached cute robot drawing (big eyes, peace sign pose, chibi proportions)
- **Secondary Reference**: Modern Mega Man character design (Mega Man 11 style)
- **Art Style**: Anime/chibi aesthetic with smooth, rounded forms

### Specific Character Features

#### 1. **Head Design**
- **Shape**: Large, rounded head (approximately 1.8x body size - chibi proportions)
- **Eyes**: 
  - VERY large, expressive anime-style eyes (major focal point)
  - White outer spheres with glossy black pupils
  - Small white highlight dots for sparkle/life effect
  - Eyes should be approximately 40% of head width each
  - Positioned close together for cute appearance
- **Antenna/Headgear**: 
  - Small antenna or fin on top of head
  - Optional: Small ear-like protrusions or headphone details

#### 2. **Body Proportions**
- **Style**: Chibi/super-deformed proportions
- **Head**: ~40% of total height
- **Torso**: ~30% of total height  
- **Legs**: ~30% of total height
- **Overall Height**: Approximately 3 units in Three.js space

#### 3. **Arms & Hands**
- **Critical Feature**: RIGHT ARM making peace sign (✌️) gesture
  - Two extended fingers (index and middle)
  - Other fingers curled inward
  - Positioned at shoulder height
- **Left Arm**: Relaxed at side or slightly raised
- **Design**: Rounded robot arms with visible joints/segments
- **Material**: Match body color (customizable via `color` prop)

#### 4. **Legs & Feet**
- **Style**: Chunky robot boots (Mega Man style)
- **Proportions**: Short, sturdy legs
- **Feet**: Large, blocky boots with rounded edges

#### 5. **Color & Materials**
- **Primary Color**: Customizable via `color` prop (currently `#667eea` blue)
- **Accent Colors**:
  - White for eyes and highlights
  - Dark gray/black for pupils and joints
  - Optional: Pink/purple cheek blushes (semi-transparent spheres)
  - Heart emblem on chest (#ff1493 pink, glowing)
- **Material Properties**:
  - Main body: `metalness: 0.7, roughness: 0.2` (shiny robot finish)
  - Eyes: `metalness: 0.8, roughness: 0.1` (glossy)

## Technical Implementation Requirements

### Code Structure
The character must be implemented within the existing `MCAICharacter` component structure:

```jsx
const MCAICharacter = ({ position, color, onInteract, emotion = 'happy', behavior = 'exploring', spawnedObjects = [], lowSpec = false }) => {
  // Character geometry here
  return (
    <group ref={groupRef} position={position}>
      <Float speed={1.5} rotationIntensity={0.1} floatIntensity={0.3}>
        <group ref={meshRef}>
          {/* 3D meshes here */}
        </group>
      </Float>
    </group>
  );
};
```

### Performance Constraints
- **Mobile Optimization**: When `lowSpec={true}`, reduce geometry segments from 64→24
- **Segments Variable**: Use `const segments = lowSpec ? 24 : 64;` for sphere/cylinder geometries
- **Shadow Casting**: All major meshes should use `castShadow receiveShadow`
- **Maximum Poly Count**: ~50k triangles on desktop, ~15k on mobile

### Animation Hooks (Already Implemented)
The character has existing animations that must continue working:
- **Floating**: Gentle up/down motion via Float component
- **Idle Breathing**: Slight rotation via `useFrame` hook
- **Right Arm Wave**: Peace sign arm should have subtle animation
- **Movement**: Character moves toward spawned objects

### Existing Props to Maintain
- `position`: [x, y, z] coordinates
- `color`: Primary body color (hex string)
- `emotion`: 'happy' | 'sad' | 'excited' (optional future facial changes)
- `behavior`: 'exploring' | 'studying' | 'playing' | 'meditating'
- `lowSpec`: Boolean for mobile optimization

## Desired Output

### What I Need from You
1. **Complete JSX code** for the character mesh geometry (replacing lines 113-240)
2. **Proper Three.js primitives**: Use `<mesh>`, `<sphereGeometry>`, `<cylinderGeometry>`, `<capsuleGeometry>`, `<boxGeometry>`, etc.
3. **Accurate positioning**: All mesh positions relative to character origin [0, 0, 0]
4. **Material setup**: Proper `<meshStandardMaterial>` with correct roughness/metalness
5. **Peace sign hand**: Detailed geometry for the right hand making ✌️ gesture

### Code Style Requirements
- Use React Three Fiber JSX syntax (not imperative Three.js)
- Position values as arrays: `position={[x, y, z]}`
- Rotation values in radians: `rotation={[rx, ry, rz]}`
- All geometries wrapped in `<mesh>` tags
- Maintain existing component structure

### Optional Enhancements
- **Facial Expressions**: Simple emotion changes (eye size, mouth shape) based on `emotion` prop
- **Joint Details**: Small spheres at arm/leg joints for robotic appearance
- **Chest Emblem**: Heart-shaped or circular emblem with glow effect (already partially implemented)

## Reference Materials Attached
- **Drawing**: Cute robot with big eyes and peace sign (main reference)
- **Style Guide**: Modern Mega Man character proportions

## Current Code Section to Replace
The current character uses simple geometric shapes (spheres and capsules). The NEW design should replace the mesh definitions while maintaining the same:
- Component props
- Animation hooks (`useFrame`, `useRef`)
- Grouping structure
- Performance optimization logic

## Questions for Claude
1. Should I use GLTF model import or pure Three.js primitives? (Prefer primitives for performance)
2. How detailed should the peace sign fingers be? (Can use simple cylinders or more complex geometry)
3. Should the character be symmetrical or have personality asymmetry?

## Timeline & Scope
This is a visual upgrade to an existing working system. The character functions perfectly with current geometry - we're just making it match the cute design drawing. Focus on **geometric accuracy** and **cute appeal** while maintaining **performance**.

---

**Contact**: This file is part of the MC AI project at `/frontend/src/components/MCAI3D.jsx`. The character appears in a 3D environment with dynamic backgrounds, interactive objects, and real-time chat bubbles.

**Thank you for helping bring MC AI's visual design to life!** 💜✨
