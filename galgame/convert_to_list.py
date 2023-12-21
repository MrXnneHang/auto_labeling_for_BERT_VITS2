
import os

def write_esd_list():
    # 获取当前目录下的所有txt文件
    txt_files = [f for f in os.listdir('./txt') if os.path.isfile("./txt/"+f) and f.endswith('.txt')]
    print(txt_files)

    # 合并文件内容
    merged_content = []
    for file in txt_files:
        with open("./txt/"+file, 'r', encoding='utf-8') as f:
            # 读取文件内容，并去除换行符
            content = f.read().replace('\n', '')
            # 合并文件名和内容
            merged_line = f"{file}|Atri|JP|{content}"
            merged_content.append(merged_line)

    # 写入到新文件
    with open('esd.list', 'w', encoding='utf-8') as f:
        for line in merged_content:
            f.write(line + '\n')

    # 返回完成状态
    print("合并完成，所有内容已写入 'esd.list' 文件。")

def replace_txt_to_wav():
    # 读取esd.list文件内容
    with open('esd.list', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 替换文件名中的后缀
    updated_lines = [line.replace('.txt', '.wav') for line in lines]

    # 将更新后的内容写回文件
    with open('esd.list', 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)

    # 返回完成状态
    print("文件名后缀已从 '.txt' 更改为 '.wav'，并已更新至 'esd.list' 文件。")

if __name__ == "__main__":
    write_esd_list()
    replace_txt_to_wav()
