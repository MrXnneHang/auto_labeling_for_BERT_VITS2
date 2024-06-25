import yaml
import os
from pathlib import  Path
import numpy as np


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

def clean_esd_wav():
    """
    根据清理完后的esd文件把已经被删掉的音频（在操作中被删掉的音频）进行清理。
    其实正常使用可以不删除，因为在数据集清理之后，esd就不会再引用被删除掉的音频。
    但是我为了留下一些混合speaker和单独speaker的数据集，我特地利用清理数据集删掉了大部分正常数据集。
    留下部分不正常数据集和正常数据集，这样我就可以进行一个speaker清洗的调参。
    """
    with open("./esd.list",'r',encoding="utf-8") as f:
        lines = f.readlines()
    file_list = [line.split("|")[0] for line in lines]
    sample_file = file_list[0]
    file_name_list = [str(Path(file).name) for file in file_list]
    parent = Path(sample_file).parent
    dir_list = get_file_list(str(parent))
    for file_name in dir_list:
        if file_name not in file_name_list:
            os.remove(str(parent / file_name))


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


def save_spk_tensors_to_yaml(tensor_list, file_list, filename):
    # 将张量列表转换为普通的 Python 列表
    tensor_data = [tensor.tolist() for tensor in tensor_list]

    # 创建一个字典来保存张量数据和文件名
    data = {'tensors': tensor_data, 'file_names': file_list}

    # 将字典转换为 YAML 格式并保存到文件中
    with open(filename, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    print(f"Data saved to {filename}")

def read_spk_tensors_from_yaml(filename):
    # 从 YAML 文件中读取数据
    with open(filename, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    # 将数据转换为 NumPy 数组，并保留文件名
    tensor_list = [np.array(tensor) for tensor in data['tensors']]
    file_list = data['file_names']

    return tensor_list, file_list