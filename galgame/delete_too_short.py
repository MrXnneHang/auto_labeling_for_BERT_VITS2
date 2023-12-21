import os
from pydub import AudioSegment

def delete_short_audio_files(directory, min_length=500):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.lower().endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a')):
            try:
                audio = AudioSegment.from_file(filepath)
                if len(audio) < min_length:
                    os.remove(filepath)
                    print(f"Deleted '{filename}' as its length is less than 2 seconds.")
            except Exception as e:
                print(f"Error processing file '{filename}': {e}")

# 使用示例
directory = 'path/to/your/directory'
delete_short_audio_files(directory)
