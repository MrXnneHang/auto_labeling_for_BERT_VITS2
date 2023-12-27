from pydub import AudioSegment
import os
from tqdm import tqdm

def merge_audio(files, output_dir, silence_duration=2000, max_length=10*60*1000):
    files = [file.split("|")[0] for file in files]
    silence = AudioSegment.silent(duration=silence_duration)
    combined = AudioSegment.empty()
    output_index = 1

    for file in tqdm(files):
        audio = AudioSegment.from_wav(file)
        if len(combined) + len(audio) > max_length:
            combined.export(os.path.join(output_dir, f"output_{output_index}.wav"), format='wav')
            combined = AudioSegment.empty()
            output_index += 1
        combined += audio + silence

    if len(combined) > 0:
        combined.export(os.path.join(output_dir, f"output_{output_index}.wav"), format='wav')


