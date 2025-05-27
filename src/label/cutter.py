import os
import shutil
import subprocess

from tqdm import tqdm
from pathlib import Path
from label.utils.cut import cut_wav
from label.utils.model import FunASRModel, generate_asr_results
from label.utils.loudness_norm import loudness_norm_file
from label.utils.util import clean_list, get_file_list, show_sentences_length
from label.utils.config import load_settings_file
from label._dataclass import RunnerSettings
from label.basic_runner.converter import convert_asr_response_to_sentences
from label.utils.ignore_sentences import ignore_long_sentences, ignore_short_sentences
from label.console.logger import Logger

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def cut(input_path:Path):
    """
    检测起始点和终止点
    忽略太短的句子,如果audio_length<ignore_line,则忽略
    根据新的起始点和终止点进行cut
    """
    Model = FunASRModel()
    model = Model.vad_and_asr()
    response = generate_asr_results(model=model, input_path=input_path)
    sentences = convert_asr_response_to_sentences(input_data=response)
    while True:
        show_sentences_length(sentences=sentences)
        ask1 = input("是否直接开始切片?(1) 或者要忽略过短的句子?(2) 或者忽略过长的句子?(3):")
        match ask1:
            case "1":
                break
            case "2":
                ask2 = input("你希望忽略的小于(int)毫秒的句子:")
                if not ask2.isdigit():
                    Logger.warning("请输入整数")
                    continue
                sentences = ignore_short_sentences(sentences=sentences, min_length=int(ask2))
            case "3":
                ask2 = input("你希望忽略长于(int)毫秒的片段:")
                if not ask2.isdigit():
                    Logger.warning("请输入整数")
                    continue
                sentences = ignore_long_sentences(sentences=sentences, max_length=int(ask2))
            case _:
                Logger.warning("无效输入")
    output_dir = cut_wav(sentences=sentences, input_path=input_path)
    return output_dir

def main():
    # 待处理的所有文件
    settings = load_settings_file("config.toml", RunnerSettings)
    file_paths = get_file_list(settings.raw_audio_dir)
    Logger.info(f"raw_audio:{file_paths}")
    support_formats = ["wav", "mp3", "opus", "m4a"]
    
    # validate
    if len(file_paths) == 0:
        Logger.warning("无待处理音频")
        exit()
    if not all(
        file_path.suffix[1:].lower() in support_formats for file_path in file_paths
    ):
        Logger.warning(f"不支持的音频格式，请使用{support_formats}格式的音频文件。")
        exit()
    ask = input("请确保待处理的音频已经放在./raw_audio下方y/n:")

    if ask == "n":
        exit()
    else:
        for file_path in file_paths:
            output_dir = cut(input_path=Path(file_path))
        Logger.info("切片完成,开始标注 ")
        cut_files = get_file_list(output_dir)
        # ------------------------------------------------------------
        # 标注
        subprocess.run(["python", "./utils/auto_DataLabeling_long.py"])
        # 生成clean_barbara_list
        subprocess.run(["python.exe", "./utils/clean_barbara_list.py"])
        labeled_files = get_file_list("./raw_audio")

        # ------------------------------------------------------------
        # 放进手动清洗数据集的文件夹中，带响度对齐，之后运行手动清理查看一遍或者忽略即可。
        # clean dataset folder
        db_dataset_path = f"./dataset/{character_name}/"
        if not os.path.isdir(db_dataset_path):
            os.mkdir(db_dataset_path)
        old_files = get_file_list(db_dataset_path)
        if old_files is not None:
            for i in old_files:
                os.remove(db_dataset_path + i)
        print("开始响度匹配，输出的文件夹为./dateset-----------------")
        for i in tqdm(labeled_files):
            loudness_norm_file(
                input_file="./raw_audio/" + i, output_file=db_dataset_path + i
            )
            os.remove("./raw_audio/" + i)
        shutil.copy("./tmp/dataset_list/clean_barbara.list", "./esd.list")


if __name__ == "__main__":
    main()
