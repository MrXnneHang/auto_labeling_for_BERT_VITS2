import os
import shutil

from tqdm import tqdm

from utils.clip import clip_wav
from utils.generate_model import FunASRModel, generate_results
from utils.short_text_to_long import convert_short_txt_to_long
from utils.time_stamp import write_lines_to_file
from utils.util import clean_txt, get_file_list, load_config

"""
单人说话音频处理的第一步:
这步会把音频中的空白背景音全部去掉，并且按照有说话的句子排列，每个句子之间间隔为1.5s
对于不怎么健谈的游戏主播来说，这一步可能会把原本半小时的音频变成五分钟。
这步可以减少很多降噪的时间。
我把它叫做clip，我英文不好。
"""

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def run_clip(wav_name):
    """
    生成音频中的起始点和终止点
    合并较近但是被分开的两个句子，比如[300,2600],[3200,4500],合并依据，combine_line . 3200 - 2600 < combine_line,则合并
    根据新的起始点和终止点clip音频
    """
    config = load_config()
    cut_line = config["cut_line"]
    combine_line = config["combine_line"]
    lines = []
    Model = FunASRModel()
    model = Model.only_vad()
    rec_result = generate_results(wav_name=wav_name, model=model)
    print(rec_result)
    values = rec_result[0]["value"]
    for value in values:
        line = f"{value[0]}|" + f"{value[1]}|"
        lines.append(line)
    write_lines_to_file(f"./tmp/{wav_name}.txt", lines)
    convert_short_txt_to_long(wav_name, combine_line=combine_line)

    print("开始合成最终的人声合集")

    clip_wav(wav_name=wav_name)


def main():
    clean_txt(clean=True)
    file_names = get_file_list("./raw_audio/")
    print(f"raw_audio:{file_names}")
    ask = input("请确保待处理的音频已经放在./raw_audio下方y/n:")
    if len(file_names) == 0:
        print("无待处理音频")
        exit()
    # run clip
    if ask == "y":
        print("开始处理")
        for file_name in tqdm(file_names):
            if len(file_name.split(".")) > 2:
                print("请不要在音频文件命名中输入多余的'.'")
                return
            print(f"processing {file_name} --------------------------")
            run_clip(wav_name=file_name.split(".")[0])
        # clip完成后删除掉这个wav  //因为正在开发，一个视频需要多次对比，所以并不删除，投入使用的时候可以考虑把for循环的注释删掉。
        for file_name in tqdm(file_names):
            os.remove("./raw_audio/" + file_name)
        print("All clips were done")
    else:
        return
    tmp_files = get_file_list("./tmp")
    for name in tmp_files:
        if ".wav" in name:
            shutil.move("./tmp/" + name, "./raw_audio/" + name)


if __name__ == "__main__":
    main()
