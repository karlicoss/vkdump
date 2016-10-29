#!/usr/bin/env python3
import json
from typing import List

from vkdump.api import get_api
from vkdump.old import collect_attaches


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
    collect_attaches()
    # favs = fetch_all_favs()
    # with open("favs.json", 'w') as fo: # TODO instead, merge and sort by timestamp?
    #     json.dump(favs, fo, ensure_ascii=False)


if __name__ == '__main__':
    main()
