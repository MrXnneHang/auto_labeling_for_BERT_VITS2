from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

def write_time_stamp_with_speaker(wav_name):
    response = run_asr_inference("./raw_audio/"+wav_name+".wav")
    lines = process_funasr_response(response=response)
    with open(f"./tmp/time_stamp_with_speaker_{wav_name}.txt","w",encoding="utf-8") as file:
        file.writelines(lines)
    return f"./tmp/time_stamp_with_speaker_{wav_name}.txt"

def run_asr_inference(audio_file_path):
    # 设置推理管道
    inference_pipeline = pipeline(
        task=Tasks.auto_speech_recognition,
        model='damo/speech_paraformer-large-vad-punc-spk_asr_nat-zh-cn',
        model_revision='v0.0.2',
        vad_model='damo/speech_fsmn_vad_zh-cn-16k-common-pytorch',
        punc_model='damo/punc_ct-transformer_cn-en-common-vocab471067-large',
        output_dir="./results"
    )

    # 运行推理
    rec_result = inference_pipeline(audio_in=audio_file_path, batch_size_token=5000, batch_size_token_threshold_s=40, max_single_segment_time=6000)
    return rec_result

def process_funasr_response(response):
    sentences = response["sentences"]
    """
    ts_list -> start&end 
    text -> content
    spk -> speaker
    start|end|speaker|content
    """
    lines = []
    for index,sentence in enumerate(sentences):
        start = str(sentence["start"])
        end = str(sentence["end"])
        spk = str(sentence["spk"])
        content = sentence["text"]+"\n"
        lines.append(start+"|"+end+"|"+spk+"|"+content)
    return lines

