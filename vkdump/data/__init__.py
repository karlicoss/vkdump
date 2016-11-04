import json
from typing import List

from vkdump.config import config


def load_favs() -> List[dict]:
    with config.FAVS.open('r') as fo:
        favs = json.load(fo)
        return favs


def save_favs(favs: List[dict]) -> None:
    with config.FAVS.open('w') as fo:
        json.dump(favs, fo, indent=5, ensure_ascii=False, sort_keys=True)