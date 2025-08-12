import os, time
import threading, queue
import argparse
import UnityPy
from UnityPy.classes.generated import *
from base import *
from chara_list import *
from config import *
from color import *

parser = argparse.ArgumentParser()

parser.add_argument('-cos', help='costume id', default=0, type=int)
parser.add_argument('-chr', help='character id', default=0, type=int)
parser.add_argument('-o', help='output path', default=CACHE_PATH, type=str)
parser.add_argument('-p', help='thread num (default: 1)', default=1, type=int)


class Costume(Base):
    def __init__(self, input):
        for obj in UnityPy.load(input).objects:
            if obj.type.name == 'TextAsset':
                v: TextAsset = obj.read()

                # name: costume_415070_400
                seg = v.m_Name.split('_')
                if len(seg) != 3 or seg[0] != 'costume':
                    raise ValueError(f'unexpected m_Name: {v.m_Name}')
                
                if not 'cset' in v.m_Script:
                    raise ValueError(f'unexpected m_Script: {v.m_Name} :: {v.m_Script}')
                
                self.cos_id = int(seg[1])
                self.chr_id = int(seg[2])
                
                seg = v.m_Script.split('\n')
                for line in v.m_Script.split('\n'):
                    if not 'cset' in line:
                        continue
                    
                    seg = line.split('\t')
                    # face2508400 -> 2508400
                    self.head_no = seg[-4].replace('face', '')
                    self.head_path = f'chara/parts/head/chara_parts_head_head{self.head_no}'

                    # body41163_2_0 -> 41163
                    self.body_no = seg[-2].split('_')[0].replace('body', '')
                    self.body_path = f'chara/parts/body/chara_parts_body_{seg[-2]}'

                    # conver string
                    #  from: /Chara/Parts/Body/body41163_Texture/body41163_a_a_0_0
                    #  to:   chara_parts_body_body41163_texture_body41163_a_a_0_0
                    self.body_texture_name = seg[-1][1:].replace('/', '_').lower()
                    self.body_texture_path = f'chara/parts/body/body{self.body_no}_texture/{self.body_texture_name}'

                    # TODO: may contain other body id
                    # check 40221_88 & 55386_88
                    break

    def download_head(self, save_dir='') -> int:
        self.cdn_download(self.head_path, save_dir)
    
    def download_body(self, save_dir='') -> int:
        for path in [ self.body_path, self.body_texture_path ]:
            self.cdn_download(path, save_dir)
        # extract addtional body texture
        src = os.path.join(save_dir, self.body_texture_name)
        if os.path.exists(src):
            try:
                self.extract_texture2D(src, save_dir)
            except Exception as e:
                print(e)

    def download_all_assets(self, save_dir=''):
        # A costume includes 3 parts
        #  chara/parts/head/chara_parts_head_head400
        #  chara/parts/body/chara_parts_body_body1497_2_0
        #  chara/parts/body/body1497_texture/chara_parts_body_body1497_texture_body1497_a_a_0_0
        self.download_head(save_dir=os.path.join(save_dir, CACHE_CHR_HEAD))
        self.download_body(save_dir=os.path.join(save_dir, CACHE_CHR_BODY, self.body_no))


    @classmethod
    def from_file(cls, path: str):
        # name should be: costume_costumedata_costume_415070_400
        return cls(path)


    @classmethod
    def from_url(cls, path: str, save_costumedata=False, save_dir=''):
        data = Costume.cdn_get(path)
        c = cls(data)

        if save_costumedata:
            _, name = os.path.split(path)
            output_dir = os.path.join(save_dir, CACHE_CHR_COSTUME)
            os.makedirs(output_dir, exist_ok=True)
            dst = os.path.join(output_dir, name)
            if not os.path.exists(dst) or os.path.getsize(dst) != len(data):
                with open(dst, 'wb') as f:
                    f.write(data)
                    print(f'[ {green(name)} ] downloaded. size={len(data)}')
            else:
                print(f'[ {yellow(name)} ] skipped. file has already existed')
        return c


    @staticmethod
    def costumedata_name(cos_id: int, chr_id: int) -> str:
        return f'costume_costumedata_costume_{cos_id}_{chr_id}'

    @staticmethod
    def costumedata_url(cos_id: int, chr_id: int) -> str:
        return f'costume/costumedata/{Costume.costumedata_name(cos_id, chr_id)}'
    

    @staticmethod
    def special_cos_ids() -> list:
        r = []
        for v in COSTUME_SP_ID_RANGE:
            r += v
        return r




def worker(no: int, q: queue.Queue, lock: threading.Lock):
    while True:
        try:
            req = q.get(timeout=2)
        except:
            break
        seg = req.split('_')
        cos_id = int(seg[0])
        chr_id = int(seg[1])
        # print(f'{no} handles {cos_id}_{chr_id}')

        try:
            c = Costume.from_url(Costume.costumedata_url(cos_id, chr_id), save_costumedata=True, save_dir=args.o)
            c.download_all_assets(save_dir=args.o)
        except ConnectionRefusedError as e:
            print(f'[{red(Costume.costumedata_name(cos_id, chr_id))}] failed. {e}')
            pass
        except FileNotFoundError as e:
            pass
        

        if q.empty():
            break

        # avoid rate-limit from cdn server
        # time.sleep(1)



if __name__ == '__main__':
    args = parser.parse_args()

    chr_ids = []
    cos_ids = []
    
    if args.chr > 0:
        chr_ids.append(args.chr)
    else:
        chr_ids = [i for i in chara_list]

    if args.cos > 0:
        cos_ids.append(args.cos)
    else:
        # read costume id from file
        with open(COSTUME_ID_PATH, 'r') as f:
            for v in f.readlines():
                cos_ids.append(int(v.replace('\n', '')))
        cos_ids += Costume.special_cos_ids()


    # decide the actually number of workers
    args.p = args.p if len(cos_ids)*len(chr_ids) > args.p else len(cos_ids)*len(chr_ids)
    workers: list[threading.Thread] = []
    lock = threading.Lock()
    q = queue.Queue()

    for i in range(args.p):
        t = threading.Thread(target=worker, args=(i, q, lock))
        workers.append(t)
        t.start()

    for chr_id in chr_ids:
        for cos_id in cos_ids:
            q.put(f'{cos_id}_{chr_id}')

    for w in workers:
        w.join()
    