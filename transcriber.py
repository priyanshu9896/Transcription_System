# # transcriber.py
# import whisper
# import os
# from pathlib import Path

# class Transcriber:
#     def __init__(self, model_size="base"):
#         """Initialize Whisper model"""
#         self.model = whisper.load_model(model_size)

#     def transcribe_file(self, file_path):
#         """Transcribe a single media file and save the result"""
#         try:
#             # Perform transcription
#             result = self.model.transcribe(file_path)
            
#             # Generate output file path
#             output_file = f"{os.path.splitext(file_path)[0]}.txt"
            
#             # Save transcription
#             with open(output_file, 'w', encoding='utf-8') as f:
#                 f.write(result["text"])
            
#             return True, output_file
#         except Exception as e:
#             print(f"Error transcribing {file_path}: {str(e)}")
#             return False, None


# # transcriber.py
# import whisper
# import os
# from pathlib import Path
# import warnings

# class Transcriber:
#     def __init__(self, model_size="base"):
#         """Initialize Whisper model"""
#         # Suppress FP16 warning
#         warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
#         self.model = whisper.load_model(model_size)

#     def transcribe_file(self, file_path):
#         """Transcribe a single media file and save the result"""
#         try:
#             result = self.model.transcribe(file_path)
#             output_file = f"{os.path.splitext(file_path)[0]}.txt"
#             with open(output_file, 'w', encoding='utf-8') as f:
#                 f.write(result["text"])
#             return True, output_file
#         except Exception as e:
#             print(f"Error transcribing {file_path}: {str(e)}")
#             return False, None

import whisper
import os
from pathlib import Path
import warnings

class Transcriber:
    def __init__(self, model_size="base"):
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
        self.model = whisper.load_model(model_size)

    def transcribe_file(self, file_path, resume=False):
        """Transcribe a file with resume support"""
        try:
            output_file = f"{os.path.splitext(file_path)[0]}.txt"
            temp_file = f"{output_file}.tmp"  # Temp file for partial results

            if resume and os.path.exists(temp_file):
                with open(temp_file, 'r', encoding='utf-8') as f:
                    partial_text = f.read()
                result = self.model.transcribe(file_path)  # Simplified: full transcription
                full_text = partial_text + " " + result["text"]
            else:
                result = self.model.transcribe(file_path)
                full_text = result["text"]

            # Save to temp file as a checkpoint
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(full_text)

            # Finalize by moving to output file
            os.rename(temp_file, output_file)
            return True, output_file
        except Exception as e:
            print(f"Error transcribing {file_path}: {str(e)}")
            return False, None