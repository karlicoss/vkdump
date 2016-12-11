import json
import logging
from pprint import pprint
from urllib.request import urlretrieve
from time import sleep
from typing import List, Set, Dict

from vkdump.api import get_api
from vkdump.config import config
from vkdump.data import load_favs
from vkdump.entities.attachments import PhotoAttach


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


# https://vk.com/dev/attachments_w

IGNORED_TYPES = {
    'audio',
    'doc',
    'page',
    'video',
}

TYPES = {
    'album',
    'graffiti',
    'link',
    'note',
    'photo',
    'photos_list',
    'poll',
    'posted_photo',
}


def get_attachments(fav: Dict[str, Dict]) -> List[Dict]:
    attaches = fav.get('attachments', [])
    att = []
    for a in attaches:
        t = a['type']
        if t not in TYPES and t not in IGNORED_TYPES:
            # TODO logger
            print("Unexpected type: " + t + " in " + str(fav))
        if t in TYPES:
            att.append(a)
    return att


def collect_images() -> Set[str]:
    favs = load_favs()
    attaches = set()
    for fav in favs:
        att = get_attachments(fav)
        photos = [a for a in att if a['type'] == 'photo']
        for photo in photos:
            att = PhotoAttach.from_json(photo)
            attaches.add(att)
    for i, a in enumerate(attaches):
        u = a.best_url()
        print("Retreiving [%d/%d]: %s" % (i, len(attaches), u))
        urlretrieve(u, config.IMAGES_DIR.joinpath(a.photo_id()).as_posix())
    # print(urls)