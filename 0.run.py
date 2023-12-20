from time_stamp import write_long_txt ## 带有时间戳的语音识别
from short_text_to_long import convert_short_txt_to_long  ## 合并那些原本是同义句但是被拆分成多句的句子，同时也合并他们的时间线
from clip import clip_wav ## 根据新的时间线来切割我们的wav，去掉所有的空白音频
wav_name = "08"

def main():
    print("开始语音识别")
    write_long_txt(wav_name=wav_name)
    print("开始处理识别后的语句")
    convert_short_txt_to_long(wav_name=wav_name)
    print("开始合成最终的人声合集")
    clip_wav(wav_name=wav_name)

if __name__ == "__main__":
    main()