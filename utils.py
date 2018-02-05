# -*- coding:utf-8 -*-

def read_headers():
    with open("data/headers.txt") as f:
        lines = f.readlines()
        headers = dict()
        for line in lines:
            splited = line.strip(":")
            key = splited[0]
            value = "".join(splited[1:])
            headers[key] = value
    return headers

