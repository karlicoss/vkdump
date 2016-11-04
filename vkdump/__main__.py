#!/usr/bin/env python3
import json
from collections import OrderedDict
from pprint import pprint
from typing import List, Dict, Any

from vkdump.api import get_api
from vkdump.data import load_favs, save_favs
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
    favs = load_favs()
    save_favs(favs)
    # api = get_api()
    # favs = api.get_favs(0)
    # pprint(favs[:10])

    # pprint(favs[1])
    # pprint(sort_dict(favs[1]))
    # favs = load_favs()
    # pprint(favs[:10])
    # dates = [f['date'] for f in favs]
    # pprint(dates)
    # print(all(a >= b for a, b in zip(dates, dates[11:])))
    # api = get_api()
    # collect_attaches()
    # favs = fetch_all_favs()
    # with open("favs.json", 'w') as fo: # TODO instead, merge and sort by timestamp?
    #     json.dump(favs, fo, ensure_ascii=False)


if __name__ == '__main__':
    main()
