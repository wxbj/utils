import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import jieba


def union_excel_sheet(file_path):
    # 读取Excel文件并合并所有Sheet
    dfs = []
    xls = pd.ExcelFile(file_path)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df = df.drop(index=0)  # 删除第一行
        dfs.append(df)

    # 合并所有Sheet数据
    merged_df = pd.concat(dfs, ignore_index=True)

    # 保存合并后的数据
    merged_df.to_excel('merged_output.xlsx', index=False)


def get_file_path():
    # 创建一个隐藏的Tk根窗口
    root = tk.Tk()
    root.withdraw()

    # 分别获取主文件和临时文件的路径
    file_path = filedialog.askopenfilename(title='主文件')

    return file_path


def build_cloud(file_path):
    df = pd.read_excel(file_path, usecols=[0])  # 修改为实际的文件名和列名

    # 将该列数据合并成一个长字符串
    text = ' '.join(df.iloc[:, 0].dropna().astype(str))
    text = text.replace("\n","")
    text = text.replace(" ","")
    text = text.replace("研究","")
    text = text.replace("调查","")
    text = text.replace("分析","")
    text = text.replace("基于","")
    text = text.replace("影响","")
    text = text.replace("因素","")

    # 使用jieba分词
    words = jieba.cut(text)
    words_filtered = [word for word in words if len(word) >1]  # 过滤掉长度为1的词

    # 生成词云    # 读取Excel文件中的数据
    wordcloud = WordCloud(font_path="msyhl.ttc", width=800, height=400).generate(' '.join(words_filtered))

    # 显示词云
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    build_cloud(get_file_path())
