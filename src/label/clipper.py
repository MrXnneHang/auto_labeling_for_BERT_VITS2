import os
import shutil
from pathlib import Path

from tqdm import tqdm
import sys

from label._dataclass import RunnerSettings
from label.basic_runner.converter import convert_asr_response_to_sentences
from label.utils.clip import clip_wav
from label.utils.config import load_settings_file
from label.utils.ffmpeg_helper import file_to_wav
from label.utils.model import FunASRModel, generate_asr_results
from label.utils.util import get_file_list
from label.console.logger import Logger
from label.basic_runner.cutter import cut_sentences
from label.basic_runner.combiner import combine_sentences


"""
单人说话音频处理的第一步:
这步会把音频中的空白背景音全部去掉，并且按照有说话的句子排列，每个句子之间间隔为1.5s
对于不怎么健谈的游戏主播来说，这一步可能会把原本半小时的音频变成五分钟。
这步可以减少很多降噪的时间。
我把它叫做clip，我英文不好。
"""

from rich.console import Console
from rich.text import Text

def show_histogram_in_terminal(duration_list, bins=10, max_height=10):

    total_count = len(duration_list)
    if total_count > 0:
        under_2s = sum(1 for d in duration_list if d < 2)
        between_2_5s = sum(1 for d in duration_list if 2 <= d < 5)
        between_5_10s = sum(1 for d in duration_list if 5 <= d < 10)
        over_10s = sum(1 for d in duration_list if d >= 10)
        
        Logger.info("\nPercentage Distribution:")
        Logger.info(f"  < 2s   : {under_2s / total_count * 100:.1f}% ({under_2s} items)")
        Logger.info(f"  2-5s   : {between_2_5s / total_count * 100:.1f}% ({between_2_5s} items)")
        Logger.info(f"  5-10s  : {between_5_10s / total_count * 100:.1f}% ({between_5_10s} items)")
        Logger.info(f"  > 10s  : {over_10s / total_count * 100:.1f}% ({over_10s} items)")


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
    sentences = convert_asr_response_to_sentences(response)
    # 计算 sentences 的长度分布
    while True:
        duration_list = []
        for sentence in sentences:
            start = sentence["start"]
            end = sentence["end"]
            duration = end - start
            duration_list.append(duration)
        # 绘制直方图
        Logger.info(f"最短音频长: {min(duration_list)/1000}, 最长音频长: {max(duration_list)/1000}")
        show_histogram_in_terminal([d / 1000 for d in duration_list])  # 转换为秒
        ask = input("是否直接切片? 1: 继续, 2: cut_sentence, 3: combine_sentence, 4: exit:")
        if ask == "1":
            break
        elif ask == "2":
            ask = input("你希望的 cut_line 是? (int)毫秒")
            cut_sentences(sentences=sentences,cut_line=int(ask))
        elif ask == "3":
            ask_1 = input("你希望的 combine_line 是? (int)毫秒")
            ask_2 = input("你希望的 max_sentence_length 是? (int)个字")
            sentences = combine_sentences(sentences=sentences, combine_line=int(ask_1),max_sentence_length=int(ask_2))
        elif ask == "4":
            Logger.info("退出程序")
            sys.exit()


    output_dir = Path(config.output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    if file_path.suffix.lower() != ".wav":
        file_to_wav(input_path=file_path,output_wav_path=file_path.with_suffix(".wav"))
        file_path.unlink()  # 删除原始文件, 只保留wav格式的文件
        file_path = file_path.with_suffix(".wav")
    clip_wav(
        sentences=sentences,
        input_path=file_path,
        output_path=output_dir / f"{file_path.stem}_clip.wav",
    )


def main():
    # 待处理的所有文件
    settings = load_settings_file("config.toml", RunnerSettings)
    file_paths = get_file_list(settings.raw_audio_dir)
    print(f"raw_audio:{file_paths}")
    support_formats = ["wav", "mp3", "opus", "m4a"]
    
    # validate
    if len(file_paths) == 0:
        print("无待处理音频")
        exit()
    if not all(
        file_path.suffix[1:].lower() in support_formats for file_path in file_paths
    ):
        print(f"不支持的音频格式，请使用{support_formats}格式的音频文件。")
        exit()
    ask = input("请确保待处理的音频已经放在./raw_audio下方y/n:")

    # run clip
    if ask == "y":
        Logger.info("开始处理")
        for file_path in file_paths:
            print(f"processing {file_path} --------------------------")
            run_clip(file_path=file_path)
        # clip完成后删除掉这个wav  //因为正在开发，一个视频需要多次对比，所以并不删除，投入使用的时候可以考虑把for循环的注释删掉。
        Logger.info("All clips were done")
    else:
        return


if __name__ == "__main__":
    main()
