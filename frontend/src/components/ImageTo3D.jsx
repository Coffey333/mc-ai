import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { useGLTF, OrbitControls, Environment, Html } from '@react-three/drei';

const SERVER_URL = window.location.origin;

function ModelViewer({ modelUrl }) {
  const { scene } = useGLTF(modelUrl);
  return <primitive object={scene} scale={2} />;
}

function Loader() {
  return (
    <Html center>
      <div style={{ 
        color: 'white', 
        fontSize: '1.5em',
        textAlign: 'center',
        background: 'rgba(0,0,0,0.8)',
        padding: '20px',
        borderRadius: '10px'
      }}>
        ✨ Generating 3D Model...<br />
        <div style={{ fontSize: '0.8em', marginTop: '10px', color: '#aaa' }}>
          This can take 2-5 minutes
        </div>
      </div>
    </Html>
  );
}

export function ImageTo3DGenerator() {
  const [modelUrl, setModelUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState('');

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);
    setError(null);
    setModelUrl(null);
    setProgress('Uploading image...');

    const formData = new FormData();
    formData.append('image', file);

    try {
      setProgress('Sending to AI...');
      const response = await fetch(`${SERVER_URL}/api/generate-model`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || 'Failed to generate model');
      }

      setProgress('Processing... almost done!');
      const data = await response.json();
      setModelUrl(data.modelUrl);
      setProgress('Complete! 🎉');

    } catch (err) {
      setError(err.message);
      setProgress('');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#0a0a0a' }}>
      <div style={{ 
        padding: '20px', 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
        color: 'white',
        borderBottom: '2px solid rgba(255,255,255,0.1)'
      }}>
        <button
          onClick={() => window.location.href = '/autonomous'}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            padding: '10px 20px',
            background: 'rgba(255,255,255,0.2)',
            border: 'none',
            borderRadius: '20px',
            color: 'white',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: 'bold'
          }}
        >
          ← Back to 3D World
        </button>
        
        <h2 style={{ margin: '0 0 10px 0', fontSize: '28px' }}>🎨 AI 2D-to-3D Model Generator</h2>
        <p style={{ margin: '0 0 15px 0', opacity: 0.9 }}>
          Upload your robot drawing to generate a 3D model using Tripo AI
        </p>
        
        <input 
          type="file" 
          accept="image/png, image/jpeg, image/jpg" 
          onChange={handleImageUpload} 
          disabled={isLoading}
          style={{
            padding: '12px',
            background: 'rgba(255,255,255,0.9)',
            border: 'none',
            borderRadius: '8px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontSize: '14px',
            color: '#333'
          }}
        />
        
        {progress && (
          <div style={{ 
            marginTop: '15px', 
            padding: '12px 20px',
            background: 'rgba(0,0,0,0.3)',
            borderRadius: '8px',
            display: 'inline-block'
          }}>
            {progress}
          </div>
        )}
        
        {error && (
          <div style={{ 
            marginTop: '15px',
            padding: '12px 20px',
            background: 'rgba(255,0,0,0.2)',
            borderRadius: '8px',
            border: '1px solid rgba(255,0,0,0.5)'
          }}>
            ❌ Error: {error}
          </div>
        )}
      </div>

      <Canvas 
        camera={{ position: [0, 2, 8], fov: 50 }}
        style={{ background: '#0a0a0a' }}
      >
        <Suspense fallback={isLoading ? <Loader /> : null}>
          {modelUrl && <ModelViewer modelUrl={modelUrl} />}

          <ambientLight intensity={0.5} />
          <directionalLight position={[10, 10, 10]} intensity={2} />
          <pointLight position={[-10, -10, -10]} intensity={1} />
          <Environment preset="sunset" />
        </Suspense>

        <OrbitControls />
      </Canvas>
      
      {!modelUrl && !isLoading && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
          color: 'white',
          fontSize: '18px',
          pointerEvents: 'none'
        }}>
          <div style={{ fontSize: '64px', marginBottom: '20px' }}>🎨</div>
          <div>Upload an image above to generate a 3D model</div>
        </div>
      )}
    </div>
  );
}

export default ImageTo3DGenerator;
