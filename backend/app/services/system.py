import os
import subprocess
import webbrowser
import platform

class SystemService:
    @staticmethod
    def open_application(app_name: str):
        app_name = app_name.lower().strip()
        
        # Common App Map (Name -> Command/URI)
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
                os.system(f"start {cmd}")
                return f"Opening {app_name}."
            else:
                # Fallback: Try generic start command (Windows Run behavior)
                os.system(f"start {app_name}")
                return f"Attempting to launch {app_name}..."
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"

    @staticmethod
    def open_website(url: str):
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Opening {url}."

    @staticmethod
    def search_google(query: str):
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searching Google for {query}."

    @staticmethod
    def play_music(query: str):
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        return f"Playing music: {query} on YouTube."

    @staticmethod
    def sleep_system():
        system = platform.system()
        if system == "Windows":
             os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting system to sleep."

    @staticmethod
    def shutdown_system():
        system = platform.system()
        if system == "Windows":
             os.system("shutdown /s /t 1")
        return "Shutting down system."

    @staticmethod
    def close_application(app_name: str):
        app_name = app_name.lower().strip()
        system = platform.system()
        
        if system == "Windows":
            # Map common names to process names
            process_map = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "chrome": "chrome.exe",
                "code": "Code.exe",
                "vscode": "Code.exe",
                "spotify": "Spotify.exe",
                "camera": "WindowsCamera.exe",
                "cmd": "cmd.exe",
            }
            
            process_name = process_map.get(app_name, f"{app_name}.exe")
            
            try:
                # /F = Force, /IM = Image Name
                subprocess.run(["taskkill", "/F", "/IM", process_name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Closed {app_name}."
            except subprocess.CalledProcessError:
                return f"Could not close {app_name}. Is it running?"
        return "OS not fully supported."

    @staticmethod
    def capture_screen():
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            # Save to a temporary file
            temp_path = os.path.join(os.getcwd(), "screenshot_temp.png")
            screenshot.save(temp_path)
            return temp_path
        except ImportError:
            return None
        except Exception as e:
            return None
