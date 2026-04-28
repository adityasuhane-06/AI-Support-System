import React, { useState } from 'react';
import axios from 'axios';
import Dashboard from './Dashboard';

function App() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [responseData, setResponseData] = useState(null);

  const handleTriageSubmit = async (emailText, imageBase64 = null) => {
    setIsProcessing(true);
    setResponseData(null);
    try {
      // Connect to the Local FastAPI Agent Node
      const res = await axios.post('http://127.0.0.1:8000/api/triage', {
        email_text: emailText,
        image_base64: imageBase64,
        image_description: null // We rely entirely on the LLM vision node now
      });
      // Small artificial delay to let the user admire the 3D processing animation
      setTimeout(() => {
        setResponseData(res.data);
        setIsProcessing(false);
      }, 800);
    } catch (err) {
      console.error(err);
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4">
      {/* Absolute Background Orbs for Premium Vibe */}
      <div className="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-brand-900/20 blur-[120px] rounded-full"></div>
        <div className="absolute bottom-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-900/10 blur-[150px] rounded-full"></div>
      </div>
      
      <div className="z-10 w-full">
        <Dashboard 
          onSubmit={handleTriageSubmit} 
          isProcessing={isProcessing} 
          responseData={responseData} 
        />
      </div>
    </div>
  );
}

export default App;
