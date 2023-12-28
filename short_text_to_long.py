from time_stamp import write_lines_to_file

def convert_short_txt_to_long(wav_name,merge_line=500):
    new_lines = []
    with open(f'./tmp/{wav_name}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    new_lines.append(lines[0])
    latest_start = lines[0].split("|")[0]
    latest_end = lines[0].split("|")[1]
    latest_content = lines[0].split("|")[2].replace("\n","")
    with open(f'./tmp/{wav_name}.txt', 'r', encoding='utf-8') as file:
        for index,line in enumerate(file):
            latest_content = new_lines[-1].split("|")[2].replace("\n","")
            latest_start=new_lines[-1].split("|")[0]
            latest_end=new_lines[-1].split("|")[1]
            if index == 0 :
                continue
            start_and_end = line.split("|")[:2]
            content = line.split("|")[2]
            if (int(start_and_end[0])-int(latest_end)<merge_line) and latest_end!=0: #合并这两行
                new_line = latest_start+"|"+start_and_end[1]+"|"+latest_content.replace("\n","")+content.replace("\n","")
                new_lines.pop(-1)
                new_lines.append(new_line.replace("\n",""))
            else:
                new_lines.append(line.replace("\n",""))


    write_lines_to_file(f"./tmp/processed_{wav_name}.txt",new_lines)