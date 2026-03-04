from .gemini import generate_response
from .chat_service import ChatService
from .command_classifier import CommandClassifier
from .command_registry import REGISTRY
from ..skills.math_skill import MathSkill
from ..skills.system_skill import SystemSkill
from ..core.logging import get_logger

logger = get_logger(__name__)


class SkillRouter:
    @staticmethod
    async def route(user_input: str):
        normalized_input = user_input.lower().strip()
        ChatService.add_message(role="user", content=user_input)

        try:
            # 1) Vision/screenshot path
            if CommandClassifier.is_vision_request(normalized_input):
                screenshot_path = SystemSkill.capture_screen()
                if screenshot_path:
                    resp_text = await generate_response(user_input, image_path=screenshot_path)
                    response_data = {"type": "chat", "response": resp_text}
                else:
                    response_data = {
                        "type": "chat",
                        "response": "I couldn't access a screenshot from this environment.",
                    }

            # 2) Deterministic math
            elif CommandClassifier.is_math_request(normalized_input):
                response_data = {
                    "type": "action",
                    "response": MathSkill.execute(normalized_input),
                }

            # 3) Deterministic local command registry
            else:
                local_response = REGISTRY.resolve(normalized_input)
                if local_response is not None:
                    response_data = local_response
                else:
                    history = ChatService.format_history_for_gemini(limit=10)
                    resp_text = await generate_response(user_input, history=history)
                    response_data = {"type": "chat", "response": resp_text}

        except Exception as exc:
            logger.exception("Router error", exc_info=exc)
            response_data = {
                "type": "chat",
                "response": "I hit an internal issue while processing that. Please try again.",
            }

        ChatService.add_message(role="assistant", content=response_data.get("response", ""))
        return response_data
