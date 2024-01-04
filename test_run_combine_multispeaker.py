import os

from pydub import AudioSegment
from tqdm import tqdm
from moviepy.editor import VideoFileClip
from test_generate_time_stamp_with_speaker import write_time_stamp_with_speaker
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def read_segments_from_file(file_path):
    segments = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            start_ms, end_ms, label = line.strip().split('|')
            segments.append((int(start_ms), int(end_ms), label))
    return segments

def group_segments_by_speaker(segments):
    grouped = {}
    for start_ms, end_ms, speaker in segments:
        if speaker in grouped:
            grouped[speaker].append((start_ms, end_ms))
        else:
            grouped[speaker] = [(start_ms, end_ms)]
    return grouped

def process_video_by_speaker(video_path, segments_file, output_dir):
    segments = read_segments_from_file(segments_file)
    grouped_segments = group_segments_by_speaker(segments)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video = VideoFileClip(video_path)
    for speaker, segs in grouped_segments.items():
        clips = []
        for start_ms, end_ms in segs:
            start_sec = start_ms / 1000.0
            end_sec = end_ms / 1000.0
            clip = video.subclip(start_sec, end_sec)
            clips.append(clip)

        if clips:
            combined_clip = concatenate_videoclips(clips)
            output_path = os.path.join(output_dir, f"{speaker}_combined.mp4")
            combined_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

# 使用此函数处理您的视频文件
# process_video_by_speaker(video_path, segments_file, output_dir)



def merge_segments(segments, threshold_ms=1000):
    merged = []
    current_segment = None

    for segment in segments:
        if current_segment is None:
            current_segment = segment
        else:
            start, end, speaker = segment
            prev_end = current_segment[1]
            prev_speaker = current_segment[2]

            if speaker == prev_speaker and start - prev_end < threshold_ms:
                current_segment = (current_segment[0], end, speaker)
            else:
                merged.append(current_segment)
                current_segment = segment

    if current_segment:
        merged.append(current_segment)

    return merged

def process_audio_with_individual_pauses(txt_path, audio_path, output_dir, output_txt_path, pause_duration_ms=1500):
    segments = []
    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            start_ms, end_ms, speaker, _ = line.strip().split('|')
            segments.append((int(start_ms), int(end_ms), speaker))

    segments = sorted(segments, key=lambda x: x[0])
    merged_segments = merge_segments(segments)

    valid_segments = [seg for seg in merged_segments if seg[1] - seg[0] >= 2000]

    audio = AudioSegment.from_file(audio_path)
    silence = AudioSegment.silent(duration=pause_duration_ms)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    speakers_audio = {}
    with open(output_txt_path, 'w', encoding='utf-8') as output_file:
        for start_ms, end_ms, speaker in valid_segments:
            output_file.write(f"{start_ms}|{end_ms}|{speaker}\n")
            segment_audio = audio[start_ms:end_ms]
            if speaker in speakers_audio:
                speakers_audio[speaker] += silence + segment_audio
            else:
                speakers_audio[speaker] = segment_audio

    for speaker, combined_audio in speakers_audio.items():
        output_path = os.path.join(output_dir, f"{speaker}_combined_audio.wav")
        combined_audio.export(output_path, format="wav")

# 使用此函数处理您的音频文件和保存新的文本文件
# process_audio_with_individual_pauses(txt_path, audio_path, output_dir, output_txt_path)


def run_multi_clip(wav_name):
    txt_path = write_time_stamp_with_speaker(wav_name=wav_name)
    process_audio_with_individual_pauses(txt_path=txt_path, output_txt_path=f"./tmp/merged_{wav_name}.txt",audio_path=f"./raw_audio/{wav_name}.wav", output_dir=f"./tmp/{wav_name}", pause_duration_ms=1500)


if __name__ == "__main__":
    file_names = os.listdir("./raw_audio")
    if "desktop.ini" in file_names:
        file_names.remove("desktop.ini")
    for i in file_names:
        if ".mp4" in i:
            file_names.remove(i)
    for i in tqdm(range(len(file_names))):
        wav_name = file_names[i].split(".")[0]
        run_multi_clip(wav_name=wav_name)
        if os.path.isfile(f"./raw_audio/{wav_name}.mp4"):
            print("开始剪辑视频")
            process_video_by_speaker(video_path=f"./raw_audio/{wav_name}.mp4",segments_file=f"./tmp/merged_{wav_name}.txt",output_dir=f"./tmp/{wav_name}") 

# 示例使用
# process_audio_with_individual_pauses("path_to_your_txt_file.txt", "original_audio.mp3", "./tmp/")

# 请在您的本地环境中运行此脚本，并确保提供正确的文本文件路径和音频文件路径。
