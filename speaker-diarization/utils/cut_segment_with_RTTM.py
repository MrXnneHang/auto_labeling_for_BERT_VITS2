import os
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip

def load_rttm(file_path):
    segments = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            speaker_id = parts[7]
            start = float(parts[3])
            end = start + float(parts[4])
            if speaker_id not in segments:
                segments[speaker_id] = []
            segments[speaker_id].append((start, end))
    return segments

def cut_segments(video_path, audio_path, segments, output_dir):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    for speaker_id, times in segments.items():
        speaker_dir = os.path.join(output_dir, speaker_id)
        os.makedirs(speaker_dir, exist_ok=True)

        for i, (start, end) in enumerate(times):
            video_segment = video_clip.subclip(start, end)
            audio_segment = audio_clip.subclip(start, end)

            video_segment.write_videofile(os.path.join(speaker_dir, f"video_{i}.mp4"))
            audio_segment.write_audiofile(os.path.join(speaker_dir, f"audio_{i}.wav"))

    video_clip.close()
    audio_clip.close()

def main():
    parser = argparse.ArgumentParser(description='Cut audio and video based on RTTM file')
    parser.add_argument('--rttm', type=str, required=True, help='Path to the RTTM file')
    parser.add_argument('--video', type=str, required=True, help='Path to the video file')
    parser.add_argument('--audio', type=str, required=True, help='Path to the audio file')
    parser.add_argument('--output', type=str, required=True, help='Output directory for segmented files')

    args = parser.parse_args()

    # Load RTTM file and process video and audio
    segments = load_rttm(args.rttm)
    cut_segments(args.video, args.audio, segments, args.output)

if __name__ == "__main__":
    main()
