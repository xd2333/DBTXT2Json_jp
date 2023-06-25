import os
import json
from settings import *

name_list = []
# load nametable
with open("nametable.txt", "r", encoding=file_encoding) as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    name, count = line.split("\t")
    name_list.append(name)

for file_name in os.listdir("txt_jp"):
    print(file_name)
    file_path = os.path.join("txt_jp", file_name)
    with open(file_path, "r", encoding=file_encoding) as f:
        text_lines = f.readlines()

    current_name = ""
    result_list = []
    for line in text_lines:
        if not line.startswith(原文标签头部特征):
            continue

        line = line.strip()

        label_end_index = line.find(原文标签尾部特征, len(原文标签头部特征))
        message = line[label_end_index + len(原文标签尾部特征) :]

        if message == "":
            continue

        if message in name_list:
            current_name = message
            continue

        tmp_obj = {"name": current_name, "message": message}
        if current_name == "":
            del tmp_obj["name"]
        result_list.append(tmp_obj)
        current_name = ""
    result_file_path = os.path.join("json_jp", file_name.replace(".txt", ".json"))
    with open(result_file_path, "w", encoding=file_encoding) as f:
        f.write(json.dumps(result_list, indent=4, ensure_ascii=False))
