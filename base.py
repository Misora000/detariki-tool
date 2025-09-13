import os
import requests
import UnityPy
from config import *
from color import *

class Base():
    URL_API = 'https://api.detarikiz.com'
    URL_CDN = 'https://detarikiz.cdn.dmmgames.com'
    PLATFORM = 'assets2022/StandaloneWindows64'

    @staticmethod
    def cdn_get(path: str) -> bytes:
        # https://detarikiz.cdn.dmmgames.com/assets2019/StandaloneWindows64/{path}
        url = f'{Base.URL_CDN}/{Base.PLATFORM}/{path}'
        r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
        if r.status_code == requests.codes.not_found:
            # raise FileNotFoundError(f'[{r.status_code}] {url}')
            raise FileNotFoundError(f'[{r.status_code}] not found')
        elif r.status_code != requests.codes.ok:
            # return ConnectionRefusedError(f'[{r.status_code}] {url}')
            return ConnectionRefusedError(f'[{r.status_code}]')
        data = r.content
        r.close()
        return data
    
    @staticmethod
    def cdn_download(path: str, save_dir='') -> int:
        """
        Check existence before download.
        """
        _, name = os.path.split(path)
        dst = os.path.join(save_dir, name)
        if os.path.exists(dst):
            print(f'[ {yellow(name)} ] skipped. file has already existed')
            return 0

        try:
            data = Base.cdn_get(path)
            os.makedirs(save_dir, exist_ok=True)
            with open(dst, 'wb') as f:
                f.write(data)
                print(f'[ {green(name)} ] downloaded. size={len(data)}')
            return len(data)
        
        except Exception as e:
            print(f'[ {red(name)} ] failed. {e}')
            return -1
        
    @staticmethod
    def extract_texture2D(input, save_dir=''):
        u = UnityPy.load(input)
        for obj in u.objects:
            if obj.type.name == 'Texture2D':
                f_name = obj.peek_name()+'.png'
                dst = os.path.join(save_dir, f_name)
                if os.path.exists(dst):
                    continue
                
                os.makedirs(save_dir, exist_ok=True)
                img = obj.read().image
                img.save(dst)
                print(f'[ {green(f_name)} ] extracted')

