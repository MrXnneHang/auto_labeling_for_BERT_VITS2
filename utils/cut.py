from pydub import AudioSegment
import os

def cut_wav(lines, wav_filename):
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

        # 剪辑音频片段
        cut = audio[start_ms:end_ms]

        # 保存剪辑后的音频
        output_filename = f"{output_dir}/{os.path.basename(wav_filename).split('.')[0]}_{i+1}.wav"
        cut.export(output_filename, format="wav")

    print(f"音频剪辑完成，保存在目录：{output_dir}")
