from pydub import AudioSegment
import os

def delete_short_wav_files(directory, min_duration_ms=500):
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        # 检查文件扩展名是否为 .wav
        if filename.endswith(".wav"):
            filepath = os.path.join(directory, filename)
            
            # 获取音频文件的持续时间
            audio = AudioSegment.from_wav(filepath)
            duration = len(audio)

            # 如果持续时间小于500毫秒，则删除文件
            if duration < min_duration_ms:
                os.remove(filepath)
                print(f"已删除文件：{filename}")

# 使用示例
directory = 'D:\\program\\auto_DataLabeling\\auto_DataLabeling\\tmp\\cut\\'  # 替换为你的目录路径
delete_short_wav_files(directory)
