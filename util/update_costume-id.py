import os
import argparse
from common import *

COSTUME_ID_PATH = '../costume-id.txt'
COSTUMEDATA_PATH = '../cache/chara/costumedata'

parser = argparse.ArgumentParser()

parser.add_argument('-i', help='path to request dump of costume icon', default='', type=str)
parser.add_argument('-run', help='run (default: False)', default=False, action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()

    # source 1: the original costume-id.txt
    with open(COSTUME_ID_PATH, 'r') as f:
        id_curr = [int(i.replace('\n', '')) for i in f.readlines()]
    id_curr = sort_and_remove_duplicate(id_curr)

    # source 2: request dump of costume icon
    id_icon = []
    if os.path.exists(args.i) and os.path.isdir(args.i):
        for v in os.listdir(args.i):
            if v.startswith('costumeicon_costume_icon_'):
                id_icon.append(int(v.split('_')[-1]))
    id_icon = sort_and_remove_duplicate(id_icon)

    # source 3: costumedata in cache
    id_costumedata = []
    for v in os.listdir(COSTUMEDATA_PATH):
        if v.startswith('costume_costumedata_costume_'):
            id_costumedata.append(int(v.split('_')[-2]))
    id_costumedata = sort_and_remove_duplicate(id_costumedata)

    # merge all sources
    id_merged = sort_and_remove_duplicate(id_curr + id_icon + id_costumedata)

    print(f'  costume-id.txt: {len(id_curr)}')
    print(f'    costume icon: {len(id_icon)}')
    print(f'+    costumedata: {len(id_costumedata)}')
    print('-' * 24)
    print(f'          merged: {len(id_merged)}')


    # update costume-id.txt
    if args.run and len(id_merged) > 0:
        with open(COSTUME_ID_PATH, 'w') as f:
            f.writelines([f'{id}\n' for id in id_merged])