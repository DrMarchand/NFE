import subprocess
import os

class GitGear:
    def __init__(self):
        self.repo_path = os.path.expanduser("~/lab")

    def chronicle(self, message):
        """Commits the current state to the permanent record."""
        try:
            print(f"📡 [GIT-GEAR] Chronicling to GitHub: {message}")
            subprocess.run(["git", "-C", self.repo_path, "add", "."], check=True)
            subprocess.run(["git", "-C", self.repo_path, "commit", "-m", message], check=True)
            # subprocess.run(["git", "-C", self.repo_path, "push"], check=True) 
            print("🟩 [GIT-GEAR] Chronicle Complete.")
        except Exception as e:
            print(f"🚨 [GIT-GEAR] Failed to chronicle: {e}")
