import os
import re
import subprocess
import time
from config import load_config

def generate_tts(text: str, output_path: str, voice: str = "en-US-ChristopherNeural", rate: str = "+15%"):
    config = load_config()
    
    # 1. Clean the text
    # Remove inner censor content for audio (e.g. s<censor>hit</censor> -> s)
    clean_text = re.sub(r'<censor>(.*?)</censor>', r'', text)
    # Remove pause tags (TTS engine doesn't support them natively in this script)
    clean_text = re.sub(r'<pause=.*?s>', '', clean_text).strip()
    
    # 2. Fallback for empty text (prevents 0-byte MP3 files)
    if not clean_text:
        print(f"  [TTS] Warning: Text for {os.path.basename(output_path)} is empty after cleaning. Using placeholder.")
        clean_text = "Keep reading." # Use a short phrase that is guaranteed to work

    # 3. Call edge-tts
    command = [
        "edge-tts",
        "--voice", voice,
        "--rate", rate,
        "--text", clean_text,
        "--write-media", output_path,
    ]
    
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    
    # 4. Error Checking
    if result.returncode != 0:
        print(f"  [TTS] Error generating audio: {result.stderr}")
    
    # Final check: if file was created but is 0 bytes, edge-tts didn't like the input
    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        print(f"  [TTS] Warning: Generated file for '{clean_text[:20]}' is 0 bytes or missing. Retrying with 'A'")
        fallback_cmd = [
            "edge-tts",
            "--voice", voice,
            "--rate", rate,
            "--text", "A",
            "--write-media", output_path,
        ]
        subprocess.run(fallback_cmd, check=False)