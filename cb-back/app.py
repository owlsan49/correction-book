# -*- coding: utf-8 -*-
# Copyright (c) 2022, Shang Luo
# All rights reserved.
# 
# Author: 罗尚
# Building Time: 2024/3/1
# Reference: None
# Description: None
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import (read_json, cb_recorder, update_words,
                   prepare_words, get_words)

app = Flask(__name__)
CORS(app)


@app.route('/push_words', methods=['POST'])
def push_words():
    results = {'resCode': 0}
    words = request.get_json()['desc']
    words = prepare_words(cb_recorder["total_list"], words)
    info = update_words(cb_recorder, words)
    results.update(info)
    return jsonify(results)


@app.route('/pop_words', methods=['GET'])
def pop_words():
    results = {'resCode': 0}
    words = get_words(cb_recorder)
    results['words'] = words
    if len(words) == 0:
        results['info'] = 'Today is no words to review. Have a good DAY!'
    else:
        results['info'] = ""
    return jsonify(results)


if __name__ == '__main__':
    port = read_json('../config.json')['port']
    app.run(debug=True, port=port)
