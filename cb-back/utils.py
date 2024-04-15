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
        cb_recorder["src_data"][formatted_datetime] = words

    cb_recorder["total_list"].extend(words)
    for rp in repeat_point:
        pos = (cb_recorder["tptr"] + rp) % cb_recorder["max_len"]
        insect_queue(cb_recorder["pop_queue"], pos, words)
    write_json(data_path, cb_recorder)

    return info


def update_add_words(cb_recorder: dict, add_words: list):
    info = {}
    tmp_tptr = cb_recorder["tptr"]
    print(add_words)
    if cb_recorder["pop_queue"][tmp_tptr] == 0:
        cb_recorder["pop_queue"][tmp_tptr] = add_words
    else:
        for w in add_words:
            if isinstance(cb_recorder["pop_queue"][tmp_tptr], list) and (w not in cb_recorder["pop_queue"][tmp_tptr]):
                cb_recorder["pop_queue"][tmp_tptr].append(w)
    write_json(data_path, cb_recorder)

    return info


def insect_queue(pop_queue, pos, words):
    if isinstance(pop_queue[pos], list):
        print(pos)
        pop_queue[pos].extend(remove_repetitions(pop_queue[pos], words))
    else:
        pop_queue[pos] = words


def prepare_words(total_list, words: str):
    words = words.replace("\n", "  ")
    words = re.split(r' {2,}', words)
    if "" in words:
        words.remove("")
    formatted_words = remove_repetitions(total_list, words)
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
        # words.extend(get_random_number())
        words = words * 2
        random.shuffle(words)
    write_json(data_path, cb_recorder)
    return words


def remove_repetitions(total_list, words):
    res_words = []
    if isinstance(total_list, int):
        res_words.extend(words)
    else:
        for i, w in enumerate(words):
            if w not in total_list:
                res_words.append(w)
            else:
                print(f'<{w}> is filtered causing repetition')
    return res_words


def get_random_number(num=5, ranges=(0, 999)):
    rand_list = [random.randint(ranges[0], ranges[1]) for _ in range(num)]
    return rand_list


cb_recorder = read_json(data_path)

if __name__ == '__main__':
    init_recorder()
    # print(update_words(cb_recorder, ['fork', 'nihao']))
