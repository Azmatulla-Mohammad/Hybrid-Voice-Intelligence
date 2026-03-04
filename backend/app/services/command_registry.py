from dataclasses import dataclass
from typing import Callable, Optional

from ..skills.system_skill import SystemSkill
from ..skills.productivity import ProductivitySkill


@dataclass
class CommandRule:
    name: str
    matcher: Callable[[str], bool]
    handler: Callable[[str], dict]


class CommandRegistry:
    """Registry for deterministic, local-first commands."""

    def __init__(self) -> None:
        self._rules: list[CommandRule] = []

    def register(self, rule: CommandRule) -> None:
        self._rules.append(rule)

    def resolve(self, text: str) -> Optional[dict]:
        for rule in self._rules:
            if rule.matcher(text):
                return rule.handler(text)
        return None


REGISTRY = CommandRegistry()


# ---- Built-in command rules ----
REGISTRY.register(
    CommandRule(
        name="stop",
        matcher=lambda t: any(k in t for k in ("stop", "shut up", "silence")),
        handler=lambda _: {"type": "stop", "response": "Stopping."},
    )
)


REGISTRY.register(
    CommandRule(
        name="open",
        matcher=lambda t: t.startswith("open "),
        handler=lambda t: _handle_open(t),
    )
)

REGISTRY.register(
    CommandRule(
        name="close",
        matcher=lambda t: t.startswith("close "),
        handler=lambda t: {
            "type": "action",
            "response": SystemSkill.close_application(t.replace("close", "", 1).strip()),
        },
    )
)

REGISTRY.register(
    CommandRule(
        name="search",
        matcher=lambda t: "search" in t or "google" in t,
        handler=lambda t: {
            "type": "action",
            "response": SystemSkill.search_google(
                t.replace("search", "").replace("google", "").replace("for", "").strip()
            ),
        },
    )
)

REGISTRY.register(
    CommandRule(
        name="play",
        matcher=lambda t: t.startswith("play "),
        handler=lambda t: {
            "type": "action",
            "response": SystemSkill.play_music(t.replace("play", "", 1).strip()),
        },
    )
)

REGISTRY.register(
    CommandRule(
        name="shutdown",
        matcher=lambda t: "shutdown" in t,
        handler=lambda _: {"type": "action", "response": SystemSkill.shutdown_system()},
    )
)

REGISTRY.register(
    CommandRule(
        name="sleep_mode",
        matcher=lambda t: "sleep" in t and "mode" in t,
        handler=lambda _: {"type": "action", "response": SystemSkill.sleep_system()},
    )
)


REGISTRY.register(
    CommandRule(
        name="todo",
        matcher=lambda t: "todo" in t,
        handler=lambda t: {"type": "action", "response": ProductivitySkill.execute(t)},
    )
)

REGISTRY.register(
    CommandRule(
        name="system_info",
        matcher=lambda t: "system info" in t or "system status" in t,
        handler=lambda _: {"type": "action", "response": SystemSkill.get_system_info()},
    )
)


# Keep helper at bottom to improve readability in command declarations above.
def _handle_open(text: str) -> dict:
    target = text.replace("open", "", 1).strip()
    if "youtube" in target:
        response = SystemSkill.open_website("youtube.com")
    elif "website" in target or any(ext in target for ext in (".com", ".org", ".net")):
        response = SystemSkill.open_website(target.replace("website", "").strip())
    else:
        response = SystemSkill.open_application(target)
    return {"type": "action", "response": response}
