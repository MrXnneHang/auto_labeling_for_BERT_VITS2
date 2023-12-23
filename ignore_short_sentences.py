from time_stamp import write_lines_to_file

def ignore_short_sentence(wav_name,audio_length):
    new_lines = []
    with open(f'./tmp/processed_{wav_name}.txt', 'r', encoding='utf-8') as file:
        for line in file:
            start_and_end = line.split("|")[:2]
            content = line.split("|")[2]
            if int(start_and_end[1])-int(start_and_end[0])<audio_length: ##忽略这一行
                continue
            else:
                new_lines.append(line.replace("\n",""))

    write_lines_to_file(f"./tmp/final_{wav_name}.txt",new_lines)