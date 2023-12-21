from time_stamp import write_long_txt ## 带有时间戳的语音识别
from short_text_to_long import convert_short_txt_to_long  ## 合并那些原本是同义句但是被拆分成多句的句子，同时也合并他们的时间线
from clip import clip_wav ## 根据新的时间线来切割我们的wav，去掉所有的空白音频
import os
from tqdm import tqdm

"""
输入例:./tmp/08.wav
输出例:08.txt,processed_08.txt,08.wav->processed_08.wav
"""

wav_name = "08"
def main(wav_name,deletshort=True,skip_line=3500):
    """
    如果设置deleshort=True,会自动跳过这些短音频，skip_line是跳过的阈值，单位ms
    """
    print("开始语音识别")
    write_long_txt(wav_name=wav_name,deletshort=True,skip_line=skip_line)
    # print("开始处理识别后的语句")
    # convert_short_txt_to_long(wav_name=wav_name)
    print("开始合成最终的人声合集")
    clip_wav(wav_name=wav_name)

if __name__ == "__main__":
    file_names = os.listdir("./raw_audio")
    file_names.remove("desktop.ini")
    for i in tqdm(range(len(file_names))):
        main(wav_name=file_names[i].split(".")[0])
    print("All process were done!")