from .gemini import generate_response
from .system import SystemService
import re

class RouterService:
    @staticmethod
    async def process_input(user_input: str):
        # 1. Clean input: lowercase and remove trailing punctuation
        user_input_lower = re.sub(r'[^\w\s]', '', user_input.lower()).strip()
        
        # 2. Stop command (Highest Priority)
        if "stop" in user_input_lower or "shut up" in user_input_lower or "silence" in user_input_lower:
            return {"type": "stop", "response": "Stopping."}

        # 3. System Controls
        if "sleep" in user_input_lower and "mode" in user_input_lower:
             return {"type": "action", "response": SystemService.sleep_system()}
        
        if "shutdown" in user_input_lower and "system" in user_input_lower:
             return {"type": "action", "response": SystemService.shutdown_system()}

        # 4. Web Search & Media (Higher priority than generic 'open')
        # Check for 'search google for X' or 'google X'
        if "google" in user_input_lower:
             # Extract query cleanly
             query = user_input_lower.replace("search", "").replace("google", "").replace("for", "").strip()
             if not query: 
                 return {"type": "action", "response": SystemService.open_website("google.com")}
             return {"type": "action", "response": SystemService.search_google(query)}
        
        if "search for" in user_input_lower:
             query = user_input_lower.split("search for")[-1].strip()
             return {"type": "action", "response": SystemService.search_google(query)}

        if "play" in user_input_lower:
             query = user_input_lower.replace("play", "").strip()
             return {"type": "action", "response": SystemService.play_music(query)}

        # 5. Open/Close Apps/Websites
        if "close" in user_input_lower:
             target = user_input_lower.replace("close", "").strip()
             return {"type": "action", "response": SystemService.close_application(target)}

        if "open" in user_input_lower:
            target = user_input_lower.replace("open", "").strip()
            if "youtube" in target:
                 return {"type": "action", "response": SystemService.open_website("youtube.com")}
            if "website" in target or ".com" in target or ".org" in target or ".net" in target:
                 return {"type": "action", "response": SystemService.open_website(target)}
            else:
                 return {"type": "action", "response": SystemService.open_application(target)}
        
        # 6. Vision / Screen Analysis
        # Check for keywords related to sight + screen/context
        vision_keywords = ["see", "look", "what is on", "read", "analyze", "scan"]
        context_keywords = ["screen", "display", "code", "image", "this", "my view"]
        
        # Trigger if (vision_keyword AND context_keyword) OR specific phrases
        is_vision_request = False
        if any(v in user_input_lower for v in vision_keywords) and any(c in user_input_lower for c in context_keywords):
            is_vision_request = True
        elif "screenshot" in user_input_lower or "capture" in user_input_lower:
             is_vision_request = True

        if is_vision_request:
             screenshot_path = SystemService.capture_screen()
             if screenshot_path:
                  response = await generate_response(user_input, image_path=screenshot_path)
                  return {"type": "chat", "response": response}
             else:
                  return {"type": "chat", "response": "I tried to see your screen, but the visual sensors aren't responding."}

        # 7. Fallback to Gemini
        response = await generate_response(user_input)
        return {"type": "chat", "response": response}
