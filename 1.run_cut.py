from time_stamp import write_long_txt ## 带有时间戳的语音识别
from short_text_to_long import convert_short_txt_to_long  ## 合并那些原本是同义句但是被拆分成多句的句子，同时也合并他们的时间线
from clip import clip_wav ## 根据新的时间线来切割我们的wav，去掉所有的空白音频
import os
from tqdm import tqdm
from cut import cut_wav
from ignore_short_sentences import ignore_short_sentence

wav_name = "08"
def main(wav_name):
    print("开始语音识别")
    write_long_txt(wav_name=wav_name,cut_line=2000) ##对于不小心被识别到同一句中的我也只能说抱歉，只能skip
    print("开始合并处理后的句子")
    convert_short_txt_to_long(wav_name=wav_name) ## ./tmp/processed.txt
    print("忽略短句")
    ignore_short_sentence(wav_name=wav_name,audio_length=2500)
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
        main(wav_name=file_names[i].split(".")[0])
    print("All process were done!")