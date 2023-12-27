from pyannote.audio import Pipeline
from tqdm import tqdm
import torch
import os
def generate_speaker_txt(wav_name):
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token="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")
    # send pipeline to GPU (when available)
    pipeline.to(torch.device("cuda"))
    # apply pretrained pipeline
    diarization = pipeline(f"./raw_audio/{wav_name}.wav")
    lines = []
    ##print the result
    for turn, _, speaker in tqdm(diarization.itertracks(yield_label=True)):
        print(f"{turn.start*1000:.1f}|{turn.end*1000:.1f}|{speaker}")
        lines.append(f"{turn.start*1000:.1f}|{turn.end*1000:.1f}|{speaker}\n")
    with open(f"./tmp/speaker_{wav_name}.txt","w",encoding="utf-8") as file:
        file.writelines(lines)
    
    new_lines = []
    with open(f"./tmp/speaker_{wav_name}.txt","r",encoding="utf-8") as file:
        lines = file.readlines()
        latest_start = lines[0].split("|")[0]
        latest_speaker = lines[0].split("|")[2]
        new_lines.append(lines[0])

        for index,line in enumerate(lines):
            if index == 0 :
                continue
            if line.split("|")[2]==latest_speaker:
                ## merge line 消除这一行
                latest_start = new_lines[-1].split("|")[0]
                new_lines.pop(-1)
                new_lines.append(latest_start+"|"+line.split("|")[1]+"|"+latest_speaker)
            else:
                ## 出现不一样的speaker
                new_lines.append(line)
            latest_speaker = line.split("|")[2]
    with open(f"./tmp/simple_speaker_{wav_name}.txt","w",encoding="utf-8") as file:
        file.writelines(new_lines)

if __name__ == "__main__":
    wav_names = os.listdir("./raw_audio")
    for name in wav_names:
        generate_speaker_txt(wav_name=name.split(".")[0])
    print("All process were done")
    