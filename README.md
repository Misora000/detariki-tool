# Detariki-Tool
A tool for collecting assets (3D model, image) of FANZA(DMM) game [デタリキZ](https://games.dmm.com/detail/detarikiz) and [デタリキZX](https://games.dmm.co.jp/detail/detarikizx) (R-18 ver.).  

## About This Game
Althougn has destop / iOS / Android app, デタリキ basically is a web game which doesn't cache any streaming assets on your device. Moreover, it doesn't have a common manifest file so that we can not get the whole asset list easily. Therefore I make this project to collect assets and maintain my own manifest.

## Installation
- Install [Python 3.13](https://www.python.org/downloads/) or newer
- Install [pip](https://pip.pypa.io/en/stable/installation/)
- Install dependencies
```sh
pip install -r requirements.txt
```

## Usage: For Normal Users (No Engineer Background)
Download assets I list in my own [manifest]().
```sh
python main.py
```

## Usage: For Professional Users
If you want to find assets not list in manifest.txt, you can run scripts manually.

### Function Overview
|Script|Description|說明|
|---|---|---|
|body.py|Download the body part of 3D model & QBi model|下載3D模型和Q版模型的身體部件|
|head.py|Download the head part of 3D model & QBi model|下載3D模型和Q版模型的頭部件|
|costume.py|Download full set of costume of 3D model & QBi model|下載完整的服裝模型(包含頭部與身體)|
|pic.py|Download image objects like illlustration, comic, portrait|下載插圖、漫畫等圖片|
||||

Be aware that in the following explanation, the term `possible` does not refer to any truly potential outcome, but rather to outcomes within a `predefined range of results`. Therefore, it does not encompass possibilities outside that range.  

You can change the predefined range in [config.py]()

Before using this tool, you must need to know there's no any official manifest so that this tool basically uses `Brute-Force` to try assets url from CDN. All we can do is try to minimize the search range of brute-force.  

Hence, I recommand you run `body.py` & `head.py` first because the search range of `costume.py` is too large and takes lots of time.  
(Body is shared object for every characters, head is exclusive to everyone, but costume is the combination of body, head and character.)

In general you should't know the id of body, head and costume unless you know how to capture the http request which carries id in url.  
Run the following commands without knowing id.

```sh
python body.py
python head.py
python costume.py
python pic.py

# if you got rate limited from CDN server when running costume.py,
# you can manually shard commands by character id, run one character a time.
# ex:
python costume.py -chr 1
python costume.py -chr 2
...
python costume.py -chr 400
```
You can get character id from [chara_list.py]()
  
  
If you are interesting in mining or finding the missed/unlisted assets, see the paremeter detail of each scripts.

### Download Body
Body id is simply an integer but distributed across many different ranges. 
|Range|Cloth Type|
|---|---|
|`[5, 10)`, `[10000, 10040]`|Nude|
|`[10100, 10150]`, `[20000, 20150]`|Half Nude|
|`[10, 35]`, `[30000, 30300)`|Underwear|
|`[100, 200)`, `[500, 1600)`|Common, Character Basic|
|`[40000, 41200]`|Unique, New|
```sh
usage: body.py [-h] [-id ID] [-o O]

options:
  -h, --help  show this help message and exit
  -id ID      body id
  -o O        output path

# example: download body 30020 & its textures
python body.py -id 30020

# example: download all possible bodies & textures
python body.py
```
### Download Head
Head id has many formats so it's no way to brute-force search the potential range.
|Format|Excample|
|---|---|
|Character ID|`1`, `2`, `313`, `400`|
|Character ID followd by some string|`19san1`|
|An unkown ID foloowd by character ID|`200504` (=2005 & 04), `2008400` (=2008 & 400)|
|More addtional string|`2412383_2` = (2412 & 383 & _2), `20080502` (=2008 & 05 & 02)|
```sh
usage: head.py [-h] [-id ID] [-o O]

options:
  -h, --help  show this help message and exit
  -id ID      head id
  -o O        output path

# example: download head 400
python head.py -id 400

# example: download all listed in head-id.txt
python head.py
```
### Download Costume
Costume is a combination structure of body, head and character.  
Costume id is an integer like body id but not the same value and currently I don't know the naming rule.  
I got a list of [costume id]() from the gallery page in game, however obviously the ids in this list are all concern to gacha and item, there still has many costumes (ex: nude) without any gacha or item icon.
```sh
usage: costume.py [-h] [-cos COS] [-chr CHR] [-o O] [-p P]

options:
  -h, --help  show this help message and exit
  -cos COS    costume id
  -chr CHR    character id
  -o O        output path
  -p P        thread num (default: 10)

# example: download costume 55524 of character 400, it contains body 1497 & head 400
python costume.py -cos 55524 -chr 400

# example: download all possible costumes of character 1
python costume.py -chr 1

# example: download everyones' costume 300200, it contains body 30020 & everyones' head
python costume.py -cos 300200

# example: download all possible costume
python costum.py
```

### Download Picture
```sh
usage: pic.py [-h] [-save] [-o O]

options:
  -h, --help  show this help message and exit
  -save       save asset bundle files (default: False)
  -o O        output path

# example: download all image objects and convert to .png
python pic.py
```

## Future work