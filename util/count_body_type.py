import os
from common import *

CACHE_BODY_PATH = '../cache/chara/body'

if __name__ == '__main__':
    body_style = {
        '0_0': 0,
        '0_1': 0,
        '0_2': 0,
        '1_0': 0,
        '1_1': 0,
        '1_2': 0,
        '2_0': 0,
        '2_1': 0,
        '2_2': 0,
        '3_0': 0,
        '3_1': 0,
        '3_2': 0,
        '4_0': 0,
        '4_1': 0,
        '4_2': 0,
        '5_0': 0,
        '5_1': 0,
        '5_2': 0,
        '6_0': 0,
        '6_1': 0,
        '6_2': 0,
        '7_0': 0,
        '7_1': 0,
        '7_2': 0,
        '8_0': 0,
        '8_1': 0,
        '8_2': 0,
        '9_0': 0,
        '9_1': 0,
        '9_2': 0,
    }
    for v in dfs(CACHE_BODY_PATH):
        name = os.path.split(v)[1]
        if name.startswith('chara_parts_body_body') and not '_texture_body' in name:
            seg = name.split('_')
            s = f'{seg[-2]}_{seg[-1]}'
            if s in body_style:
                body_style[s] += 1
            else:
                body_style[s] = 1

    for key in body_style:
        print(f'{key}: {body_style[key]}')
            