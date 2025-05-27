from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from pydub import AudioSegment

from label._dataclass import RunnerSettings
from label.console.logger import Logger
from label.utils.config import load_settings_file

if TYPE_CHECKING:
    from label._typing import Sentence


def cut_wav(
    sentences: list[Sentence], input_path: Path, extend_length: int = 200
) -> Path:
    """
    根据传入的起始点和终止点把音频切片。
    """
    config = load_settings_file("config.toml", RunnerSettings)
    # 确保输出目录存在
    output_dir = Path(config.output_dir)
    output_dir = output_dir / "cut" / input_path.stem
    shutil.rmtree(str(output_dir), ignore_errors=True)
    # 确保每次运行都清空输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 加载原始音频文件
    audio = AudioSegment.from_wav(str(input_path))

    # 处理每一行，剪辑音频
    for index, sentence in enumerate(sentences):
        # 剪辑时把起始点和终止点向外扩张 200ms , 防止截断.
        if extend_length + sentence["end"] >= len(audio):
            cut = audio[sentence["start"] - extend_length : -1]
        elif sentence["start"] - extend_length <= 0:
            cut = audio[0 : sentence["end"] + extend_length]
        else:
            cut = audio[
                sentence["start"] - extend_length : sentence["end"] + extend_length
            ]

        # 保存剪辑后的音频
        output_path = output_dir / f"{input_path.stem}_{index + 1}.wav"
        cut.export(str(output_path), format="wav")

    Logger.info(f"音频剪辑完成，保存在目录：{output_dir}")
    return output_dir
