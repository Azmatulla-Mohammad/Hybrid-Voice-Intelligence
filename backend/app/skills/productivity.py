import json
import os
from datetime import datetime


class ProductivitySkill:
    DB_FILE = "productivity_db.json"

    @staticmethod
    def _load_db():
        if not os.path.exists(ProductivitySkill.DB_FILE):
            return {"todos": [], "notes": [], "reminders": [], "timers": [], "alarms": []}
        try:
            with open(ProductivitySkill.DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"todos": [], "notes": [], "reminders": [], "timers": [], "alarms": []}

    @staticmethod
    def _save_db(data):
        with open(ProductivitySkill.DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def execute(command: str) -> str:
        data = ProductivitySkill._load_db()
        command = command.lower().strip()

        # ---- To-do ----
        if "add todo" in command or "add to todo" in command:
            item = command.replace("add todo", "").replace("add to todo", "").strip()
            if not item:
                return "Please tell me what to add to the to-do list."
            data["todos"].append({"task": item, "created_at": str(datetime.now()), "done": False})
            ProductivitySkill._save_db(data)
            return f"Added '{item}' to your to-do list."

        if "list todo" in command or "show todo" in command or "my todos" in command:
            pending = [t["task"] for t in data["todos"] if not t["done"]]
            if not pending:
                return "You have no pending tasks."
            return "Your To-Dos:\n" + "\n".join([f"- {t}" for t in pending])

        if "complete todo" in command or "finish todo" in command:
            item = command.replace("complete todo", "").replace("finish todo", "").strip()
            for todo in data["todos"]:
                if item and item in todo["task"].lower():
                    todo["done"] = True
                    ProductivitySkill._save_db(data)
                    return f"Marked '{todo['task']}' as done."
            return f"Could not find task '{item}'."

        # ---- Notes ----
        if command.startswith("save note") or command.startswith("take note"):
            note = command.replace("save note", "", 1).replace("take note", "", 1).strip()
            if not note:
                return "Please provide note content."
            data["notes"].append({"text": note, "created_at": str(datetime.now())})
            ProductivitySkill._save_db(data)
            return "Note saved."

        if "read notes" in command or "show notes" in command:
            if not data["notes"]:
                return "You don't have any saved notes yet."
            recent = data["notes"][-5:]
            formatted = "\n".join([f"- {n['text']}" for n in recent])
            return f"Recent notes:\n{formatted}"

        # ---- Reminders / Alarms / Timers (stored, not scheduled daemon) ----
        if command.startswith("set reminder"):
            reminder = command.replace("set reminder", "", 1).strip()
            if not reminder:
                return "Please include reminder details."
            data["reminders"].append({"text": reminder, "created_at": str(datetime.now())})
            ProductivitySkill._save_db(data)
            return f"Reminder saved: {reminder}."

        if command.startswith("set alarm"):
            alarm = command.replace("set alarm", "", 1).strip()
            if not alarm:
                return "Please provide an alarm time."
            data["alarms"].append({"time": alarm, "created_at": str(datetime.now())})
            ProductivitySkill._save_db(data)
            return f"Alarm saved for {alarm}."

        if command.startswith("start timer"):
            timer = command.replace("start timer", "", 1).strip() or "unspecified duration"
            data["timers"].append({"duration": timer, "created_at": str(datetime.now())})
            ProductivitySkill._save_db(data)
            return f"Timer noted for {timer}."

        return "Productivity command not recognized."
