import os

COSTUMEDATA_PATH = '../cache/chara/costumedata'

if __name__ == '__main__':
    ll = []
    for v in os.listdir(COSTUMEDATA_PATH):
        if not v.startswith('costume_costumedata_costume_'):
            continue
        seg = v.split('_')
        ll.append(int(seg[-2]))
    ll.sort()

    ss = 0
    no = 0
    for v in ll:
        if v == no:
            continue

        if v == no + 1:
            no = v
            continue

        if ss == no:
            print(f'{ss}')
        else:
            print(f'{ss}-{no}')
        ss = v
        no = v