# file_scanner.py
import os
from config import Config

class FileScanner:
    def __init__(self):
        self.processed_files = self._load_processed_files()

    def _load_processed_files(self):
        """Load previously processed files from log"""
        try:
            with open(Config.PROCESSED_FILES_LOG, 'r') as f:
                return set(line.strip() for line in f)
        except FileNotFoundError:
            return set()

    def save_processed_file(self, file_path):
        """Save processed file path to log"""
        self.processed_files.add(file_path)
        with open(Config.PROCESSED_FILES_LOG, 'a') as f:
            f.write(f"{file_path}\n")

    def scan_directory(self):
        """Recursively scan directory for supported media files"""
        media_files = []
        for root, _, files in os.walk(Config.WATCH_DIRECTORY):
            for file in files:
                file_path = os.path.join(root, file)
                if (os.path.splitext(file.lower())[1] in Config.SUPPORTED_FORMATS and 
                    file_path not in self.processed_files):
                    media_files.append(file_path)
        return media_files