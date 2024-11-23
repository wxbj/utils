import re
import os
import tkinter as tk
from tkinter import filedialog


def merge_file_by_lines(file_path_main, file_path_temp):
    # 以追加模式打开主文件
    with open(file_path_main, "a+", encoding="utf-8") as file_main:
        # 由于以a+打开的文件指针会指向文件尾部所以需要移动指针至首部
        file_main.seek(0)
        # 读取文件最后一行的内容,用来确定序号
        the_last_line = file_main.readlines()[-1]
        # 用正则表达式提取最后一行的序号
        match = re.match(r"^\d+", the_last_line)
        the_last_number = int(match.group(0))
        # 此处回车,让主文件从新的一行开始写入
        file_main.write("\n")
        # 以读模式打开临时文件
        with open(file_path_temp, "r", encoding="utf-8") as file_temp:
            # 逐行读取文件内容到临时文件列表中
            file_temp_lines = file_temp.readlines()
        # 根据主文件最后一行的序号修改临时文件的每一行的序号和基本格式并写入主文件
        for i, line in enumerate(file_temp_lines, start=1):
            # 由于临时文件是"1、我爱你"或者"1. 我爱你"这两种格式之一,所以有了下面的匹配代码
            match = re.search(r"^\d+、", line) or re.search(r"^\d+. ", line)
            # 由于主文件是"1. 我爱你"这种格式,所以有了下面这种修改方式
            line_new = line.replace(match.group(0), f"{the_last_number + i}. ")
            # 将修改后的行写入文件
            file_main.write(line_new)

        # 临时文件用不到了,这里删除临时文件
        os.remove(file_path_temp)
        print("处理成功。")


def get_file_path():
    # 创建一个隐藏的Tk根窗口
    root = tk.Tk()
    root.withdraw()

    # 分别获取主文件和临时文件的路径
    file_path_main = filedialog.askopenfilename(title='主文件')
    file_path_temp = filedialog.askopenfilename(title='临时文件')

    return file_path_main, file_path_temp


def delete_blank_lines(file_path):
    # 打开输入文件读取内容
    with open(file_path, "r", encoding="utf-8 ") as file:
        lines = file.readlines()

    # 过滤掉空白行（包括只包含换行符"\n"的行和完全空白的行）
    non_blank_lines = [line for line in lines if line.strip()]

    # 删除原文件,并创建将无空白行的文件
    os.remove(file_path)
    with open(file_path, "w", encoding="utf-8 ") as file:
        file.writelines(non_blank_lines)


if __name__ == "__main__":
    # 通过窗口化选择获取两个文件的路径
    file_path_main, file_path_temp = get_file_path()
    # 由于临时文件中可能会出现无意义的空行,所以需要先需处理下
    delete_blank_lines(file_path_temp)
    # 将临时文件中的内容合并到主文件,并删除临时文件
    merge_file_by_lines(file_path_main, file_path_temp)