import React from 'react';
import { motion } from 'framer-motion';
import '../styles/ArcReactor.css';

const MotionDiv = motion.div;

const ArcReactor = ({ isListening, isSpeaking }) => {
  const mode = isListening ? 'LISTENING' : isSpeaking ? 'SPEAKING' : 'STANDBY';

  return (
    <div className="arc-container">
      <MotionDiv
        className={`arc-core ${isListening ? 'listening' : ''} ${isSpeaking ? 'speaking' : ''}`}
        animate={{
          scale: isListening ? [1, 1.08, 1] : isSpeaking ? [1, 1.04, 1] : 1,
        }}
        transition={{ duration: 1.4, repeat: Infinity, ease: 'easeInOut' }}
      >
        <div className="arc-ring outer-ring" />
        <div className="arc-ring mid-ring" />
        <div className="arc-ring inner-ring" />
        <div className="arc-center" />
      </MotionDiv>
      <div className="status-text">{mode}</div>
    </div>
  );
};

export default ArcReactor;
