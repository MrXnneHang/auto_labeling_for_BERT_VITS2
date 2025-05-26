import os

from tqdm import tqdm

from utils.automodel_rec_to_sentences import (  # 把automodel 返回的rec转换成以前Pipline的格式。
    convert_format,
    remove_chinese_punctuation,
)
from utils.generate_model import FunASRModel, generate_results
from utils.sentences_method import generate_new_sentences


def write_lines_to_file(file_path, lines):
    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")


# 定义长文本写入函数
def write_long_txt(wav_name, cut_line, hot_word, debug=False):
    Model = FunASRModel()
    model = Model.full_version()
    response = generate_results(model=model, wav_name=wav_name, hot_word=hot_word)
    if debug == True:
        print(response[0])
        print(remove_chinese_punctuation(response[0]["text"]))
        print(
            len(remove_chinese_punctuation(response[0]["text"])),
            len(response[0]["timestamp"]),
        )  ## 比对长度，如果不一样，说明有多余的未加入的符号。
        ## 英文单词，不是按字母来算time_stamp的，而是按照单词来算time_stamp的，不管单词是不是有效。
        ## 比如ablilly,koliyaal，这算两个词，占用两个time_stamp[start,end]x2
        ## 因为有时候会识别出英文，所以需要让这个长度对齐。
        print(response[0]["timestamp"])
    sentences = convert_format(response)

    print("=====")
    print(sentences)
    print("=====")
    # 拆分句子
    sentences = generate_new_sentences(
        sentences=sentences, cutline=cut_line
    )  ##这个会把一个句子中两句话分开，如果两句话的间隔超过cutline ,default =1000ms
    lines = []
    for i in sentences:
        skip = False
        start_time_list = []
        end_time_list = []
        ## start - end too long
        for j in i["ts_list"]:
            ## 遍历start_end的元组
            start_time_list.append(j[0])
            end_time_list.append(j[1])
        # for index in range(len(start_time_list)-1): #这两个应该等长
        lines.append(
            str(i["ts_list"][0][0]) + "|" + str(i["ts_list"][-1][-1]) + "|" + i["text"]
        )
        print(
            str(i["ts_list"][0][0]) + "|" + str(i["ts_list"][-1][-1]) + "|" + i["text"]
        )
        # else:
        #     continue
    write_lines_to_file(f"./tmp/{wav_name}.txt", lines)
