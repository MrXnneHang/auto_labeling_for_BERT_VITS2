import os
import shutil
from pathlib import Path

from tqdm import tqdm
from utils.clip import clip_wav
from utils.util import get_file_list

from label._dataclass import RunnerSettings
from label.basic_runner.converter import convert_asr_response_to_sentences
from label.utils.config import load_settings_file
from label.utils.model import FunASRModel, generate_asr_results

"""
单人说话音频处理的第一步:
这步会把音频中的空白背景音全部去掉，并且按照有说话的句子排列，每个句子之间间隔为1.5s
对于不怎么健谈的游戏主播来说，这一步可能会把原本半小时的音频变成五分钟。
这步可以减少很多降噪的时间。
我把它叫做clip，我英文不好。
"""


def run_clip(file_path: Path):
    """
    生成音频中的起始点和终止点
    合并较近但是被分开的两个句子，比如[300,2600],[3200,4500],合并依据，combine_line . 3200 - 2600 < combine_line,则合并
    根据新的起始点和终止点clip音频
    """
    config: RunnerSettings = load_settings_file("config.toml", RunnerSettings)
    Model = FunASRModel()
    model = Model.vad_and_asr()
    response = generate_asr_results(model=model, input_path=file_path)
    sentences = convert_asr_response_to_sentences(
        response=response, max_sentence_length=config.max_sentence_length
    )

    clip_wav(
        sentences=sentences,
        input_path=file_path,
        output_path=Path(config.output_dir) / f"{file_path.stem}_clip.wav",
    )


def main():
    # 待处理的所有文件
    file_paths = get_file_list("./raw_audio/")
    print(f"raw_audio:{file_paths}")
    if len(file_paths) == 0:
        print("无待处理音频")
        exit()
    ask = input("请确保待处理的音频已经放在./raw_audio下方y/n:")

    # run clip
    if ask == "y":
        print("开始处理")
        for file_path in tqdm(file_paths):
            print(f"processing {file_path} --------------------------")
            run_clip(file_path=file_path)
        # clip完成后删除掉这个wav  //因为正在开发，一个视频需要多次对比，所以并不删除，投入使用的时候可以考虑把for循环的注释删掉。
        print("All clips were done")
    else:
        return


if __name__ == "__main__":
    main()
