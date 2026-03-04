from ..skills.math_skill import MathSkill


class CommandClassifier:
    """Classify raw text into deterministic paths before AI fallback."""

    VISION_HINTS = (
        "look at",
        "what is on my screen",
        "read this code",
        "scan this",
        "screenshot",
    )

    @classmethod
    def is_vision_request(cls, text: str) -> bool:
        text = text.lower().strip()
        return any(hint in text for hint in cls.VISION_HINTS)

    @staticmethod
    def is_math_request(text: str) -> bool:
        return MathSkill.is_match(text.lower().strip())
