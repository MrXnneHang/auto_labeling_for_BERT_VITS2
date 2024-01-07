import os

from tqdm import tqdm
from utils.time_stamp import write_long_txt ## 带有时间戳的语音识别
from utils.short_text_to_long import convert_short_txt_to_long  ## 合并那些原本是同义句但是被拆分成多句的句子，同时也合并他们的时间线
from utils.clip import clip_wav ## 根据新的时间线来切割我们的wav，去掉所有的空白音频
from utils.cut import cut_wav
from utils.ignore_short_sentences import ignore_short_sentence


def cut(wav_name):
    print("开始语音识别")
    write_long_txt(wav_name=wav_name,cut_line=1000) # 这里是对clip后的操作所以可以拉得长一些，我每一句之间加了1.5s的空白。
    ## cut_line 越大，长句占比越多，原理根据短句时间的间隔，如果小于cut_line就把它们合并到一起。
    ## 推荐值300(很多短句),1000(很多长句).不应该长于1500,会把所有连在一起，
    ## 保持一致即可
    print("开始合并处理后的句子")
    convert_short_txt_to_long(wav_name=wav_name) ## ./tmp/processed.txt
    print("忽略短句")
    ignore_short_sentence(wav_name=wav_name,audio_length=2500)
    ## 通用保持一致
    print("开始保存切片")
    with open(f"./tmp/final_{wav_name}.txt",'r',encoding="utf-8") as f:
        lines = f.readlines()
    cut_wav(wav_filename=f"./raw_audio/{wav_name}.wav",lines=lines)
    ## ./tmp/cut/processed_01.wav
if __name__ == "__main__":
    file_names = os.listdir("./raw_audio")
    if "desktop.ini" in file_names:
        file_names.remove("desktop.ini")
    for i in tqdm(range(len(file_names))):
        cut(wav_name=file_names[i].split(".")[0])
    print("All process were done!")
