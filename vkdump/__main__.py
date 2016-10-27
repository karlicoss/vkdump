#!/usr/bin/env python3
import json
import logging
from pprint import pprint
from time import sleep
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


def load_favs_ids() -> List[str]:
    with open("posts.json", 'r') as fo:
        posts = json.load(fo)
        return posts


def fetch_all_favs() -> List[dict]:
    logger = logging.getLogger('FavsFetcher')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # logger.error("FEWFWEF")

    api = get_api()
    ids = load_favs_ids()
    BUCKET_SIZE = 100  # not sure how much is allowed
    fav_posts = []  # TODO ordering?
    not_found = set()
    for start in range(0, len(ids), BUCKET_SIZE):
        cur_ids = ids[start: start + BUCKET_SIZE]
        posts = api.get_posts_by_ids(cur_ids)
        logger.info("Queried %d items, got %d posts", len(cur_ids), len(posts))
        posts_ids = [str(p['owner_id']) + "_" + str(p['id']) for p in posts]
        expected = set(cur_ids)
        actual = set(posts_ids)
        unexpected = actual.difference(expected)
        if len(unexpected) > 0:
            raise AssertionError("Unexpected items: " + str(unexpected))
        cur_not_found = expected.difference(actual)
        logger.debug("Not found: %s", str(cur_not_found))
        fav_posts.extend(posts)
        not_found.update(cur_not_found)
        sleep(1)
    print("Total items: " + str(len(fav_posts)))
    print("Not found:")
    pprint(sorted(list(not_found)))
    return fav_posts


def main():
    api = get_api()
    favs = fetch_all_favs()
    with open("favs.json", 'w') as fo: # TODO instead, merge and sort by timestamp?
        json.dump(favs, fo, ensure_ascii=False)


if __name__ == '__main__':
    main()
