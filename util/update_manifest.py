import os
import argparse
from common import *

MANIFEST_PATH = '../manifest.txt'
CACHE_PATH = '../cache'

parser = argparse.ArgumentParser()

parser.add_argument('-run', help='run (default: False)', default=False, action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()

    # read the original manifest (for compare)
    ori = []
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, 'r') as f:
            ori = f.readlines()
    ori = sort_and_remove_duplicate(ori)
    
    new = []
    for v in dfs(CACHE_PATH):
        if not os.path.isfile(v):
            continue
        
        parent, name = os.path.split(v)
        save_dir = os.path.relpath(parent, CACHE_PATH)
        path = ''

        if name.startswith('chara_parts_body_body'):
            _, id = os.path.split(parent)
            if '_s_texture_body' in name:
                path = f'chara/parts/body/body{id}_0_s_texture/{name}'
            elif '_texture_body' in name:
                path = f'chara/parts/body/body{id}_texture/{name}'
            else:
                path = f'chara/parts/body/{name}'

        elif name.startswith('chara_parts_head_'):
            path = f'chara/parts/head/{name}'

        elif name.startswith('costume_costumedata_costume_'):
            path = f'costume/costumedata/{name}'

        elif name.startswith('comic_') and os.path.splitext(name)[1] == '.png':
            path = f'comic/comic_{os.path.splitext(name)[0]}'

        elif name.startswith('portrait_') and os.path.splitext(name)[1] == '.png':
            path = f'portrait/portrait_{os.path.splitext(name)[0]}'

        elif name.startswith('illustration_') and os.path.splitext(name)[1] == '.png':
            path = f'illustration/illustration_{os.path.splitext(name)[0]}'

        if len(path) > 0:
            new.append(f'{save_dir}\t{path}\n')

    new = sort_and_remove_duplicate(new)

    print(f'manifest.txt: {len(ori)}')
    print(f'now in cache: {len(new)}')

    if args.run:
        with open(MANIFEST_PATH, 'w') as f:
            f.writelines(new)
