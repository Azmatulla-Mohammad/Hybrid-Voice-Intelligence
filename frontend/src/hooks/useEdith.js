import { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';

const WAKE_WORDS = ['edith', 'hey edith'];

const useEdith = () => {
    const [isListening, setIsListening] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [messages, setMessages] = useState([]);
    const recognitionRef = useRef(null);

    const stopSpeaking = useCallback(() => {
        if (window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
            setIsSpeaking(false);
        }
    }, []);

    const speak = useCallback((text) => {
        stopSpeaking();
        const utterance = new SpeechSynthesisUtterance(text);
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find((voice) => voice.name.includes('Google US English')) || voices[0];
        if (preferredVoice) utterance.voice = preferredVoice;

        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);

        window.speechSynthesis.speak(utterance);
    }, [stopSpeaking]);

    const processCommand = useCallback(async (command) => {
        setMessages((prev) => [...prev, { text: command, sender: 'user' }]);

        try {
            const response = await axios.post('http://localhost:8000/chat', { message: command });
            const aiResponse = response.data.response;
            setMessages((prev) => [...prev, { text: aiResponse, sender: 'edith' }]);
            speak(aiResponse);
        } catch (error) {
            console.error('Error processing command:', error);
            const fallback = "I can't reach the backend right now. I can still listen for your next command.";
            setMessages((prev) => [...prev, { text: fallback, sender: 'edith' }]);
            speak(fallback);
        }
    }, [speak]);

    useEffect(() => {
        if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
            console.error('Speech Recognition not supported in this browser.');
            return undefined;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        recognitionRef.current = recognition;

        recognition.onstart = () => setIsListening(true);
        recognition.onend = () => {
            setIsListening(false);
            if (!isSpeaking) {
                try {
                    recognition.start();
                } catch (error) {
                    console.warn('Recognition restart skipped:', error);
                }
            }
        };

        recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.trim();
            const lower = transcript.toLowerCase();

            const hasWakeWord = WAKE_WORDS.some((wakeWord) => lower.startsWith(wakeWord));
            if (!hasWakeWord) return;

            const command = WAKE_WORDS.reduce((text, wakeWord) => {
                if (text.startsWith(wakeWord)) {
                    return text.slice(wakeWord.length).trim();
                }
                return text;
            }, lower);

            if (command.length > 0) {
                processCommand(command);
            }
        };

        try {
            recognition.start();
        } catch (error) {
            console.warn('Recognition start skipped:', error);
        }
        return () => recognition.stop();
    }, [isSpeaking, processCommand]);

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
        stopSpeaking,
    };
};

export default useEdith;
