import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Icosahedron, Float } from '@react-three/drei';

function SleekCore({ isProcessing }) {
  const outerRef = useRef();
  const innerRef = useRef();

  useFrame(({ clock }) => {
    const time = clock.getElapsedTime();
    
    if (outerRef.current && innerRef.current) {
      if (isProcessing) {
        // Fast, erratic spinning when processing data
        outerRef.current.rotation.x = time * 1.5;
        outerRef.current.rotation.y = time * 2.0;
        innerRef.current.rotation.y = -time * 1.2;
        
        // Aggressive pulsating scale
        const pulse = 1 + Math.sin(time * 15) * 0.08;
        outerRef.current.scale.set(pulse, pulse, pulse);
      } else {
        // Slow, elegant idle revolving
        outerRef.current.rotation.x = time * 0.15;
        outerRef.current.rotation.y = time * 0.2;
        innerRef.current.rotation.y = -time * 0.1;
        
        // Smooth breathing scale
        const breathe = 1 + Math.sin(time * 2) * 0.02;
        outerRef.current.scale.set(breathe, breathe, breathe);
      }
    }
  });

  return (
    <Float speed={isProcessing ? 6 : 2} rotationIntensity={0.5} floatIntensity={isProcessing ? 2 : 1}>
      <group scale={1.1}>
        {/* Inner Solid Tech Core */}
        <Icosahedron ref={innerRef} args={[1, 3]}>
          <meshStandardMaterial 
            color="#0f172a" 
            roughness={0.7}
            metalness={0.5}
          />
        </Icosahedron>
        
        {/* Outer Neural Wireframe */}
        <Icosahedron ref={outerRef} args={[1.25, 2]}>
          <meshBasicMaterial 
            color={isProcessing ? "#d946ef" : "#64748b"} 
            wireframe={true} 
            transparent={true}
            opacity={isProcessing ? 0.9 : 0.2}
          />
        </Icosahedron>
      </group>
    </Float>
  );
}

export default function AnimatedCore({ isProcessing = false }) {
  return (
    <div className="w-full h-full relative pointer-events-none flex items-center justify-center">
      {/* Background glow behind the core */}
      <div className={`absolute w-40 h-40 blur-[80px] rounded-full transition-colors duration-1000 ${
        isProcessing ? 'bg-brand-500/50' : 'bg-slate-500/10'
      }`}></div>
      
      <Canvas camera={{ position: [0, 0, 4.5], fov: 45 }}>
        <ambientLight intensity={1.5} />
        <directionalLight position={[10, 10, 5]} intensity={2} />
        <directionalLight position={[-10, -10, -5]} intensity={1} color="#d946ef" />
        <SleekCore isProcessing={isProcessing} />
        <OrbitControls enableZoom={false} enablePan={false} />
      </Canvas>
    </div>
  );
}
