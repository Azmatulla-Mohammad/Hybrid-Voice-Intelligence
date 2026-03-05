import asyncio
from pathlib import Path

from ..core.config import settings
from ..core.logging import get_logger

logger = get_logger(__name__)

try:
    from google import genai
    from google.genai import types
except Exception:  # noqa: BLE001
    genai = None
    types = None

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

if settings.GEMINI_API_KEY and genai is not None:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
else:
    client = None


def _build_text_prompt(prompt: str, history: list | None) -> str:
    if not history:
        return prompt

    chunks: list[str] = []
    for item in history[-10:]:
        role = item.get("role", "user")
        parts = item.get("parts", [])
        text = " ".join(str(p) for p in parts)
        chunks.append(f"{role}: {text}")

    chunks.append(f"user: {prompt}")
    return "\n".join(chunks)


async def generate_response(prompt: str, image_path: str = None, history: list | None = None):
    if client is None:
        if genai is None:
            return "AI mode is unavailable because google-genai is not installed."
        return "AI mode is unavailable because GEMINI_API_KEY is not configured."

    max_retries = 3
    base_delay = 2

    for attempt in range(max_retries):
        try:
            contents = []
            full_prompt = _build_text_prompt(prompt, history)
            contents.append(full_prompt)

            if image_path:
                img_bytes = Path(image_path).read_bytes()
                contents.append(
                    types.Part.from_bytes(
                        data=img_bytes,
                        mime_type="image/png",
                    )
                )

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )

            if getattr(response, "text", None):
                return response.text

            return "I processed that request but did not receive a text response."

        except Exception as exc:  # noqa: BLE001
            if "429" in str(exc) and attempt < max_retries - 1:
                delay = base_delay * (2**attempt)
                logger.warning("429 from Gemini API. Retrying in %ss", delay)
                await asyncio.sleep(delay)
                continue

            logger.exception("Gemini call failed", exc_info=exc)
            return "I couldn't reach the AI service, so I can only run local commands right now."
