import os

class Config:
    SUPPORTED_FORMATS = {'.mp3', '.wav', '.mp4', '.mkv', '.mov', '.flv', '.aac', '.m4a'}
    WATCH_DIRECTORY = "./media"
    PROCESSED_FILES_LOG = "processed_files.txt"
    SESSION_STATE_PATH = "session_state.json"  # New: Path for session state

os.makedirs(Config.WATCH_DIRECTORY, exist_ok=True)