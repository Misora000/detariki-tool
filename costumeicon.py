import os
import argparse
from base import *
from config import *
from chara_list import *

parser = argparse.ArgumentParser()

parser.add_argument('-id', help='icon id', default=0, type=int)
parser.add_argument('-save', help='save asset bundle files (default: False)', default=False, action='store_true')
parser.add_argument('-o', help='output path', default=CACHE_PATH, type=str)


class CostumeIcon(Base):
    dummy_r3_size = 3020
    dummy_r4_size = 2762
    dummy_r5_size = 4570
    dummy_change_size = 324

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
            # print(f'[ {red(a_name)} ] failed. {e}')
            pass


    def download_costumeicon(self, no: int, save_dir='', save_ab=False):
        # costumeicon/costumeicon_costume_icon_30007
        path = f'costumeicon/costumeicon_costume_icon_{no}'
        p_name = f'costume_icon_{no}.png'
        self.__download(path, p_name, os.path.join(save_dir, CACHE_CHR_COSTUME_ICON), save_ab)

        # remove dummy
        path_p = os.path.join(save_dir, CACHE_CHR_COSTUME_ICON, p_name)
        path_ab = os.path.join(save_dir, CACHE_CHR_COSTUME_ICON, os.path.split(path)[1])
        if self.isdummy(no, path_p):
            try:
                os.remove(path_p)
                print(f'[ {red(p_name)} ] is dummy, delete')
                if not os.path.exists(path_ab):
                    return
                os.remove(path_ab)
                print(f'[ {red(os.path.split(path)[1])} ] is dummy, delete')
            except Exception as e:
                print(f'[ {red(p_name)} ] {e}')
                pass
        

    def isdummy(self, no: int, path_p: str) -> bool:
        if not os.path.exists(path_p):
            return False
        
        size = os.path.getsize(path_p)
        if no < 60000 and no >= 50000:
            return size == self.dummy_r5_size
        if no < 50000 and no >= 40000:
            return size == self.dummy_r4_size
        if no < 40000 and no >= 30000:
            return size == self.dummy_r3_size
        return False


    def download_costumechangeicon(self, no: int, save_dir='', save_ab=False):
        # costumeicon/costumeicon_costume_icon_30007
        path = f'costumechangeicon/costumechangeicon_costume_change_icon_{no}'
        p_name = f'costume_change_icon_{no}.png'
        self.__download(path, p_name, os.path.join(save_dir, CACHE_CHR_COSTUME_CHANGE_ICON), save_ab)

        # remove dummy
        path_p = os.path.join(save_dir, CACHE_CHR_COSTUME_CHANGE_ICON, p_name)
        path_ab = os.path.join(save_dir, CACHE_CHR_COSTUME_CHANGE_ICON, os.path.split(path)[1])
        if os.path.exists(path_p) and os.path.getsize(path_p) == self.dummy_change_size:
            try:
                os.remove(path_p)
                print(f'[ {red(p_name)} ] is dummy, delete')
                if not os.path.exists(path_ab):
                    return
                os.remove(path_ab)
                print(f'[ {red(os.path.split(path)[1])} ] is dummy, delete')
            except Exception as e:
                print(f'[ {red(p_name)} ] {e}')
                pass



if __name__ == '__main__':
    args = parser.parse_args()

    p = CostumeIcon()

    if args.id > 0:
        p.download_costumeicon(args.id, args.o, args.save)
        p.download_costumechangeicon(args.id, args.o, args.save)
        if args.id < 100000:
            p.download_costumechangeicon(args.id+900000, args.o, args.save) # 差分ver.

    else:
        r = []
        for v in COSTUME_ICON_ID_RANGE:
            r += v

        for id in r:
            p.download_costumeicon(id, args.o, args.save)

        for v in COSTUME_CHANGE_ICON_ID_RANGE:
            r += v
        for id in r:
            p.download_costumechangeicon(id, args.o, args.save)
            if id < 100000:
                p.download_costumechangeicon(id+900000, args.o, args.save)