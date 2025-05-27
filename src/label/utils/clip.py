import re
from pathlib import Path

from pydub import AudioSegment
from tqdm import tqdm

from label._typing import Sentence


def clip_wav(
    sentences: list[Sentence],
    input_path: Path,
    output_path: Path,
    extend_length: int = 200,
):
    """
    根据起始点和终止点来去掉空白（没有人声）的音频片段。
    """
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # 读取音频文件
    audio = AudioSegment.from_wav(str(input_path))
    processed_audio = AudioSegment.silent(duration=0)

    # 处理音频，移除静音部分，添加空白
    for sentence in tqdm(sentences, desc="处理进度"):
        processed_audio += AudioSegment.silent(duration=500)
        # 剪辑时把起始点和终止点向外扩张 200ms , 防止截断.
        if extend_length + sentence["end"] >= len(audio):
            segment = audio[sentence["start"] - extend_length : -1]
        elif sentence["start"] - extend_length <= 0:
            segment = audio[0 : sentence["end"] + extend_length]
        else:
            segment = audio[
                sentence["start"] - extend_length : sentence["end"] + extend_length
            ]
        processed_audio += AudioSegment.silent(duration=1500)  # 添加1.5秒空白
        processed_audio += segment

    # 保存新的音频文件
    processed_audio.export(str(output_path), format="wav")
