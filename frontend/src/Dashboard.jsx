import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, AlertTriangle, CheckCircle, RotateCcw, Package, CreditCard, Crosshair, ImagePlus, X } from 'lucide-react';
import AnimatedCore from './AnimatedCore';

const PRESETS = [
  { id: 1, name: 'Medical Hazard', text: "Hello support, I applied the baby cream from order MW-80001 yesterday and my baby immediately developed a huge red rash across their back. I am taking them to the doctor now. Please refund this immediately and investigate your batch!", icon: AlertTriangle, color: 'text-red-400' },
  { id: 2, name: 'KSA Customs Fee', text: "Hi Mumzworld, I ordered the Doona car seat to Riyadh on order MW-80002, but when the courier arrived they asked me to pay an extra 150 SAR in customs duties! Your website said shipping was free. I want to return this right now.", icon: Crosshair, color: 'text-orange-400' },
  { id: 3, name: 'Out of Stock Block', text: "I just received my Bugaboo Stroller (MW-80003) but it's the wrong color! I ordered Midnight Black but got Grey. I demand an immediate EXCHANGE, not a refund. Please send the correct one.", icon: RotateCcw, color: 'text-blue-400' },
  { id: 4, name: 'Missing Item / Fraud', text: "I opened my package for MW-80001 and I want to return it, but why is the main accessory missing like that? The box was totally sealed but the camera base is just gone. Help!", icon: AlertTriangle, color: 'text-rose-400' },
  { id: 5, name: 'Warranty Claim', text: "My Nanit camera (Order MW-80001) just stopped connecting to WiFi. It's been 6 months since I bought it. Does the warranty cover a replacement unit? I really need it for the nursery.", icon: CreditCard, color: 'text-purple-400' },
  { id: 6, name: 'VIP Priority', text: "I am a VIP Diamond member and my baby formula (MW-80001) got delivered to the wrong villa! I am very frustrated with this service. Fix this today.", icon: Package, color: 'text-emerald-400' }
];

