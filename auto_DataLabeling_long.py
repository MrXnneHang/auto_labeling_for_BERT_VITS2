from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os

## 删除所有标注//因为标注实际上不会太耗时，相对于降噪.
biaozhu = ["./long_character_anno.txt","./barbara.list","cleaned_barbara.list"]
for i in biaozhu:
    os.remove(i)

parent_dir = "./raw_audio/"
local_dir_model = "./Model/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
complete_list = []
filelist = list(os.walk(parent_dir))[0][2]



if os.path.exists('long_character_anno.txt'):
    with open("./long_character_anno.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            pt, _, _ = line.strip().split('|')
            complete_list.append(pt)

inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model=local_dir_model
)


for file in filelist:
    if file[-3:] != 'wav':
        print(f"{file} not supported, ignoring...\n")
        continue
    print(f"transcribing {parent_dir + file}...\n")

    character_name = file.rstrip(".wav").split("_")[0]
    savepth = "./dataset/" + character_name + "/" + file


    rec_result = inference_pipeline(audio_in=parent_dir + file)

    if 'text' not in rec_result:
        print("Text is not recognized，ignoring...\n")
        continue

    annos_text = rec_result['text']
    annos_text = '[ZH]' + annos_text.replace("\n", "") + '[ZH]'
    annos_text = annos_text + "\n"
    line1 = savepth + "|" + character_name + "|" + annos_text
    line2 = savepth + "|" + character_name + "|ZH|" + rec_result['text'] + "\n"
    with open("./long_character_anno.txt", 'a', encoding='utf-8') as f:
        f.write(line1)
    with open(f"./barbara.list", 'a', encoding='utf-8') as f:
        f.write(line2)
    print(rec_result['text'])
print("Done!\n")

