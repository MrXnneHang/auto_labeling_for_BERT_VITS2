from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import yaml

from label.console.logger import Logger

if TYPE_CHECKING:
    from label._typing import Sentence


def read_hot_words():
    if not Path("./hot_words.txt").exists():
        return ""
    with Path("./hot_words.txt").open("r", encoding="utf-8") as f:
        lines = f.readlines()
    hot_words = ""
    for line in lines:
        hot_words += (
            line.strip() + " "
        )  # 不加换行, hotwords 不支持换行等分隔，只认空格，其他无效。
    return hot_words


def load_config():
    # 加载YAML文件
    if not os.path.isfile("./config.yml"):
        print("error:你的config.yml不存在，请创建，并且这样初始化")
        print("cut_line: 1000")
        print("combine_line: 400")
        return 0
    else:
        with open("./config.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        return config


# def clean_esd_wav():
#     """
#     根据清理完后的esd文件把已经被删掉的音频（在操作中被删掉的音频）进行清理。
#     其实正常使用可以不删除，因为在数据集清理之后，esd就不会再引用被删除掉的音频。
#     但是我为了留下一些混合speaker和单独speaker的数据集，我特地利用清理数据集删掉了大部分正常数据集。
#     留下部分不正常数据集和正常数据集，这样我就可以进行一个speaker清洗的调参。
#     """
#     with open("./esd.list", "r", encoding="utf-8") as f:
#         lines = f.readlines()
#     file_list = [line.split("|")[0] for line in lines]
#     sample_file = file_list[0]
#     file_name_list = [str(Path(file).name) for file in file_list]
#     parent = Path(sample_file).parent
#     dir_list = []
#     for file_name in dir_list:
#         if file_name not in file_name_list:
#             os.remove(str(parent / file_name))


def clean_txt(clean=True):
    tmp_files = os.listdir("./tmp")
    if clean:
        for name in tmp_files:
            if ".txt" in name:
                os.remove("./tmp/" + name)
    return tmp_files


def show_sentences_length(sentences: list[Sentence]):
    duration_list = []
    for sentence in sentences:
        start = sentence["start"]
        end = sentence["end"]
        duration = (end - start) / 1000  # 转换为秒
        duration_list.append(duration)
    total_count = len(duration_list)
    Logger.info(f"音频段数: {total_count}")
    Logger.info(f"最短音频长: {min(duration_list)}, 最长音频长: {max(duration_list)}")
    if total_count > 0:
        under_2s = sum(1 for d in duration_list if d < 2)
        between_2_5s = sum(1 for d in duration_list if 2 <= d < 5)
        between_5_10s = sum(1 for d in duration_list if 5 <= d < 10)
        over_10s = sum(1 for d in duration_list if d >= 10)

        Logger.info(
            f"  < 2s   : {under_2s / total_count * 100:.1f}% ({under_2s} items)"
        )
        Logger.info(
            f"  2-5s   : {between_2_5s / total_count * 100:.1f}% ({between_2_5s} items)"
        )
        Logger.info(
            f"  5-10s  : {between_5_10s / total_count * 100:.1f}% ({between_5_10s} items)"
        )
        Logger.info(
            f"  > 10s  : {over_10s / total_count * 100:.1f}% ({over_10s} items)"
        )
