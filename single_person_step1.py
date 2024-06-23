import os
import shutil
from tqdm import tqdm


from utils.util import get_file_list,clean_txt,load_config,read_hot_words
from utils.time_stamp import write_long_txt ## 带有时间戳的语音识别
from utils.short_text_to_long import convert_short_txt_to_long  ## 合并那些原本是同义句但是被拆分成多句的句子，同时也合并他们的时间线
from utils.clip import clip_wav ## 根据新的时间线来切割我们的wav，去掉所有的空白音频
from utils.ignore_short_sentences import ignore_short_sentence


"""
单人说话音频处理的第一步:
这步会把音频中的空白背景音全部去掉，并且按照有说话的句子排列，每个句子之间间隔为1.5s
对于不怎么健谈的游戏主播来说，这一步可能会把原本半小时的音频变成五分钟。
这步可以减少很多降噪的时间。
我把它叫做clip，我英文不好。
"""

os.chdir(os.path.dirname(os.path.abspath(__file__)))



def clip(wav_name):
    """这个最终做的是什么,
       1.生成语音字幕和time_stamp,写入第一个txt
       2.根据*.txt合并被拆分的短句-> processed*.txt
       3.根据processed*.txt 忽略少于一定长度的句子 -> final*.txt
       4.根据final*.txt的time_stamp剪辑*.wav
    """
    config = load_config()
    cut_line = config["cut_line"]
    combine_line = config["combine_line"]
    ignore_line = config["ignore_line"]

    print("开始语音识别")
    hot_words = read_hot_words()
    write_long_txt(wav_name=wav_name, cut_line=cut_line, hot_word=hot_words)  # ./tmp/.txt
    convert_short_txt_to_long(wav_name,combine_line=combine_line)
    print("忽略短句")
    ignore_short_sentence(wav_name=wav_name,audio_length=ignore_line)
    ## 这个audio_length会把所有短于ignore_line的忽略掉，根据字幕。
    ## 如果希望有短句，可以保留，把它设的小一点1000ms这样。

    print("开始合成最终的人声合集")

    clip_wav(wav_name=wav_name)


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
        for i in tqdm(range(len(file_names))):
            os.remove("./raw_audio/"+file_names[i])
        print("All clips were done")
    else:
        return
    ## 移动处理完后的processed音频到raw_audio下并且清空tmp   //同理，暂时保留tmp下的文件，作为对比，以及，只是覆盖。
    tmp_files = clean_txt()
    for name in tmp_files:
      if ".wav" in name:
            shutil.move("./tmp/"+name,"./raw_audio/"+name)
    
    

        
if __name__ == "__main__":
    main()
