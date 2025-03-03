# utils.py
import os

def ensure_directory_exists(directory):
    """Ensure a directory exists, create it if it doesn't"""
    os.makedirs(directory, exist_ok=True)

def validate_file_path(file_path):
    """Validate if file exists and is accessible"""
    return os.path.exists(file_path) and os.access(file_path, os.R_OK)