from pydub import AudioSegment
import os

def cut_wav(lines, wav_filename,combine_line):
    """
    根据传入的起始点和终止点把音频切片。
    """
    # 确保输出目录存在
    output_dir = "./tmp/cut"
    os.makedirs(output_dir, exist_ok=True)

    # 加载原始音频文件
    audio = AudioSegment.from_wav(wav_filename)

    # 处理每一行，剪辑音频
    for i, line in enumerate(lines):
        parts = line.strip().split('|')
        start_ms = int(parts[0])  # 开始时间，转换为毫秒
        end_ms = int(parts[1])    # 结束时间，转换为毫秒

        # 剪辑音频片段,防止截断。
        if combine_line+end_ms > len(audio) or combine_line+end_ms==len(audio):
            cut = audio[start_ms:-1]
        elif start_ms - 200 < 0:
            cut = audio[0:end_ms+combine_line]
        else:
            cut = audio[start_ms-200:combine_line+end_ms]

        # 保存剪辑后的音频
        output_filename = f"{output_dir}/{os.path.basename(wav_filename).split('.')[0]}_{i+1}.wav"
        cut.export(output_filename, format="wav")

    print(f"音频剪辑完成，保存在目录：{output_dir}")
