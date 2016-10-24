#!/usr/bin/env python3
import json
from pprint import pprint
from typing import List

from vkdump.api import get_api


def dump(favs: List):
    with open("fav_posts.json", 'w') as fo:
        json.dump(favs, fo)
        # js = json.dumps(favs, ensure_ascii=False)
        # fo.write(js)


def load() -> List:
    with open("fav_posts.json", 'r') as fo:
        items = json.load(fo)
        return items


def main():
    api = get_api()

    # item = load()[66]
    # pprint(item)
    print(api.get_posts_by_ids(["-106024047_1970"]))
    # favs = api.get_all_favs()
    # dump(favs)


if __name__ == '__main__':
    main()
