from pydub import AudioSegment
import re
from tqdm import tqdm


def clip_wav(wav_name):
    # 读取文本文件并解析时间戳
    timestamps = []
    with open('./tmp/08.txt', 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r'(\d+)\|(\d+)\|', line)
            if match:
                start, end = int(match.group(1)), int(match.group(2))
                timestamps.append((start, end))

    # 读取音频文件
    audio = AudioSegment.from_wav(f'{wav_name}.wav')
    processed_audio = AudioSegment.silent(duration=0)

    # 处理音频，移除静音部分，添加空白
    last_end = 0
    for start, end in tqdm(timestamps, desc="处理进度"):
            
        segment = audio[start:end+50]
        #processed_audio += AudioSegment.silent(duration=500)  # 添加0.5秒空白
        processed_audio += segment
        last_end = end

    # 保存新的音频文件
    processed_audio.export(f'./tmp/processed_{wav_name}.wav', format='wav')
