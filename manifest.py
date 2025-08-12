import os
import argparse
from base import *
from config import *

parser = argparse.ArgumentParser()

parser.add_argument('-f', help='path to manifest.txt', default=MANIFEST_PATH, type=str)
parser.add_argument('-o', help='output path', default=CACHE_PATH, type=str)

class Manifest(Base):
    def __init__(self, path: str):
        with open(path, 'r') as f:
            self.manifest = f.readlines()
    
    def download_all(self, save_dir=''):
        for v in self.manifest:
            seg = v.split('\t')
            if len(seg) != 2:
                continue

            path = seg[1].replace('\n', '')
            output_dir = os.path.join(save_dir, seg[0])
            os.makedirs(output_dir, exist_ok=True)
            # print(os.path.join(output_dir, os.path.split(path)[1]))

            self.cdn_download(path, output_dir)

            # extract texture
            name = os.path.split(path)[1]
            if '_texture_body' in name or seg[0].startswith('pic/'):
                src = os.path.join(output_dir, name)
                if os.path.exists(src):
                    self.extract_texture2D(src, output_dir)


if __name__ == '__main__':
    args = parser.parse_args()

    Manifest(args.f).download_all(args.o)
