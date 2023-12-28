from time_stamp import write_long_txt ## 带有时间戳的语音识别
from short_text_to_long import convert_short_txt_to_long  ## 合并那些原本是同义句但是被拆分成多句的句子，同时也合并他们的时间线
from clip_wav_by_speaker import clip_wav_with_speaker
import os
from tqdm import tqdm
from ignore_short_sentences import ignore_short_sentence
from generate_final_with_speaker_txt import final_with_speaker
from speaker_detect import generate_speaker_txt
def clip_with_speaker_txt(wav_name):
    """
    如果设置deleshort=True,会自动跳过这些短音频，skip_line是跳过的阈值，单位ms
    """
    print("开始语音识别")
    write_long_txt(wav_name=wav_name,cut_line=1000)
    print("开始处理识别后的语句")
    convert_short_txt_to_long(wav_name=wav_name,merge_line=150)
    print("忽略短句")
    ignore_short_sentence(wav_name=wav_name,audio_length=2500)
    print("生成speaker.txt")
    generate_speaker_txt(wav_name=wav_name)
    print("结合speaker的txt来生成final_with_speaker.txt")
    final_with_speaker(wav_name=wav_name)
    print("根据最后的带有speaker标注的txt来生成clip文件")
    ## 需要新的clip,我们不动旧代码
    clip_wav_with_speaker(wav_name=wav_name)


if __name__ == "__main__":
    file_names = os.listdir("./raw_audio")
    if "desktop.ini" in file_names:
        file_names.remove("desktop.ini")
    for i in tqdm(range(len(file_names))):
        clip_with_speaker_txt(wav_name=file_names[i].split(".")[0])
        
        
    print("All process were done!")
