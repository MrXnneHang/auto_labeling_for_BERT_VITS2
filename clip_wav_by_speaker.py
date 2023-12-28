from pydub import AudioSegment
import re
from tqdm import tqdm
import os

def clip_wav_with_speaker(wav_name):
    # 读取文本文件并解析时间戳和说话者
    timestamps = []
    speakers = set()
    with open(f'./tmp/final_with_speaker_{wav_name}.txt', 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r'(\d+)\|(\d+)\|(\w+)?\|', line)
            if match:
                start, end, speaker = int(match.group(1)), int(match.group(2)), match.group(3)
                if speaker is None:
                    speaker = 'None'
                speakers.add(speaker)
                timestamps.append((start, end, speaker))

    # 创建每个说话者的音频对象
    audio = AudioSegment.from_wav(f'./raw_audio/{wav_name}.wav')
    speaker_audios = {speaker: AudioSegment.silent(duration=0) for speaker in speakers}

    # 处理音频
    for start, end, speaker in tqdm(timestamps, desc="处理进度"):
        segment = audio[start:end]
        speaker_audios[speaker] += AudioSegment.silent(duration=500)  # 添加0.5秒空白
        speaker_audios[speaker] += segment
        speaker_audios[speaker] += AudioSegment.silent(duration=1500)  # 添加1.5秒空白

    # 为每个说话者创建文件夹并保存音频
    for speaker, audio_segment in speaker_audios.items():
        speaker_dir = f'./tmp/split_speaker_{wav_name}/{speaker}'
        os.makedirs(speaker_dir, exist_ok=True)
        audio_segment.export(f'{speaker_dir}/{wav_name}.wav', format='wav')
