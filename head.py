import os
import argparse
from base import *
from chara_list import *
from config import *
from color import *

parser = argparse.ArgumentParser()

parser.add_argument('-id', help='head id', default='', type=str)
parser.add_argument('-o', help='output path', default=CACHE_PATH, type=str)


class Head(Base):
    def __init__(self, id: str):
        """
        The naming of head ID has many formats:
        - Character ID, ex: 1, 2, 313, 400
        - Character ID followd by some string, ex: 19san1
        - An unkown ID foloowd by character ID, ex: 200504 (=2005 & 04), 2008400 (=2008 & 400)
        - More addtional string, ex: 2412383_2 = (2412 & 383 & _2), 20080502 (=2008 & 05 & 02)
        """
        self.id = id

    def download(self, save_dir=''):
        # chara/parts/head/chara_parts_head_head400
        path = f'chara/parts/head/chara_parts_head_head{self.id}'
        output_dir = os.path.join(save_dir, CACHE_CHR_HEAD)
        dl_size = self.cdn_download(path, output_dir)
        # download QBi version
        if  dl_size >= 0:
            # chara/parts/head/chara_parts_head_head400_s
            path = f'chara/parts/head/chara_parts_head_head{self.id}_s'
            output_dir = os.path.join(save_dir, CACHE_CHR_HEAD_S)
            self.cdn_download(path, output_dir)

    @staticmethod
    def possible_id_range() -> list:
        r = []
        for v in HEAD_ID_RANGE:
            r += v
        return r



if __name__ == '__main__':
    args = parser.parse_args()

    ids = [args.id]
    if len(args.id) == 0:
        # read head id from file
        with open(HEAD_ID_PATH, 'r') as f:
            for v in f.readlines():
                ids.append(v.replace('\n', ''))
        ids += Head.possible_id_range()

    for id in ids:
        if len(id) > 0:
            Head(id).download(args.o)
