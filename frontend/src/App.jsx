import React, { useEffect } from 'react';
import ArcReactor from './components/ArcReactor';
import useEdith from './hooks/useEdith';


function App() {
  const { isListening, isSpeaking, startListening, messages } = useEdith();

  // Auto-start listening on load or key press (optional)
  useEffect(() => {
    // Add keyboard shortcut: Ctrl+Space to toggle listening
    const handleKeyDown = (e) => {
      if (e.ctrlKey && e.code === 'Space') {
        startListening();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [startListening]);

  return (
    <div className="app-container" onClick={startListening}>
      <div className="hud-overlay">
        <div className="top-left">SYSTEM: ONLINE</div>
        <div className="top-right">PROTOCOL: VERONICA</div>
        <div className="bottom-left">CPU: STABLE</div>
        <div className="bottom-right">NET: SECURE</div>
      </div>

      <ArcReactor isListening={isListening} isSpeaking={isSpeaking} />

      <div className="message-container">
        {messages.slice(-3).map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.sender === 'edith' ? "EDITH: " : "YOU: "}{msg.text}
          </div>
        ))}
      </div>

      <div className="instructions">
        SAY "HEY EDITH" OR PRESS CTRL+SPACE TO SPEAK
      </div>
    </div>
  );
}

export default App;
