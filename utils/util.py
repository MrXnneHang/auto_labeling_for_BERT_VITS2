import yaml
import os


def read_hot_words():
    with open("./hot_words.txt", 'r', encoding="utf-8") as f:
        lines = f.readlines()
    hot_words = ""
    for line in lines:
        hot_words += line.strip() + " "  # 不加换行, hotwords 不支持换行等分隔，只认空格，其他无效。
    return hot_words


def load_config():

    # 加载YAML文件
    if not os.path.isfile("./config.yml"):
        print("error:你的config.yml不存在，请创建，并且这样初始化")
        print("cut_line: 1000")
        print("combine_line: 400")
        return 0
    else:
        with open('./config.yml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        return config


def get_file_list(dir):
    file_names = os.listdir(dir)
    if "desktop.ini" in file_names:
        file_names.remove("desktop.ini")
    return file_names


def clean_txt(clean=True):
    tmp_files = os.listdir("./tmp")
    if clean:
        for name in tmp_files:
            if ".txt" in name:
                os.remove("./tmp/"+name)
    return tmp_files


def clean_list():
    if not os.path.isdir("./tmp/dataset_list"):
        os.mkdir("./tmp/dataset_list")
    files = get_file_list("./tmp/dataset_list")
    for i in files:
        if "barbara" in i:
            os.remove("./tmp/dataset_list/"+i)
        if "long_character_anno" in i:
            os.remove("./tmp/dataset_list/"+i)