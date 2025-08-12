import os
import argparse
from base import *
from config import *

parser = argparse.ArgumentParser()

parser.add_argument('-id', help='body id', default=0, type=int)
parser.add_argument('-o', help='output path', default=CACHE_PATH, type=str)


class Body(Base):
    def __init__ (self, id: int):
        self.id = id
        self.b_type = BODY_STYLE_TYPE
        self.t_p1_range = BODY_SKIN_COLOR_RANGE
        self.t_p2_range = BODY_CLOTH_COLOR_RANGE

    def download_all(self, save_dir=''):
        """
        Try to download all possible assets related to this body no.
        """
        found = False
        output_dir = os.path.join(save_dir, CACHE_CHR_BODY, str(self.id))
        for b in self.b_type:
            # try main asset, it may contain versions with many different body types
            if self.cdn_download(self.body_path(self.id, b), output_dir) < 0:
                continue

            found = True
            # if found this body types, then found its related textures
            # body texture may contain versions with many different skin colors or cloth colors 
            for p1 in self.t_p1_range:

                # p1 is for skin colors, try all possible
                for p2 in self.t_p2_range:

                    # p2 is for cloth colors, assume it starts from 0 and continuously incrementing uninterrupted
                    if self.cdn_download(self.texture_path(self.id, self.b_type[b], p1, p2), output_dir) < 0:
                        break

                    # extract image if download texture asset successfully
                    p_texture = os.path.join(output_dir, self.texture_name(self.id, self.b_type[b], p1, p2))
                    if os.path.exists(p_texture):
                        self.extract_texture2D(p_texture, output_dir)

        # download QBi version
        if found:
            output_dir = os.path.join(save_dir, CACHE_CHR_BODY_S, str(self.id))
            if self.cdn_download(self.body_s_path(self.id), output_dir) >= 0:
                self.cdn_download(self.texture_S_path(self.id), output_dir)
                # extract image if download texture asset successfully
                p_texture = os.path.join(output_dir, self.texture_s_name(self.id))
                if os.path.exists(p_texture):
                    self.extract_texture2D(p_texture, output_dir)


    @staticmethod
    def body_name(id: int, body_type='0_0'):
        # chara_parts_body_body1497_2_0
        return f'chara_parts_body_body{id}_{body_type}'
    
    @staticmethod
    def body_path(id: int, body_type='0_0'):
        # chara/parts/body/chara_parts_body_body1497_2_0
        return f'chara/parts/body/{Body.body_name(id, body_type)}'
    
    @staticmethod
    def texture_name(id: int, body_type = 'a_a', p1 = 0, p2 = 0):
        # chara_parts_body_body1497_texture_body1497_a_a_0_0
        return f'chara_parts_body_body{id}_texture_body{id}_{body_type}_{p1}_{p2}'
    
    @staticmethod
    def texture_path(id: int, body_type = 'a_a', p1 = 0, p2 = 0):
        # chara/parts/body/body1497_texture/chara_parts_body_body1497_texture_body1497_a_a_0_0
        return f'chara/parts/body/body{id}_texture/{Body.texture_name(id, body_type, p1, p2)}'


    @staticmethod
    def body_s_name(id: int):
        # chara_parts_body_body517_0_s
        return f'chara_parts_body_body{id}_0_s'
    
    @staticmethod
    def body_s_path(id: int):
        # chara/parts/body/chara_parts_body_body517_0_s
        return f'chara/parts/body/{Body.body_s_name(id)}'
    
    @staticmethod
    def texture_s_name(id: int):
        # chara_parts_body_body517_0_s_texture_body517_0_s_0_0
        return f'chara_parts_body_body{id}_0_s_texture_body{id}_0_s_0_0'
    
    @staticmethod
    def texture_S_path(id: int):
        # chara/parts/body/body517_0_s_texture/chara_parts_body_body517_0_s_texture_body517_0_s_0_0
        return f'chara/parts/body/body{id}_0_s_texture/{Body.texture_s_name(id)}'


    @staticmethod
    def possible_id_range() -> list:
        r = []
        for v in BODY_ID_RANGE:
            r += v
        return r
        


if __name__ == '__main__':
    args = parser.parse_args()

    ids = [args.id]
    if args.id == 0:
        ids = Body.possible_id_range()

    for id in ids:
        b = Body(id)
        b.download_all(args.o)
        