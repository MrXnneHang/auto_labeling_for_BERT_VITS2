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
    new_name = input("请为你的音频起一个新名字:")
    ## run cut
    if ask == "y":
        print("开始处理")
        ## rename:
        audios = get_file_list("./raw_audio")
        for index,name  in enumerate(audios):
            os.rename("./raw_audio/"+name,"./raw_audio/"+new_name+"_"+str(index)+".wav")
        file_names = get_file_list("./raw_audio/")

        ## cut前先清除所有之前的文件
        old_files = get_file_list("./tmp/cut")
        for old_file in old_files:
            os.remove("./tmp/cut/"+cut_files)
        for i in tqdm(range(len(file_names))):
            if len(file_names[i].split("."))>2:
                print("请不要在音频文件命名中输入多余的.")
                return
            cut(wav_name=file_names[i].split(".")[0])
            os.remove("./raw_audio/"+file_names[i])
        print("All cuts were done")
    tmp_files = clean_txt()
    cut_files = get_file_list("./tmp/cut/")
    for i in cut_files:
        shutil.move("./tmp/cut/"+i,"./raw_audio/"+i)
    ## 清理txt
    clean_txt()
    ## 清理list
    clean_list()
    ## autolabeling
    os.system("D:\\program\\auto_DataLabeling\\auto_DataLabeling\\10.带标点符号的标注.bat")
    os.system("D:\\program\\auto_DataLabeling\\auto_DataLabeling\\12.清理用于Bert_VITS2的标注.bat")
    labeled_files = get_file_list("./raw_audio")
    ## clean dataset folder
    db_dataset_path = "./db/dataset/xishi/"
    old_files = get_file_list(db_dataset_path)
    if old_files is not None:
        for i in old_files:
            os.remove(db_dataset_path+i)
    for i in labeled_files:
        shutil.move("./raw_audio/"+i,db_dataset_path+i)
    shutil.move("./clean_barbara.list","./db/esd.list")
    
    

        
if __name__ == "__main__":
    main()