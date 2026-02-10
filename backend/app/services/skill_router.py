from ..skills.math_skill import MathSkill
from ..skills.system_skill import SystemSkill
from ..skills.productivity import ProductivitySkill
from .gemini import generate_response
from .chat_service import ChatService
import re

class SkillRouter:
    @staticmethod
    async def route(user_input: str):
        user_input_lower = user_input.lower().strip()
        
        # Save User Message to DB
        ChatService.add_message(role="user", content=user_input)

        response_data = {"type": "chat", "response": ""}

        # 0. VISION / SCREENSHOT (Priority)
        if "look at" in user_input_lower or "what is on my screen" in user_input_lower or "read this code" in user_input_lower or "scan this" in user_input_lower:
             screenshot_path = SystemSkill.capture_screen()
             if screenshot_path:
                  resp_text = await generate_response(user_input, image_path=screenshot_path)
                  response_data = {"type": "chat", "response": resp_text}
             else:
                  response_data = {"type": "chat", "response": "I couldn't see the screen."}

        # 1. MATH SKILL (Deterministic)
        elif MathSkill.is_match(user_input_lower):
            resp_text = MathSkill.execute(user_input_lower)
            response_data = {"type": "action", "response": resp_text}

        # 2. SYSTEM SKILL (Deterministic)
        elif "stop" in user_input_lower or "shut up" in user_input_lower:
            response_data = {"type": "stop", "response": "Stopping."}
            
        elif "open" in user_input_lower:
            target = user_input_lower.replace("open", "").strip()
            if "youtube" in target:
                 resp_text = SystemSkill.open_website("youtube.com")
            elif "website" in target or ".com" in target:
                 resp_text = SystemSkill.open_website(target)
            else:
                 resp_text = SystemSkill.open_application(target)
            response_data = {"type": "action", "response": resp_text}
            
        elif "close" in user_input_lower:
            target = user_input_lower.replace("close", "").strip()
            resp_text = SystemSkill.close_application(target)
            response_data = {"type": "action", "response": resp_text}
            
        elif "search" in user_input_lower or "google" in user_input_lower:
             query = user_input_lower.replace("search", "").replace("google", "").replace("for", "").strip()
             resp_text = SystemSkill.search_google(query)
             response_data = {"type": "action", "response": resp_text}
             
        elif "play" in user_input_lower:
             query = user_input_lower.replace("play", "").strip()
             resp_text = SystemSkill.play_music(query)
             response_data = {"type": "action", "response": resp_text}
             
        elif "shutdown" in user_input_lower:
             resp_text = SystemSkill.shutdown_system()
             response_data = {"type": "action", "response": resp_text}
             
        elif "sleep" in user_input_lower and "mode" in user_input_lower:
             resp_text = SystemSkill.sleep_system()
             response_data = {"type": "action", "response": resp_text}

        # 3. PRODUCTIVITY SKILL
        elif "todo" in user_input_lower:
             resp_text = ProductivitySkill.execute(user_input_lower)
             response_data = {"type": "action", "response": resp_text}

        # 4. FALLBACK TO GEMINI (The Brain)
        else:
             # Get history from DB
             history = ChatService.format_history_for_gemini(limit=10)
             resp_text = await generate_response(user_input, history=history)
             response_data = {"type": "chat", "response": resp_text}

        # Save Assistant Response to DB
        # Note: If response is a dict (like stop), the text is in "response" key
        final_text = response_data.get("response", str(response_data))
        ChatService.add_message(role="assistant", content=final_text)
        
        return response_data
