import argparse
from pydub import AudioSegment
import os

def resample_wav(input_path):
    # 检查文件是否为WAV格式
    if not input_path.lower().endswith('.wav'):
        raise ValueError("文件必须是WAV格式")

    # 加载音频文件
    audio = AudioSegment.from_wav(input_path)

    # 重新采样为16000Hz
    audio = audio.set_frame_rate(16000)

    # 构建输出文件的路径
    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}_16k.wav"

    # 导出文件
    audio.export(output_path, format="wav")

    print(f"文件已重新采样并保存为: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="将WAV单通道音频文件重新采样为16000Hz")
    parser.add_argument("input_path", type=str, help="输入的WAV文件路径")

    args = parser.parse_args()
    resample_wav(args.input_path)

if __name__ == "__main__":
    main()

