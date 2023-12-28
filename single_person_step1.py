import os
import shutil
from tqdm import tqdm
from run_clip import clip 
from run_cut import cut
from merge_wav_by_list import merge_audio

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_file_list(dir):
    file_names = os.listdir(dir)
    if "desktop.ini" in file_names:
        file_names.remove("desktop.ini")
    return file_names
def clean_txt():
    tmp_files = os.listdir("./tmp")
    for name in tmp_files:
        if ".txt" in name:
            os.remove("./tmp/"+name)
    return tmp_files
def clean_list():
    files = get_file_list("./")
    for i in files:
        if "barbara" in i:
            os.remove("./"+i)
        if "long_character_anno" in i:
            os.remove("./"+i)

def main():
    file_names = get_file_list("./raw_audio/")
    print(file_names)
    ask = input("请确保所有下载完的音频已经放在./raw_audio下方y/n:")
    ## run clip
    if ask == "y":
        print("开始处理")
        for i in tqdm(range(len(file_names))):
            if len(file_names[i].split("."))>2:
                print("请不要在音频文件命名中输入多余的.")
                return
            clip(wav_name=file_names[i].split(".")[0])
            ## clip完成后删除掉这个wav
            os.remove("./raw_audio/"+file_names[i])
        print("All clips were done")
    ## 移动处理完后的processed音频到raw_audio下并且清空tmp
    tmp_files = clean_txt()
    for name in tmp_files:
        if ".wav" in name:
            shutil.move("./tmp/"+name,"./raw_audio/"+name)
    ## run_cut
    cliped_files = get_file_list("./raw_audio")
    for i in tqdm(range(len(cliped_files))):
        cut(wav_name=cliped_files[i].split(".")[0])
        os.remove("./raw_audio/"+cliped_files[i])
    print("All cut were done")
    cut_files = os.listdir("./tmp/cut")
    for name in cut_files:
        shutil.move("./tmp/cut/"+name,"./raw_audio/"+name)
    ## 清理txt
    clean_txt()
    ## 清理list
    clean_list()
    os.system("D:\\program\\auto_DataLabeling\\auto_DataLabeling\\10.带标点符号的标注.bat")
    os.system("D:\\program\\auto_DataLabeling\\auto_DataLabeling\\12.清理用于Bert_VITS2的标注.bat")
    labeled_files = get_file_list("./raw_audio")
    ## clean dataset folder
    old_files = get_file_list("./dataset/processed")
    if old_files is not None:
        for i in old_files:
            os.remove("./dataset/processed/"+i)
    for i in labeled_files:
        shutil.move("./raw_audio/"+i,"./dataset/processed/"+i)
    with open("./clean_barbara.list","r",encoding="utf-8") as file:
        lines = file.readlines()
        merge_audio(lines,"./merged_wav")
    
    

        
if __name__ == "__main__":
    main()