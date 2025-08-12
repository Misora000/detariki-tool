import os
import argparse
from common import *

HEAD_ID_PATH = '../head-id.txt'
HEAD_PATH = '../cache/chara/head'

parser = argparse.ArgumentParser()

parser.add_argument('-run', help='run (default: False)', default=False, action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()

    # source 1: the original head-id.txt
    with open(HEAD_ID_PATH, 'r') as f:
        id_curr = [i.replace('\n', '') for i in f.readlines()]
    id_curr = sort_and_remove_duplicate(id_curr)

    # source 2: head in cache
    id_head = []
    for v in os.listdir(HEAD_PATH):
        if v.startswith('chara_parts_head_head'):
            id_head.append(v[len('chara_parts_head_head'):])
    id_head = sort_and_remove_duplicate(id_head)

    # merge all sources
    id_merged = sort_and_remove_duplicate(id_curr + id_head)

    print(f'  costume-id.txt: {len(id_curr)}')
    print(f'+    costumedata: {len(id_head)}')
    print('-' * 24)
    print(f'          merged: {len(id_merged)}')


    # update costume-id.txt
    if args.run and len(id_merged) > 0:
        with open(HEAD_ID_PATH, 'w') as f:
            f.writelines([f'{id}\n' for id in id_merged])