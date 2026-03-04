import re
from dataclasses import dataclass
from typing import Callable, Optional

from ..skills.productivity import ProductivitySkill
from ..skills.system_skill import SystemSkill


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


def _action(response: str) -> dict:
    return {"type": "action", "response": response}


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
        name="system_datetime",
        matcher=lambda t: any(k in t for k in ("current date", "current time", "what time", "what is the time", "today date")),
        handler=lambda _: _action(SystemSkill.now_datetime()),
    )
)

REGISTRY.register(
    CommandRule(
        name="restart",
        matcher=lambda t: "restart" in t,
        handler=lambda _: _action(SystemSkill.restart_system()),
    )
)

REGISTRY.register(
    CommandRule(
        name="shutdown",
        matcher=lambda t: "shutdown" in t,
        handler=lambda _: _action(SystemSkill.shutdown_system()),
    )
)

REGISTRY.register(
    CommandRule(
        name="lock",
        matcher=lambda t: "lock" in t and "system" in t or "lock computer" in t,
        handler=lambda _: _action(SystemSkill.lock_system()),
    )
)

REGISTRY.register(
    CommandRule(
        name="sleep_mode",
        matcher=lambda t: "sleep" in t and "mode" in t,
        handler=lambda _: _action(SystemSkill.sleep_system()),
    )
)

REGISTRY.register(
    CommandRule(
        name="set_volume",
        matcher=lambda t: "volume" in t and ("set" in t or "%" in t),
        handler=lambda t: _action(_handle_volume(t)),
    )
)

REGISTRY.register(
    CommandRule(
        name="open_folder",
        matcher=lambda t: t.startswith("open folder") or t.startswith("open directory"),
        handler=lambda t: _action(
            SystemSkill.open_folder(
                t.replace("open folder", "", 1).replace("open directory", "", 1).strip()
            )
        ),
    )
)

REGISTRY.register(
    CommandRule(
        name="search_local_files",
        matcher=lambda t: t.startswith("search files") or t.startswith("find file"),
        handler=lambda t: _action(
            SystemSkill.search_local_files(
                t.replace("search files", "", 1).replace("find file", "", 1).replace("for", "").strip()
            )
        ),
    )
)

REGISTRY.register(
    CommandRule(
        name="open",
        matcher=lambda t: t.startswith("open "),
        handler=lambda t: _action(_handle_open(t)),
    )
)

REGISTRY.register(
    CommandRule(
        name="close",
        matcher=lambda t: t.startswith("close "),
        handler=lambda t: _action(SystemSkill.close_application(t.replace("close", "", 1).strip())),
    )
)

REGISTRY.register(
    CommandRule(
        name="youtube_search",
        matcher=lambda t: "youtube" in t and "search" in t,
        handler=lambda t: _action(
            SystemSkill.search_youtube(
                t.replace("search", "").replace("youtube", "").replace("for", "").strip()
            )
        ),
    )
)

REGISTRY.register(
    CommandRule(
        name="weather",
        matcher=lambda t: "weather" in t,
        handler=lambda t: _action(SystemSkill.get_weather(t.replace("weather", "").replace("in", "").strip())),
    )
)

REGISTRY.register(
    CommandRule(
        name="news",
        matcher=lambda t: "news" in t,
        handler=lambda t: _action(SystemSkill.get_news_headlines(t.replace("news", "").strip() or "latest")),
    )
)

REGISTRY.register(
    CommandRule(
        name="search_web",
        matcher=lambda t: "search" in t or "google" in t,
        handler=lambda t: _action(
            SystemSkill.search_google(
                t.replace("search", "").replace("google", "").replace("for", "").strip()
            )
        ),
    )
)

REGISTRY.register(
    CommandRule(
        name="play",
        matcher=lambda t: t.startswith("play ") or "play music" in t,
        handler=lambda t: _action(SystemSkill.play_music(t.replace("play", "", 1).strip())),
    )
)

REGISTRY.register(
    CommandRule(
        name="terminal",
        matcher=lambda t: t.startswith("run command") or t.startswith("terminal"),
        handler=lambda t: _action(
            SystemSkill.run_terminal_command(t.replace("run command", "", 1).replace("terminal", "", 1).strip())
        ),
    )
)

REGISTRY.register(
    CommandRule(
        name="productivity",
        matcher=lambda t: any(k in t for k in ("todo", "note", "reminder", "alarm", "timer")),
        handler=lambda t: _action(ProductivitySkill.execute(t)),
    )
)

REGISTRY.register(
    CommandRule(
        name="system_info",
        matcher=lambda t: "system info" in t or "system status" in t,
        handler=lambda _: _action(SystemSkill.get_system_info()),
    )
)


def _handle_open(text: str) -> str:
    target = text.replace("open", "", 1).strip()
    if "youtube" in target:
        return SystemSkill.open_website("youtube.com")
    if "github" in target:
        return SystemSkill.open_website("github.com")
    if "website" in target or any(ext in target for ext in (".com", ".org", ".net")):
        return SystemSkill.open_website(target.replace("website", "").strip())
    return SystemSkill.open_application(target)


def _handle_volume(text: str) -> str:
    match = re.search(r"(\d{1,3})", text)
    if not match:
        return "Please specify a volume percentage, for example set volume to 35."
    return SystemSkill.set_volume(int(match.group(1)))
