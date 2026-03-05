import datetime
import os
import platform
import subprocess
import urllib.parse
import webbrowser


class SystemSkill:
    @staticmethod
    def open_application(app_name: str):
        app_name = app_name.lower().strip()
        system = platform.system()

        if system == "Windows":
            app_map = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "cmd": "start cmd",
                "command prompt": "start cmd",
                "code": "code",
                "vscode": "code",
                "explorer": "explorer",
                "chrome": "start chrome",
                "spotify": "spotify:",
                "camera": "microsoft.windows.camera:",
                "settings": "ms-settings:",
                "store": "ms-windows-store:",
                "whatsapp": "whatsapp:",
                "netflix": "netflix:",
            }

            try:
                if app_name in app_map:
                    cmd = app_map[app_name]
                    if cmd.startswith("start ") or cmd.endswith(":"):
                        os.system(f"start {cmd}")
                    else:
                        subprocess.Popen(cmd, shell=True)
                    return f"Opening {app_name}."

                os.system(f"start {app_name}")
                return f"Attempting to launch {app_name}."
            except Exception as exc:
                return f"Failed to open {app_name}: {str(exc)}"

        return "OS not fully supported."

    @staticmethod
    def close_application(app_name: str):
        app_name = app_name.lower().strip()
        system = platform.system()

        if system == "Windows":
            process_map = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "chrome": "chrome.exe",
                "code": "Code.exe",
                "vscode": "Code.exe",
                "spotify": "Spotify.exe",
                "windows camera": "WindowsCamera.exe",
                "camera": "WindowsCamera.exe",
            }
            process_name = process_map.get(app_name, f"{app_name}.exe")
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", process_name],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return f"Closed {app_name}."
            except Exception:
                return f"Could not close {app_name}."
        return "OS not fully supported."

    @staticmethod
    def open_website(url: str):
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Opening {url}."

    @staticmethod
    def search_google(query: str):
        if not query:
            webbrowser.open("https://www.google.com")
            return "Opening Google."
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}"
        webbrowser.open(url)
        return f"Searching Google for {query}."

    @staticmethod
    def search_youtube(query: str):
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        webbrowser.open(url)
        return f"Searching YouTube for {query}."

    @staticmethod
    def play_music(query: str):
        query = query or "music"
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        webbrowser.open(url)
        return f"Playing music: {query} on YouTube."

    @staticmethod
    def open_folder(path_or_name: str):
        target = path_or_name.strip().strip('"')
        if platform.system() == "Windows":
            os.system(f'start "" "{target}"')
            return f"Opening folder {target}."
        return "Folder opening is currently optimized for Windows."

    @staticmethod
    def search_local_files(term: str):
        if platform.system() == "Windows":
            os.system(f'start "" "search-ms:query={term}"')
            return f"Searching local files for {term}."
        return "Local file search is currently optimized for Windows."

    @staticmethod
    def restart_system():
        if platform.system() == "Windows":
            os.system("shutdown /r /t 1")
        return "Restarting system."

    @staticmethod
    def lock_system():
        if platform.system() == "Windows":
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "Locking your system."
        return "Lock system is currently optimized for Windows."

    @staticmethod
    def set_volume(level: int):
        if level < 0 or level > 100:
            return "Please provide a volume level between 0 and 100."
        # Placeholder without OS-specific dependency.
        return f"Volume command received: set to {level}%."

    @staticmethod
    def get_weather(location: str):
        query = location or "current location"
        webbrowser.open(f"https://www.google.com/search?q=weather+{urllib.parse.quote_plus(query)}")
        return f"Fetching weather for {query}."

    @staticmethod
    def get_news_headlines(topic: str = "latest"):
        query = f"{topic} news headlines"
        webbrowser.open(f"https://news.google.com/search?q={urllib.parse.quote_plus(query)}")
        return f"Fetching news headlines for {topic}."

    @staticmethod
    def now_datetime():
        now = datetime.datetime.now()
        return now.strftime("Today is %A, %d %B %Y. The current time is %I:%M %p.")

    @staticmethod
    def run_terminal_command(command: str):
        command = command.strip()
        if not command:
            return "Please provide a terminal command to run."
        try:
            completed = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=12)
            output = (completed.stdout or completed.stderr or "No output").strip()
            return f"Command exit code {completed.returncode}. Output: {output[:300]}"
        except Exception as exc:
            return f"Failed to run terminal command: {str(exc)}"

    @staticmethod
    def capture_screen():
        try:
            from PIL import ImageGrab

            screenshot = ImageGrab.grab()
            temp_path = os.path.join(os.getcwd(), "screenshot_temp.png")
            screenshot.save(temp_path)
            return temp_path
        except Exception:
            return None

    @staticmethod
    def get_system_info():
        return f"Running on {platform.system()} {platform.release()} ({platform.machine()})."

    @staticmethod
    def shutdown_system():
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")
        return "Shutting down system."

    @staticmethod
    def sleep_system():
        if platform.system() == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting system to sleep."
