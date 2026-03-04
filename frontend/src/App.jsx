import React, { useEffect, useMemo } from 'react';
import ArcReactor from './components/ArcReactor';
import useEdith from './hooks/useEdith';

const QUICK_COMMANDS = [
  'Hey Edith, open github',
  'Hey Edith, search youtube for arc reactor build',
  'Hey Edith, set reminder team call at 7 PM',
  'Hey Edith, what is the time',
];

function App() {
  const { isListening, isSpeaking, startListening, submitCommand, messages } = useEdith();

  const latest = messages[messages.length - 1];
  const cpuState = isSpeaking ? 'HIGH LOAD' : isListening ? 'AUDIO ACTIVE' : 'STABLE';
  const networkState = latest?.text?.toLowerCase().includes("can't reach the backend") ? 'DEGRADED' : 'SECURE';
  const mode = isListening ? 'ACTIVE LISTEN' : isSpeaking ? 'RESPONSE MODE' : 'PASSIVE SCAN';

  const telemetry = useMemo(
    () => [
      { label: 'VOICE MODE', value: mode },
      { label: 'CPU PROFILE', value: cpuState },
      { label: 'NETWORK', value: networkState },
      { label: 'COMMANDS PROCESSED', value: String(messages.length) },
    ],
    [mode, cpuState, networkState, messages.length]
  );

  useEffect(() => {
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
      <div className="bg-grid" />
      <div className="hud-overlay">
        <div className="hud-box top-left">EDITH Mk.II • ONLINE</div>
        <div className="hud-box top-right">STARK PROTOCOL • VERONICA</div>
        <div className="hud-box bottom-left">MISSION: AUTOMATE THE HEAVY WORK</div>
        <div className="hud-box bottom-right">WAKE WORD: HEY EDITH</div>
      </div>

      <div className="left-panel">
        <h3>TACTICAL TELEMETRY</h3>
        {telemetry.map((item) => (
          <div className="telemetry-row" key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </div>
        ))}
      </div>

      <ArcReactor isListening={isListening} isSpeaking={isSpeaking} />

      <div className="right-panel">
        <h3>QUICK COMMANDS</h3>
        {QUICK_COMMANDS.map((cmd) => (
          <button
            key={cmd}
            className="quick-command"
            onClick={(e) => {
              e.stopPropagation();
              submitCommand(cmd.replace('Hey Edith, ', ''));
            }}
            type="button"
          >
            {cmd}
          </button>
        ))}
      </div>

      <div className="message-container">
        {messages.slice(-4).map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.sender === 'edith' ? 'EDITH: ' : 'YOU: '}
            {msg.text}
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
