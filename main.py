from config import Config
from file_scanner import FileScanner
from transcriber import Transcriber
from monitor import DirectoryMonitor
from session_manager import SessionManager
from utils import ensure_directory_exists

def main():
    ensure_directory_exists(Config.WATCH_DIRECTORY)
    scanner = FileScanner()
    transcriber = Transcriber(model_size="base")
    session_manager = SessionManager()

    # Process existing files and resume pending ones
    print("Scanning for existing files...")
    existing_files = scanner.scan_directory()
    pending_files = session_manager.get_pending_files()

    all_files = list(set(existing_files + pending_files))  # Combine and remove duplicates
    for file_path in all_files:
        success, output_file = transcriber.transcribe_file(file_path, resume=True)
        if success:
            scanner.save_processed_file(file_path)
            session_manager.remove_pending_file(file_path)
            session_manager.update_last_file(file_path)
            print(f"Transcribed existing file: {file_path} -> {output_file}")

    # Start real-time monitoring
    monitor = DirectoryMonitor(transcriber, scanner, session_manager)
    monitor.start_monitoring(Config.WATCH_DIRECTORY)

if __name__ == "__main__":
    main()