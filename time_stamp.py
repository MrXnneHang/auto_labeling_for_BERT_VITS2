from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


def write_long_txt(wav_name):
    inference_pipeline = pipeline(
        task=Tasks.auto_speech_recognition,
        model='./model/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
        param_dict={'use_timestamp': True}
    )
    rec_result = inference_pipeline(audio_in=f'./raw_audio/{wav_name}.wav')
    print(rec_result["sentences"])
    sentences = rec_result["sentences"]
    lines = []
    for i in sentences:
        lines.append(str(i["ts_list"][0][0])+"|"+str(i["ts_list"][-1][-1])+"|"+i["text"])
        print(str(i["ts_list"][0][0])+"|"+str(i["ts_list"][-1][-1])+"|"+i["text"])
    write_lines_to_file(f'./tmp/{wav_name}.txt', lines)

def write_lines_to_file(file_path, lines):
    """
    将给定的文本行写入指定的文件。

    :param file_path: 要写入的文件的路径。
    :param lines: 要写入文件的行的列表。
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')





