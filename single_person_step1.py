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
            processed_file_names = os.listdir("./tmp/")
            if "processed_"+file_names[i] in processed_file_names:
                print("已经处理过了.skip-----")
                continue
            if len(file_names[i].split("."))>2:
                print("请不要在音频文件命名中输入多余的.")
                return
            print(f"processing {file_names[i]} --------------------------")
            clip(wav_name=file_names[i].split(".")[0])
        ## clip完成后删除掉这个wav  //因为正在开发，一个视频需要多次对比，所以并不删除，投入使用的时候可以考虑把for循环的注释删掉。
        #for i in tqdm(range(len(file_names))):
        #    os.remove("./raw_audio/"+file_names[i])
        print("All clips were done")
    else:
        return
    ## 移动处理完后的processed音频到raw_audio下并且清空tmp   //同理，暂时保留tmp下的文件，作为对比，以及，只是覆盖。
    ## tmp_files = clean_txt()
    ## for name in tmp_files:
    ##  if ".wav" in name:
    ##        shutil.move("./tmp/"+name,"./raw_audio/"+name)
    
    

        
if __name__ == "__main__":
    main()
