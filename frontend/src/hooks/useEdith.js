import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const useEdith = () => {
    const [isListening, setIsListening] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [messages, setMessages] = useState([]);
    const recognitionRef = useRef(null);

    useEffect(() => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognitionRef.current = new SpeechRecognition();
            recognitionRef.current.continuous = false;
            recognitionRef.current.lang = 'en-US';

            recognitionRef.current.onstart = () => setIsListening(true);
            recognitionRef.current.onend = () => setIsListening(false);

            recognitionRef.current.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                processCommand(transcript);
            };
        } else {
            console.error("Speech Recognition not supported in this browser.");
        }
    }, []);

    const processCommand = async (command) => {
        setMessages(prev => [...prev, { text: command, sender: 'user' }]);
        setIsSpeaking(true);

        try {
            const response = await axios.post('http://localhost:8000/chat', { message: command });
            const aiResponse = response.data.response; // Assuming backend structure

            setMessages(prev => [...prev, { text: aiResponse, sender: 'edith' }]);
            speak(aiResponse);
        } catch (error) {
            console.error("Error processing command:", error);
            const errorMsg = "I'm having trouble connecting to the network, sir.";
            speak(errorMsg);
        } finally {
            setIsSpeaking(false);
        }
    };

    const stopSpeaking = () => {
        if (window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
            setIsSpeaking(false);
        }
    };

    const speak = (text) => {
        stopSpeaking(); // Stop any current speech
        const utterance = new SpeechSynthesisUtterance(text);
        // Select a suitable voice if available (e.g., Google US English)
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(voice => voice.name.includes('Google US English')) || voices[0];
        if (preferredVoice) utterance.voice = preferredVoice;

        utterance.rate = 1.0;
        utterance.pitch = 1.0;

        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);

        window.speechSynthesis.speak(utterance);
    };

    const startListening = () => {
        if (recognitionRef.current && !isListening) {
            recognitionRef.current.start();
        }
    };

    return {
        isListening,
        isSpeaking,
        messages,
        startListening,
        stopSpeaking
    };
};

export default useEdith;
