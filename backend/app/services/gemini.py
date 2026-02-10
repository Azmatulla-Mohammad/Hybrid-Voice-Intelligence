import google.generativeai as genai
from ..core.config import settings
import PIL.Image

# Configuration
genai.configure(api_key=settings.GEMINI_API_KEY)

# Persona
SYSTEM_PROMPT = """
You are EDITH (Even Dead I'm The Hero), an advanced AI assistant.
Your goal is to be helpful, witty, and conversational, like a real human assistant.
Do not sound robotic. Use natural language, idioms, and humor where appropriate.
Keep responses concise (1-2 sentences) unless asked for a detailed explanation.
You represent the pinnacle of Stark technology. Be confident but polite.
**Capabilities**:
- You CAN see the user's screen when they ask (an image will be attached).
- You can control the system (Music, Apps, Shutdown).
If asked to do something you can't (like physical actions), explain clearly.
"""

model = genai.GenerativeModel('gemini-2.0-flash-lite-001', system_instruction=SYSTEM_PROMPT)

# Helper to manage chat sessions
# Retry decorator for 429 errors
import time
import asyncio

async def generate_response(prompt: str, image_path: str = None, history: list = []):
    max_retries = 3
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            if image_path:
                import PIL.Image
                img = PIL.Image.open(image_path)
                response = model.generate_content([prompt, img])
            else:
                chat = model.start_chat(history=history or [])
                response = chat.send_message(prompt)
                
            return response.text
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"429 Quota Exceeded. Retrying in {delay}s...")
                await asyncio.sleep(delay)
                continue
            return f"Error communicating with EDITH intelligence: {str(e)}"
