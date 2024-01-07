import os
from tqdm import tqdm

from utils.time_stamp import write_long_txt ## 带有时间戳的语音识别
from utils.short_text_to_long import convert_short_txt_to_long  ## 合并那些原本是同义句但是被拆分成多句的句子，同时也合并他们的时间线
from utils.clip import clip_wav ## 根据新的时间线来切割我们的wav，去掉所有的空白音频
from utils.ignore_short_sentences import ignore_short_sentence

"""这个最终做的是什么,
   1.生成语音字幕和time_stamp,写入第一个txt
   2.根据*.txt合并被拆分的短句-> processed*.txt
   3.根据processed*.txt 忽略少于一定长度的句子 -> final*.txt
   4.根据final*.txt的time_stamp剪辑*.wav

"""


def clip(wav_name):
    """
    如果设置deleshort=True,会自动跳过这些短音频，skip_line是跳过的阈值，单位ms
    """
    print("开始语音识别")
    write_long_txt(wav_name=wav_name,cut_line=1000)  ## cut line会把两个字间隔长于1000ms的分隔开来，建议根据实际情况调整，如果调整成1000ms(1s).会出现很多超级长句(20s以上)
    ## 如果希望分割的句子短一些，建议300 or 500
    ## 保持一致。

    print("开始处理识别后的语句")
    convert_short_txt_to_long(wav_name=wav_name)
    print("忽略短句")
    ignore_short_sentence(wav_name=wav_name,audio_length=2500)
    ## 这个audio_length会把所有短于2500ms的忽略掉，根据字幕。
    ## 如果希望有短句，可以保留，把它设的小一点1000ms这样。
    print("开始合成最终的人声合集")
    clip_wav(wav_name=wav_name)

if __name__ == "__main__":
    file_names = os.listdir("./raw_audio")
    if "desktop.ini" in file_names:
        file_names.remove("desktop.ini")
    for i in tqdm(range(len(file_names))):
        print(f'processing {i}---------------------------------')
        clip(wav_name=file_names[i].split(".")[0])
    print("All process were done!")
