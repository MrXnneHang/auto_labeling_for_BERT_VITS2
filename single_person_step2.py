import os
import shutil
from tqdm import tqdm


from utils.util import get_file_list,clean_txt,clean_list,load_config,read_hot_words
from utils.loudness_norm import loudness_norm_file
from utils.generate_model import FunASRModel,generate_results
from utils.time_stamp import write_lines_to_file
from utils.cut import cut_wav
from utils.ignore_short_sentences import ignore_short_sentence

import subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def cut(wav_name):
    """
    检测起始点和终止点
    忽略太短的句子,如果audio_length<ignore_line,则忽略
    根据新的起始点和终止点进行cut
    """
    config = load_config()
    ignore_line = config["ignore_line"]
    combine_line = config["combine_line"]
    lines = []
    Model = FunASRModel()
    model = Model.only_vad()
    rec_result = generate_results(wav_name=wav_name,model=model)
    values = rec_result[0]["value"]
    for value in values:
        line = f"{value[0]}|"+f"{value[1]}|"
        lines.append(line)
    write_lines_to_file(f"./tmp/{wav_name}.txt",lines)
    ignore_short_sentence(wav_name=wav_name,audio_length=ignore_line)
    with open(f"./tmp/final_{wav_name}.txt",'r',encoding="utf-8") as f:
        lines = f.readlines()
    cut_wav(wav_filename=f"./raw_audio/{wav_name}.wav",lines=lines,combine_line=combine_line)


def main():
    config = load_config()

    # ----------------------------------------------------------------
    # 切片
    clean_txt()
    file_names = get_file_list("./raw_audio")
    print(f"raw_audio:{file_names}")
    ask = input("请确保待处理的音频已经放在./raw_audio下方y/n:")
    if ask == "n":
        print("退出程序...")
        exit()
    character_name = input("请为你的音频起一个新名字:")
    print("开始处理")
    # rename:
    audios = get_file_list("./raw_audio")
    if len(audios) == 0:
        print("无待处理音频")
        exit()
    for index,name in enumerate(audios):
        os.rename("./raw_audio/"+name,"./raw_audio/"+character_name+"_"+str(index)+".wav")
    file_names = get_file_list("./raw_audio/")

    # cut前先清除所有之前的文件
    old_files = get_file_list("./tmp/cut")
    for old_file in old_files:
        os.remove("./tmp/cut/"+old_file)
    for file in tqdm(file_names):
        if len(file.split("."))>2:
            print("请不要在音频文件命名中输入多余的.")
            return
        cut(wav_name=file.split(".")[0])
        os.remove("./raw_audio/"+file)
    print("切片完成,开始标注 ")
    cut_files = get_file_list("./tmp/cut/")
    for i in cut_files:
        shutil.move("./tmp/cut/"+i,"./raw_audio/"+i)

    # ------------------------------------------------------------
    # 标注
    # 删除barbara_list和long_ano
    clean_list()
    # 生成barbar_list和Long_ano
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
            os.remove(db_dataset_path+i)
    print("开始响度匹配，输出的文件夹为./dateset-----------------")
    for i in tqdm(labeled_files):
        loudness_norm_file(input_file="./raw_audio/"+i,output_file=db_dataset_path+i)
        os.remove("./raw_audio/"+i)
    shutil.copy("./tmp/dataset_list/clean_barbara.list","./esd.list")


if __name__ == "__main__":
    main()