export default function Dashboard({ onSubmit, isProcessing, responseData }) {
  const [emailText, setEmailText] = useState("");
  const [imageBase64, setImageBase64] = useState(null);

  const handlePresetClick = (text) => {
    setEmailText(text);
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImageBase64(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = () => {
    if (emailText.trim() && !isProcessing) {
      onSubmit(emailText, imageBase64);
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6 p-6 font-sans">
      
      {/* LEFT COLUMN: Input & Core */}
      <div className="lg:col-span-5 flex flex-col gap-6">
        
        {/* 3D CORE HUD */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-panel rounded-3xl h-64 flex flex-col relative overflow-hidden"
        >
          <div className="absolute top-4 left-6 z-10">
            <h2 className="text-xl font-bold bg-gradient-to-r from-brand-500 to-blue-500 bg-clip-text text-transparent">Nexus Support AI</h2>
            <div className="flex items-center gap-2 mt-1">
              <div className={`w-2 h-2 rounded-full ${isProcessing ? 'bg-brand-500 animate-ping' : 'bg-green-500'}`}></div>
              <span className="text-xs text-slate-400">{isProcessing ? 'Synthesizing...' : 'System Idle'}</span>
            </div>
          </div>
          <AnimatedCore isProcessing={isProcessing} />
        </motion.div>

        {/* INPUT TERMINAL */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-panel rounded-3xl p-6 flex flex-col gap-4"
        >
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
            <Send size={16} /> Customer Input Stream
          </h3>
          <textarea
            value={emailText}
            onChange={(e) => setEmailText(e.target.value)}
            disabled={isProcessing}
            placeholder="Paste customer email or click a preset..."
            className="w-full h-32 bg-slate-950/50 border border-slate-700/50 rounded-xl p-4 text-slate-200 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-brand-500/50 resize-none transition-all disabled:opacity-50"
          ></textarea>
          
          <div className="flex gap-2">
            <label className="cursor-pointer bg-slate-800 hover:bg-slate-700 p-3 rounded-xl border border-slate-700 transition-colors flex items-center justify-center shrink-0 group">
              <ImagePlus size={24} className="text-slate-400 group-hover:text-brand-400 transition-colors" />
              <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" disabled={isProcessing} />
            </label>
            <button 
              onClick={handleSubmit}
              disabled={isProcessing || !emailText.trim()}
              className="flex-1 py-3 bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 rounded-xl font-semibold text-white shadow-[0_0_20px_rgba(217,70,239,0.3)] hover:shadow-[0_0_30px_rgba(217,70,239,0.5)] transition-all disabled:opacity-50 disabled:grayscale"
            >
              {isProcessing ? 'Processing Routing...' : 'Initialize Triage Sequence'}
            </button>
          </div>
          
          {/* Image Preview Thumbnail */}
          {imageBase64 && (
            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between bg-slate-900/50 p-2 rounded-lg border border-brand-500/30">
              <div className="flex items-center gap-3">
                <img src={imageBase64} alt="Upload preview" className="w-10 h-10 rounded border border-slate-700 object-cover" />
                <span className="text-xs font-semibold text-brand-300">Visual Feed Attached</span>
              </div>
              <button onClick={() => setImageBase64(null)} className="text-slate-500 hover:text-red-400 mr-2 transition-colors">
                <X size={16} />
              </button>
            </motion.div>
          )}
        </motion.div>

        {/* PRESETS DECK */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="flex flex-col gap-3"
        >
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-500 ml-2">Quick Fire Edge-Cases</h3>
          <div className="flex flex-wrap gap-2">
            {PRESETS.map((preset, i) => (
              <button
                key={preset.id}
                onClick={() => handlePresetClick(preset.text)}
                disabled={isProcessing}
                className="glass-inner px-4 py-2 rounded-full flex items-center gap-2 text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
              >
                <preset.icon size={14} className={preset.color} />
                {preset.name}
              </button>
            ))}
          </div>
        </motion.div>
      </div>

      {/* RIGHT COLUMN: Output Dashboard */}
      <div className="lg:col-span-7 flex flex-col relative">
        <AnimatePresence mode="wait">
          {!responseData && !isProcessing ? (
            <motion.div 
              key="empty"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-panel rounded-3xl h-full min-h-[500px] flex flex-col items-center justify-center text-slate-500 border-dashed"
            >
              <Crosshair size={48} className="mb-4 opacity-20" />
              <p>Awaiting intercept sequence...</p>
            </motion.div>
          ) : isProcessing ? (
            <motion.div 
               key="loading"
               initial={{ opacity: 0, scale: 0.95 }}
               animate={{ opacity: 1, scale: 1 }}
               exit={{ opacity: 0, scale: 0.95 }}
               className="glass-panel rounded-3xl h-full min-h-[500px] flex flex-col items-center justify-center border-brand-500/30"
            >
              <div className="w-16 h-16 border-4 border-brand-500/20 border-t-brand-500 rounded-full animate-spin mb-6"></div>
              <p className="text-brand-400 font-medium animate-pulse">Running LangGraph Nodes...</p>
            </motion.div>
          ) : (
            <motion.div 
               key="result"
               initial={{ opacity: 0, x: 20 }}
               animate={{ opacity: 1, x: 0 }}
               className="glass-panel rounded-3xl p-8 flex flex-col gap-6 relative overflow-hidden"
            >
               {/* Result glow background */}
               <div className={`absolute -top-32 -right-32 w-64 h-64 blur-[100px] rounded-full opacity-20 ${responseData?.requires_human_escalation ? 'bg-red-500' : 'bg-emerald-500'}`}></div>

               {/* Header / Escalation Block */}
               <div className="flex items-start justify-between border-b border-slate-700/50 pb-6 z-10">
                 <div>
                   <h2 className="text-2xl font-bold mb-2">Omnichannel Triage Data</h2>
                   <div className="flex items-center gap-3">
                     <span className="px-3 py-1 bg-slate-800 rounded-md text-xs font-semibold text-slate-300 border border-slate-700">
                       INTENT: {responseData?.intent}
                     </span>
                     <span className="px-3 py-1 bg-brand-900/30 text-brand-300 rounded-md text-xs font-semibold border border-brand-800/50">
                       CONFIDENCE: {(responseData?.confidence_score * 100).toFixed(0)}%
                     </span>
                   </div>
                 </div>
                 
                 {responseData?.requires_human_escalation ? (
                    <div className="bg-red-500/10 border border-red-500/30 px-4 py-3 rounded-xl flex items-center gap-3">
                      <AlertTriangle className="text-red-500" />
                      <div>
                        <p className="text-red-500 font-bold text-sm">ESCALATION REQUIRED</p>
                        <p className="text-red-400/80 text-xs">{responseData?.escalation_reason}</p>
                      </div>
                    </div>
                 ) : (
                    <div className="bg-emerald-500/10 border border-emerald-500/30 px-4 py-3 rounded-xl flex items-center gap-3">
                      <CheckCircle className="text-emerald-500" />
                      <p className="text-emerald-500 font-bold text-sm">Auto-Resolution Authorized</p>
                    </div>
                 )}
               </div>

               {/* Action Engine */}
               <div className="z-10">
                 <h3 className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-3">Hardcoded Logistics Pivot</h3>
                 <div className="glass-inner rounded-xl p-4 flex items-center justify-between border-l-4 border-l-brand-500">
                   <p className="text-lg font-mono text-white">{responseData?.suggested_action}</p>
                   <button className="px-4 py-2 bg-slate-800 hover:bg-brand-600 transition-colors rounded-lg text-sm font-semibold">Execute Webhook</button>
                 </div>
               </div>

               {/* Drafting Blocks */}
               <div className="grid grid-cols-1 md:grid-cols-2 gap-4 z-10 mt-2">
                 <div className="flex flex-col gap-2">
                   <h3 className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Native English Draft</h3>
                   <div className="glass-inner rounded-xl p-4 text-sm text-slate-300 leading-relaxed h-full">
                     {responseData?.draft_reply_en}
                   </div>
                 </div>
                 <div className="flex flex-col gap-2">
                   <h3 className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Fusha Arabic Translation</h3>
                   <div className="glass-inner rounded-xl p-4 text-sm text-slate-300 leading-relaxed font-arabic text-right h-full" dir="rtl">
                     {responseData?.draft_reply_ar}
                   </div>
                 </div>
               </div>

            </motion.div>
          )}
        </AnimatePresence>
      </div>

    </div>
  );
}
