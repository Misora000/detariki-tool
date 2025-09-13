CACHE_PATH = 'cache'
CACHE_CHR_HEAD = 'chara/head'
CACHE_CHR_BODY = 'chara/body'
CACHE_CHR_COSTUME = 'chara/costumedata'
CACHE_CHR_COSTUME_ICON = 'chara/costumeicon'
CACHE_CHR_COSTUME_CHANGE_ICON = 'chara/costumechangeicon'
CACHE_CHR_HEAD_S = 'chara/head-s'
CACHE_CHR_BODY_S = 'chara/body-s'
CACHE_CHR_COSTUME_S = 'chara/costumedata-s'
CACHE_PIC_ILLUST = 'pic/illust'
CACHE_PIC_COMIC = 'pic/comic'
CACHE_PIC_PORTRAIT = 'pic/portrait'

MANIFEST_PATH = 'manifest.txt'


# ------------------------ costume ----------------------
COSTUME_ID_PATH = 'costume-id.txt'
COSTUME_SP_ID_RANGE = [
    # # common swimsuits
    [30039, 40048],
    # # underwear
    range(300000, 300010),
    range(300100, 300120),
    range(300200, 300230),
    range(300300, 300310),
    range(300400, 300410),
    range(300500, 300520),
    range(300600, 300610),
    # # nude
    range(100000, 100120, 10),
    # range(400000, 416000, 10), # ex: 409750 415150
]

COSTUME_ICON_ID_RANGE = [
    range(10000, 10020),
    range(20000, 20030),
    range(30000, 30300),
    range(40000, 40500),
    range(50000, 50500),
    range(55000, 55700),
    range(90000, 90200),
]

COSTUME_CHANGE_ICON_ID_RANGE = [
    range(108000, 108050),
    range(109000, 109050),
]

# ------------------------ body ------------------------
# The possible id range of body asset
BODY_ID_RANGE = [
    range(5, 10),            # nude
    range(10, 35),           # underwear
    range(100, 200),
    range(500, 1600),
    range(10000, 10041, 10), # nude
    range(10100, 10150, 10), # half nude
    range(20001, 20500, 1),  # half nude
    range(30000, 30300),     # underwear
    range(40000, 41200), 
]
# List the known body type and its texture parameter.
# Comment the types with zero or less instances (up-to-date 2025-08-12).
BODY_STYLE_TYPE = {
    '0_0': 'a_a',
    '0_1': 'a_a',
    # '0_2': 'a_a',
    '1_0': 'a_a',
    '1_1': 'a_a',
    # '1_2': 'a_a',
    '2_0': 'a_a',
    '2_1': 'a_a',
    # '2_2': 'a_a',
    # '3_0': '3_0', # 1
    # '3_1': '3_1',
    # '3_2': '3_2',
    '4_0': '4_0',
    # '4_1': '4_1',
    # '4_2': '4_2',
    '5_0': '5_0',
    # '5_1': '5_1',
    # '5_2': '5_2',
    '6_0': '6_0',
    # '6_1': '6_1',
    # '6_2': '6_2',
    '7_0': '7_0',
    '7_1': '7_1',
    # '7_2': '7_2',
    '8_0': '8_0', # 4
    '8_1': '8_1',
    # '8_2': '8_2',
    '9_0': '9_0',
    # '9_1': '9_1',
    '9_2': '9_2', # 6
}
BODY_SKIN_COLOR_RANGE = range(5)
BODY_CLOTH_COLOR_RANGE = range(50)


# ------------------------ head ------------------------
HEAD_ID_PATH = 'head-id.txt'
HEAD_ID_RANGE = []


# ------------------------ picture ---------------------
ILLUST_RANGE = range(1, 90) 