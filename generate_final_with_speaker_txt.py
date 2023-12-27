"""
这一步必须插入在ignore_short_之后也就是根据final_{wav_name}.txt来生成
"""
import os
from tqdm import tqdm

def determine_speaker(content_start, content_end, speaker_data):
    content_start = float(content_start)
    content_end = float(content_end)
    content_duration = content_end - content_start

    overlap_duration = 0
    chosen_speaker = 'None'
    for speaker_start, speaker_end, speaker in speaker_data:
        speaker_start = float(speaker_start)
        speaker_end = float(speaker_end)

        # Calculate overlap
        overlap = min(content_end, speaker_end) - max(content_start, speaker_start)
        if overlap > 0:
            overlap_duration += overlap
            if overlap_duration / content_duration >= 0.6:
                chosen_speaker = speaker
                break

    return chosen_speaker
def final_with_speaker(wav_name):
    ## 我们要做的只是把final{wav_name}.txt -> final_with_speaker_{wav_name}.txt,实际上就是加上一个speaker标签，不是很难.
    # Reading content data from a file
    with open(f'./tmp/final_{wav_name}.txt', 'r',encoding="utf-8") as file:
        content_lines = file.readlines()
    content_list = [tuple(line.strip().split('|')) for line in content_lines]

    # Reading speaker data from a file
    with open(f'./tmp/simple_speaker_{wav_name}.txt', 'r',encoding="utf-8") as file:
        speaker_lines = file.readlines()
    speaker_list = [tuple(line.strip().split('|')) for line in speaker_lines]
    # Creating the final output with speaker annotations
    final_with_speaker = []
    for content_start, content_end, content in content_list:
        speaker = determine_speaker(content_start, content_end, speaker_list)
        final_with_speaker.append(f"{content_start}|{content_end}|{speaker}|{content}")

    final_with_speaker_output = "\n".join(final_with_speaker)
    with open(f"./tmp/final_with_speaker_{wav_name}.txt","w",encoding="utf-8") as file:
        file.write(final_with_speaker_output)

if __name__ == "__main__":
    file_names = os.listdir("./raw_audio")
    if "desktop.ini" in file_names:
        file_names.remove("desktop.ini")
    for i in tqdm(range(len(file_names))):
        final_with_speaker(file_names[i].split(".")[0])
        
    print("All process were done!")
