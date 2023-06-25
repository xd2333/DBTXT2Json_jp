import os
import json
from settings import *

name_table = {}
message_table = {}

for file_name in os.listdir("txt_jp"):
    print(file_name)
    file_path_txt_jp = os.path.join("txt_jp", file_name)
    file_path_json_jp = os.path.join("json_jp", file_name.replace(".txt", ".json"))
    file_path_json_cn = os.path.join("json_cn", file_name.replace(".txt", ".json"))
    file_path_txt_cn = os.path.join("txt_cn", file_name)

    json_jp = json.load(open(file_path_json_jp, "r", encoding=file_encoding))
    json_cn = json.load(open(file_path_json_cn, "r", encoding=file_encoding))

    for i, obj in enumerate(json_jp):
        if "name" in obj:
            jp_name = obj["name"]
            cn_name = json_cn[i]["name"]
            name_table[jp_name] = cn_name
        message_table[obj["message"]] = json_cn[i]["message"]

    result_list = []
    with open(file_path_txt_jp, "r", encoding=file_encoding) as f:
        text_lines = f.readlines()
    for line in text_lines:
        if not line.startswith(译文标签头部特征):
            result_list.append(line)
            continue

        line = line.strip()

        label_end_index = line.find(译文标签尾部特征, len(译文标签头部特征))

        label = line[: label_end_index + len(译文标签尾部特征)]
        message = line[label_end_index + len(译文标签尾部特征) :]

        if message == "":
            continue

        tmp_text = ""
        if message in message_table:
            tmp_text = label + message_table[message] + "\n"
        elif message in name_table:
            tmp_text = label + name_table[message] + "\n"
        else:
            tmp_text = line + "\n"
        result_list.append(tmp_text)

    with open(file_path_txt_cn, "w", encoding=file_encoding) as f:
        f.writelines(result_list)
