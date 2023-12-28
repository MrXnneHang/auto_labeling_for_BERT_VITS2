from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

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

# 示例音频文件路径
audio_file = './raw_audio/chaidan.wav'

# 运行推理
result = run_asr_inference(audio_file)
print(result)
