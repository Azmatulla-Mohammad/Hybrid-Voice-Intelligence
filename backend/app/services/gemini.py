import asyncio
import google.generativeai as genai
import PIL.Image

from ..core.config import settings
from ..core.logging import get_logger

logger = get_logger(__name__)

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

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-lite-001", system_instruction=SYSTEM_PROMPT)
else:
    model = None


async def generate_response(prompt: str, image_path: str = None, history: list | None = None):
    if model is None:
        return "AI mode is unavailable because GEMINI_API_KEY is not configured."

    max_retries = 3
    base_delay = 2

    for attempt in range(max_retries):
        try:
            if image_path:
                img = PIL.Image.open(image_path)
                response = model.generate_content([prompt, img])
            else:
                chat = model.start_chat(history=history or [])
                response = chat.send_message(prompt)
            return response.text
        except Exception as exc:
            if "429" in str(exc) and attempt < max_retries - 1:
                delay = base_delay * (2**attempt)
                logger.warning("429 from Gemini API. Retrying in %ss", delay)
                await asyncio.sleep(delay)
                continue

            logger.exception("Gemini call failed", exc_info=exc)
            return "I couldn't reach the AI service, so I can only run local commands right now."
