import React from 'react';
import { motion } from 'framer-motion';
import '../styles/ArcReactor.css';

const ArcReactor = ({ isListening, isSpeaking }) => {
  return (
    <div className="arc-container">
      <motion.div
        className="arc-core"
        animate={{
          scale: isListening ? [1, 1.1, 1] : 1,
          boxShadow: isListening 
            ? "0px 0px 60px 20px rgba(0, 217, 255, 0.8)" 
            : "0px 0px 30px 10px rgba(0, 217, 255, 0.4)"
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        <div className="arc-ring outer-ring"></div>
        <div className="arc-ring inner-ring"></div>
        <div className="arc-center"></div>
      </motion.div>
      <div className="status-text">
        {isListening ? "LISTENING..." : isSpeaking ? "PROCESSING..." : "ONLINE"}
      </div>
    </div>
  );
};

export default ArcReactor;
