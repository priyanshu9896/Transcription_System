import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from file_scanner import FileScanner
from transcriber import Transcriber
from session_manager import SessionManager
from config import Config

class FileHandler(FileSystemEventHandler):
    def __init__(self, transcriber, scanner, session_manager):
        self.transcriber = transcriber
        self.scanner = scanner
        self.session_manager = session_manager

    def on_created(self, event):
        """Handle new file creation"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        file_ext = os.path.splitext(file_path.lower())[1]
        
        if file_ext in Config.SUPPORTED_FORMATS:
            time.sleep(1)  # Wait for file to be fully written
            if file_path not in self.scanner.processed_files:
                self.session_manager.add_pending_file(file_path)
                success, output_file = self.transcriber.transcribe_file(file_path)
                if success:
                    self.scanner.save_processed_file(file_path)
                    self.session_manager.remove_pending_file(file_path)
                    self.session_manager.update_last_file(file_path)
                    print(f"Transcribed: {file_path} -> {output_file}")

class DirectoryMonitor:
    def __init__(self, transcriber, scanner, session_manager):
        self.observer = Observer()
        self.handler = FileHandler(transcriber, scanner, session_manager)
        self.session_manager = session_manager

    def start_monitoring(self, directory):
        """Start monitoring with session resume"""
        self.observer.schedule(self.handler, directory, recursive=True)
        self.observer.start()
        print(f"Started monitoring: {directory}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_monitoring()

    def stop_monitoring(self):
        """Stop monitoring"""
        self.observer.stop()
        self.observer.join()
        print("Monitoring stopped")