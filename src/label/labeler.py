import os
import sys
from pathlib import Path

from label.utils.model import FunASRModel, generate_asr_results
from label.utils.util import  read_hot_words
from label.utils.config import load_settings_file
from label._dataclass import RunnerSettings
from label.console.logger import Logger

def main():
    config = load_settings_file("config.toml", RunnerSettings)
    Model = FunASRModel()
    model = Model.full_asr()
    ## 删除所有标注//因为标注实际上不会太耗时，相对于降噪.
    labels = [
        "./long_character_anno.txt",
        "./esd.list",
        "./cleaned_esd.list",
    ]
    for label_path in labels:
        label_path = Path(label_path)
        if label_path.exists():
            label_path.unlink()


    input_dir = Path(config.output_dir) / "cut"
    # global parent_dir, 读取所有音频文件
    input_paths = list(input_dir.glob("*/*.wav"))
    if len(input_paths) == 0:
        Logger.warning("没有找到任何待标注音频文件请先运行 clipper 和 cutter.")
        sys.exit(1)

    responses = []
    for input_path in input_paths:
        responses.append(generate_asr_results(model=model, input_path=input_path))

    for index, rec in enumerate(responses):
        file = input_paths[index]
        character_name = file.name.rstrip(".wav").split("_")[0]
        savepth = "./dataset/" + character_name + "/" + file.name
        Logger.info(rec["text"])
        annos_text = rec["text"]
        annos_text = "[ZH]" + annos_text.replace("\n", "") + "[ZH]"
        annos_text = annos_text + "\n"

        line1 = savepth + "|" + character_name + "|" + annos_text
        line2 = savepth + "|" + character_name + "|ZH|" + rec["text"] + "\n"
        with Path("./long_character_anno.txt").open("a", encoding="utf-8") as f:
            f.write(line1)
        with Path("./esd.list").open("a", encoding="utf-8") as f:
            f.write(line2)

    print("Done!\n")
