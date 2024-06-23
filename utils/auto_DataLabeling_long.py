import os
import sys
from pathlib import Path
path = os.path.abspath(__file__)
path = Path(path)
parent = path.parent.parent
sys.path.append(str(parent))
from utils.util import load_config,read_hot_words
from utils.generate_model import FunASRModel,generate_results

if __name__ == "__main__":
    Model = FunASRModel()
    model = Model.full_version()

    ## 删除所有标注//因为标注实际上不会太耗时，相对于降噪.
    biaozhu = ["./tmp/dataset_list/long_character_anno.txt",
               "./tmp/dataset_list/barbara.list",
               "./tmp/dataset_list/cleaned_barbara.list"]
    for i in biaozhu:
        if os.path.exists(i):
            os.remove(i)

    parent_dir = "./raw_audio/"
    complete_list = []
    filelist = list(os.walk(parent_dir))[0][2]
    file_path_list = []



    if os.path.exists('./tmp/dataset_list/long_character_anno.txt'):
        with open("./tmp/dataset_list/long_character_anno.txt", 'r', encoding='utf-8') as f:
            for line in f.readlines():
                pt, _, _ = line.strip().split('|')
                complete_list.append(pt)


    for file in filelist:
        if file[-3:] != 'wav' and file[-3:] != 'WAV':
            print(f"{file} not supported, ignoring...\n")
            filelist.remove(file)
            continue
        else:
            file = parent_dir + file
            file_path_list.append(file)


    hot_words = read_hot_words()
    rec_result = generate_results(model = model,wav_name=file_path_list)

    for index,rec in enumerate(rec_result):
        file = filelist[index]
        character_name = file.rstrip(".wav").split("_")[0]
        savepth = "./dataset/" + character_name + "/" + file
        print(rec["text"])
        annos_text = rec["text"]
        annos_text = '[ZH]' + annos_text.replace("\n", "") + '[ZH]'
        annos_text = annos_text + "\n"

        line1 = savepth + "|" + character_name + "|" + annos_text
        line2 = savepth + "|" + character_name + "|ZH|" + rec["text"] + "\n"
        with open("./tmp/dataset_list/long_character_anno.txt", 'a', encoding='utf-8') as f:
            f.write(line1)
        with open(f"./tmp/dataset_list/barbara.list", 'a', encoding='utf-8') as f:
            f.write(line2)

    print("Done!\n")

