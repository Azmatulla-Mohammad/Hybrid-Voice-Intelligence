import json
import os
from datetime import datetime

class ProductivitySkill:
    DB_FILE = "productivity_db.json"

    @staticmethod
    def _load_db():
        if not os.path.exists(ProductivitySkill.DB_FILE):
            return {"todos": [], "habits": []}
        try:
            with open(ProductivitySkill.DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {"todos": [], "habits": []}

    @staticmethod
    def _save_db(data):
        with open(ProductivitySkill.DB_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def execute(command: str) -> str:
        data = ProductivitySkill._load_db()
        command = command.lower()

        # TODO Logic
        if "add todo" in command or "add to todo" in command:
            item = command.replace("add todo", "").replace("add to todo", "").strip()
            data["todos"].append({"task": item, "created_at": str(datetime.now()), "done": False})
            ProductivitySkill._save_db(data)
            return f"Added '{item}' to your to-do list."
        
        if "list todo" in command or "show todo" in command or "my todos" in command:
            pending = [t["task"] for t in data["todos"] if not t["done"]]
            if not pending: return "You have no pending tasks."
            return "Your To-Dos:\n" + "\n".join([f"- {t}" for t in pending])

        if "complete todo" in command or "finish todo" in command:
            item = command.replace("complete todo", "").replace("finish todo", "").strip()
            for t in data["todos"]:
                if item in t["task"].lower():
                    t["done"] = True
                    ProductivitySkill._save_db(data)
                    return f"Marked '{t['task']}' as done."
            return f"Could not find task '{item}'."

        return "Productivity command not recognized."
