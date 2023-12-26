import os
from pydub import AudioSegment

# 获取./tmp/目录下所有的.wav文件
file_list = [file for file in os.listdir('./tmp') if file.endswith('.wav')]
file_list.sort()  # 按文件名顺序排序

# 计算总长度
total_length = 0
segments = []
for file_name in file_list:
    audio = AudioSegment.from_wav(f'./tmp/{file_name}')
    total_length += len(audio)
    segments.append(audio)
    if total_length >= 30 * 60 * 1000:  # 30分钟的长度，以毫秒为单位
        break

# 拼接音频
output = segments[0]
for segment in segments[1:]:
    output = output.append(segment, crossfade=0)

# 导出拼接后的音频
output.export('output.wav', format='wav')
