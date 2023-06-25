import os
from settings import *

name_table = {}
for file_name in os.listdir("txt_jp"):
    print(file_name)
    file_path = os.path.join("txt_jp", file_name)
    with open(file_path, "r", encoding=file_encoding) as f:
        text_lines = f.readlines()
    for line in text_lines:
        if not line.startswith(原文标签头部特征):
            continue

        line = line.strip()

        label_end_index = line.find(原文标签尾部特征, len(原文标签头部特征))

        message = line[label_end_index + len(原文标签尾部特征) :]

        if message == "":
            continue

        if len(message) < 人名长度阈值:
            black_flag = False
            for char in 人名黑名单字符:
                if char in message:
                    black_flag = True
                    break
            if black_flag:
                continue

            if message in name_table:
                name_table[message] += 1
            else:
                name_table[message] = 1

with open("nametable.txt", "w", encoding=file_encoding) as f:
    for name,count in name_table.items():
        f.write(name + "\t" + str(count) + "\n")