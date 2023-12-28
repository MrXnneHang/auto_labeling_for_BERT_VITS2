from pydub import AudioSegment
import os

def process_audio_with_individual_pauses(txt_path, audio_path, output_dir, pause_duration_ms=1500):
    # 读取文本文件
    segments = []
    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            start_ms, end_ms, speaker, _ = line.strip().split('|')
            segments.append((int(start_ms), int(end_ms), speaker))

    # 检查是否有重叠的时间段
    segments = sorted(segments, key=lambda x: x[0])
    valid_segments = []
    prev_end = 0
    for segment in segments:
        start, end, speaker = segment
        if start >= prev_end:
            valid_segments.append(segment)
            prev_end = end

    # 检查每个时间段的长度
    valid_segments = [seg for seg in valid_segments if seg[1] - seg[0] >= 2000]

    # 加载音频文件
    audio = AudioSegment.from_file(audio_path)

    # 创建静音段
    silence = AudioSegment.silent(duration=pause_duration_ms)

    # 根据发言人切割和组合音频
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    speakers_audio = {}
    for start_ms, end_ms, speaker in valid_segments:
        segment_audio = audio[start_ms:end_ms]
        if speaker in speakers_audio:
            speakers_audio[speaker] += silence + segment_audio
        else:
            speakers_audio[speaker] = segment_audio

    # 保存每个发言人的音频
    for speaker, combined_audio in speakers_audio.items():
        output_path = os.path.join(output_dir, f"{speaker}_combined_audio.mp3")
        combined_audio.export(output_path, format="mp3")

# 示例使用
# process_audio_with_individual_pauses("path_to_your_txt_file.txt", "original_audio.mp3", "./tmp/")

# 请在您的本地环境中运行此脚本，并确保提供正确的文本文件路径和音频文件路径。
