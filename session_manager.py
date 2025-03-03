import json
import os
from config import Config

class SessionManager:
    def __init__(self):
        self.state_file = Config.SESSION_STATE_PATH
        self.state = self._load_state()

    def _load_state(self):
        """Load session state"""
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"last_file": None, "pending_files": []}

    def save_state(self):
        """Save session state"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)

    def update_last_file(self, file_path):
        """Update last processed file"""
        self.state["last_file"] = file_path
        self.save_state()

    def add_pending_file(self, file_path):
        """Add file to pending list"""
        if file_path not in self.state["pending_files"]:
            self.state["pending_files"].append(file_path)
            self.save_state()

    def remove_pending_file(self, file_path):
        """Remove file from pending list"""
        if file_path in self.state["pending_files"]:
            self.state["pending_files"].remove(file_path)
            self.save_state()

    def get_pending_files(self):
        """Get pending files"""
        return self.state["pending_files"]