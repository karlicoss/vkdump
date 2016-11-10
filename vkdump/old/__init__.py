import logging
from pprint import pprint
from time import sleep
from typing import List

from vkdump.api import get_api


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
    ids = []  # type: List
    # ids = load_favs_ids()
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