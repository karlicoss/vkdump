import json
from typing import List

from vkdump.config import config


# TODO sorted by timestamp?
def load_favs() -> List[dict]:
    with config.FAVS.open('r') as fo:
        favs = json.load(fo)
        return favs
