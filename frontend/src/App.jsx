import React, { useEffect, useMemo, useState } from 'react';
import ArcReactor from './components/ArcReactor';
import useEdith from './hooks/useEdith';

const QUICK_COMMANDS = [
  'open github',
  'search youtube for arc reactor build',
  'set reminder team call at 7 PM',
  'what is the time',
];

function App() {
  const edithState = useEdith();
  const {
    isListening = false,
    isSpeaking = false,
    isProcessing = false,
    startListening = () => {},
    submitCommand = () => {},
    speechSupported = true,
    messages = [],
  } = edithState || {};

  const [manualCommand, setManualCommand] = useState('');

  const latest = messages[messages.length - 1];
  const cpuState = isProcessing || isSpeaking ? 'HIGH LOAD' : isListening ? 'AUDIO ACTIVE' : 'STABLE';
  const networkState = latest?.text?.toLowerCase().includes("can't reach the backend") ? 'DEGRADED' : 'SECURE';
  const mode = isProcessing ? 'PROCESSING' : isSpeaking ? 'RESPONSE MODE' : isListening ? 'ACTIVE LISTEN' : 'PASSIVE SCAN';

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

  const executeManualCommand = (e) => {
    e.stopPropagation();
    const trimmed = manualCommand.trim();
    if (!trimmed) return;
    submitCommand(trimmed);
    setManualCommand('');
  };

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
        {!speechSupported && <div className="warning">Speech recognition unsupported: use manual command mode.</div>}
      </div>

      <ArcReactor isListening={isListening || isProcessing} isSpeaking={isSpeaking} />

      <div className="right-panel">
        <h3>QUICK COMMANDS</h3>
        {QUICK_COMMANDS.map((cmd) => (
          <button
            key={cmd}
            className="quick-command"
            onClick={(e) => {
              e.stopPropagation();
              submitCommand(cmd);
            }}
            type="button"
          >
            {`Hey Edith, ${cmd}`}
          </button>
        ))}

        <div className="manual-console">
          <input
            value={manualCommand}
            onChange={(e) => setManualCommand(e.target.value)}
            onClick={(e) => e.stopPropagation()}
            placeholder="Type command..."
          />
          <button type="button" onClick={executeManualCommand}>
            EXECUTE
          </button>
        </div>
      </div>

      <div className="message-container">
        {messages.slice(-4).map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.sender === 'edith' ? 'EDITH: ' : 'YOU: '}
            {msg.text}
          </div>
        ))}
      </div>

      <div className="instructions">TAP ANYWHERE OR PRESS CTRL+SPACE • SAY “HEY EDITH” • OR TYPE COMMAND</div>
    </div>
  );
}

export default App;
