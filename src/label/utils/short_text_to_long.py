from utils.time_stamp import write_lines_to_file

"""
根据./tmp/wavname.txt里面的
354|2680|
2740|3440|
来合并距离过短的两个相邻句子。
似乎只能处理一次合并，如果一次合并后还有这种情况就需要二次运行了。
"""


def convert_short_txt_to_long(wav_name, combine_line):
    latest_start = 0
    latest_end = 0
    latest_content = ""
    latest_line = ""
    new_lines = []
    with open(f"./tmp/{wav_name}.txt", "r", encoding="utf-8") as file:
        for line in file:
            start_and_end = line.split("|")[:2]
            content = line.split("|")[2]
            if (int(start_and_end[0]) - int(latest_end) < combine_line) and (
                int(latest_end) != 0
            ):  # 合并这两行
                new_line = (
                    latest_start
                    + "|"
                    + start_and_end[1]
                    + "|"
                    + latest_content.replace("\n", "")
                    + content.replace("\n", "")
                )

                new_lines.pop()
                new_lines.append(new_line)
            else:
                new_lines.append(line.replace("\n", ""))

    write_lines_to_file(f"./tmp/processed_{wav_name}.txt", new_lines)
