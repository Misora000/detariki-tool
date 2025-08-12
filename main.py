import os
from config import *
from manifest import Manifest


if __name__ == '__main__':
    Manifest(MANIFEST_PATH).download_all(CACHE_PATH)