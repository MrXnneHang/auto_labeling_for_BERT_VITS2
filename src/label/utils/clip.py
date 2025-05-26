import re
from pathlib import Path

from pydub import AudioSegment
from tqdm import tqdm

from label._typing import Sentence


def clip_wav(sentences: list[Sentence], input_path: Path, output_path: Path):
    """
    根据起始点和终止点来去掉空白（没有人声）的音频片段。
    """
    # 读取音频文件
    audio = AudioSegment.from_wav(str(input_path))
    processed_audio = AudioSegment.silent(duration=0)

    # 处理音频，移除静音部分，添加空白
    last_end = 0
    for sentence in tqdm(sentences, desc="处理进度"):
        processed_audio += AudioSegment.silent(duration=500)
        segment = audio[sentence["start"] : sentence["end"]]
        processed_audio += AudioSegment.silent(duration=1500)  # 添加1.5秒空白
        processed_audio += segment
        last_end = sentence["end"]

    # 保存新的音频文件
    processed_audio.export(str(output_path), format="wav")
