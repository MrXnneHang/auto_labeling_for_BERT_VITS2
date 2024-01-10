import argparse
import json
from moviepy.editor import VideoFileClip, AudioFileClip

def cut_video(input_file, output_file, start_time, end_time):
    # 使用try-except结构来处理可能的异常
    input_file = input_file.replace(".wav",".mp4")
    try:
        with VideoFileClip(input_file) as video:
            new_video = video.subclip(start_time, end_time)
            new_video.write_videofile(output_file, codec="libx264")
    except Exception as e:
        print(f"处理视频文件时出现错误: {e}")

def cut_audio(input_file, output_file, start_time, end_time):
    try:
        with AudioFileClip(input_file) as audio:
            new_audio = audio.subclip(start_time, end_time)
            new_audio.write_audiofile(output_file)
    except Exception as e:
        print(f"处理音频文件时出现错误: {e}")

def main():
    parser = argparse.ArgumentParser(description="Audio/Video clipping tool")
    parser.add_argument("-c", "--config", help="JSON configuration file", required=True)
    parser.add_argument("-o", "--output", help="Output directory", required=True)
    # 修改这里的解析方式，确保能正确处理布尔值
    parser.add_argument("--video", dest='video', action='store_true')
    parser.set_defaults(video=False)
    args = parser.parse_args()

    with open(args.config, 'r') as json_file:
        data = json.load(json_file)

    for key, values in data.items():
        input_file = values['file']
        output_file = f"{args.output}/{key}.{'mp4' if args.video else 'wav'}"
        start_time = values['start']
        end_time = values['stop']

        if args.video:
            cut_video(input_file, output_file, start_time, end_time)
        else:
            cut_audio(input_file, output_file, start_time, end_time)

if __name__ == "__main__":
    main()
