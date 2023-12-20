import os
import wave

# 拆分wav文件
def split_wav_file(input_file, output_dir):
    with wave.open(input_file, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(wav.getnframes())

        # 计算拆分点，这里将wav文件均匀拆分成两段
        split_point = len(frames) // 2

        # 拆分并保存第一部分
        first_half_frames = frames[:split_point]
        output_file = os.path.join(output_dir, f'{os.path.basename(input_file)}_part1.wav')
        with wave.open(output_file, 'wb') as out_wav:
            out_wav.setparams(params)
            out_wav.writeframes(first_half_frames)

        # 拆分并保存第二部分
        second_half_frames = frames[split_point:]
        output_file = os.path.join(output_dir, f'{os.path.basename(input_file)}_part2.wav')
        with wave.open(output_file, 'wb') as out_wav:
            out_wav.setparams(params)
            out_wav.writeframes(second_half_frames)

# 主函数
def main():
    # 输入文件夹和输出文件夹路径
    input_dir = './input'
    output_dir = './split'

    # 确保输出文件夹存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 遍历输入文件夹中的所有wav文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.wav'):
            input_file = os.path.join(input_dir, file_name)
            split_wav_file(input_file, output_dir)
    
    print('拆分完成！')

if __name__ == '__main__':
    main()
