import os
import argparse
from base import *
from config import *
from chara_list import *

parser = argparse.ArgumentParser()

parser.add_argument('-save', help='save asset bundle files (default: False)', default=False, action='store_true')
parser.add_argument('-o', help='output path', default=CACHE_PATH, type=str)


class Pic(Base):
    def __download(self, path: str, p_name: str, save_dir='', save_ab=False):
        try:
            a_name = os.path.split(path)[1]
            os.makedirs(save_dir, exist_ok=True)
            if save_ab:
                if not os.path.exists(os.path.join(save_dir, path)):
                    self.cdn_download(path, save_dir)
                if not os.path.exists(os.path.join(save_dir, p_name)):
                    self.extract_texture2D(os.path.join(save_dir, a_name), save_dir)
            else:
                if os.path.exists(os.path.join(save_dir, p_name)):
                    return        
                if not os.path.exists(os.path.join(save_dir, a_name)):
                    data = self.cdn_get(path)
                    self.extract_texture2D(data, save_dir)
                else:
                    self.extract_texture2D(os.path.join(save_dir, a_name), save_dir)
        except Exception as e:
            print(f'[ {red(a_name)} ] failed. {e}')
            pass


    def download_illust(self, no: int, save_dir='', save_ab=False):
        # illustration/illustration_illustration_00001
        path = f'illustration/illustration_illustration_{no:05d}'
        p_name = f'illustration_{no:05d}.png'
        self.__download(path, p_name, os.path.join(save_dir, CACHE_PIC_ILLUST), save_ab)

    def download_comic(self, chr_id: int, save_dir='', save_ab=False):
        # comic/comic_comic_00006_1
        path = f'comic/comic_comic_{chr_id:05d}_1'
        p_name = f'comic_{chr_id:05d}.png'
        self.__download(path, p_name, os.path.join(save_dir, CACHE_PIC_COMIC), save_ab)

    def download_portrait(self, chr_id: int, save_dir='', save_ab=False):
        # portrait/portrait_portrait_00017
        path = f'portrait/portrait_portrait_{chr_id:05d}'
        p_name = f'portrait_{chr_id:05d}.png'
        self.__download(path, p_name, os.path.join(save_dir, CACHE_PIC_PORTRAIT), save_ab)



if __name__ == '__main__':
    args = parser.parse_args()

    p = Pic()

    for id in ILLUST_RANGE:
        p.download_illust(id, args.o, args.save)

    ids = [i for i in chara_list]
    for id in ids:
        p.download_comic(id, args.o, args.save)

    for id in ids:
        p.download_portrait(id, args.o, args.save)