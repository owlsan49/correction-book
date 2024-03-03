# -*- coding: utf-8 -*-
# Copyright (c) 2022, Shang Luo
# All rights reserved.
# 
# Author: 罗尚
# Building Time: 2024/3/1
# Reference: None
# Description: None
import json
import re
import copy
import random

from datetime import datetime

data_path = './cb_recorder.json'
data_bk_path = './cb_recorder-bk.json'
data_std_path = './cb_recorder_std.json'
repeat_point = [1, 4, 11, 41]


def read_json(data_path):
    try:
        with open(data_path, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
    except Exception as e:
        print(e)
        print(f'{data_path} is Null')
        data = {}
    return data


def write_json(file_name, json_dict, mode='w'):
    with open(file_name, mode, encoding='utf-8') as jf:
        json.dump(json_dict, jf)


def update_words(cb_recorder: dict, words: list):
    info = {}
    if len(cb_recorder["pop_queue"]) == 0:
        cb_recorder["pop_queue"] = [0] * cb_recorder["max_len"]

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d')
    flag = formatted_datetime in cb_recorder["src_data"].keys()
    if flag:
        cb_recorder["src_data"][formatted_datetime].extend(words)
    else:
        write_json(data_bk_path, cb_recorder)
        cb_recorder["tptr"] = (cb_recorder["tptr"] + 1) % cb_recorder["max_len"]
        cb_recorder["src_data"][formatted_datetime] = words

    cb_recorder["total_list"].extend(words)
    for rp in repeat_point:
        pos = (cb_recorder["tptr"] + rp) % cb_recorder["max_len"]
        insect_queue(cb_recorder["pop_queue"], pos, words)
    write_json(data_path, cb_recorder)

    return info


def insect_queue(pop_queue, pos, words):
    if isinstance(pop_queue[pos], list):
        pop_queue[pos].extend(words)
    else:
        pop_queue[pos] = words


def prepare_words(total_list, words: str):
    words = words.replace("\n", "  ")
    words = re.split(r' {2,}', words)
    formatted_words = []
    for i, w in enumerate(words):
        if w not in total_list:
            formatted_words.append(w.lower())
        else:
            print(f'<{w}> is filtered causing repetition')
    return formatted_words


def init_recorder():
    std_recorder = read_json(data_std_path)
    write_json(data_path, std_recorder)


def get_words(cb_recorder: dict, length=50, shuffle=True):
    tptr = cb_recorder["tptr"]
    words_source = cb_recorder["pop_queue"][tptr]
    if words_source == 0:
        words = []
        cb_recorder["tptr"] = (cb_recorder["tptr"] + 1) % cb_recorder["max_len"]
    elif len(words_source) <= length:
        words = copy.deepcopy(words_source)
        cb_recorder["pop_queue"][tptr] = 0
        cb_recorder["tptr"] = (cb_recorder["tptr"] + 1) % cb_recorder["max_len"]
    else:
        words = copy.deepcopy(words_source[:length])
        del words_source[:length]
    if shuffle:
        random.shuffle(words)
    write_json(data_path, cb_recorder)
    return words


cb_recorder = read_json(data_path)

if __name__ == '__main__':
    init_recorder()
    # print(update_words(cb_recorder, ['fork', 'nihao']))
